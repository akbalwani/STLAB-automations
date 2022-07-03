import win32com.client
import os
import json
# from datetime import datetime, timedelta
from datetime import date
import pysftp
from os.path import exists

# SFTP vars
fn = r'C:\automation\License-automation\known_hosts'

# cnopts = pysftp.CnOpts(knownhosts=fn)
cnopts = pysftp.CnOpts
cnopts.hostkeys = None


# Load the server details
with open(r'.\server-details\servers.json', 'r') as file:
    list_of_servers = json.load(file)


# Get inbox details
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")
for account in mapi.Accounts:
    print(account.DeliveryStore.DisplayName)
inbox = mapi.GetDefaultFolder(6)  # Inbox folder
# inbox = inbox.Folders["some-folder"] #Folder inside Inbox Folder
messages = inbox.Items
target_date = date.today() 
#target_date = date(2022, 6, 30)  # this is for a test run
received_dt = target_date.strftime('%m/%d/%Y %H:%M %p')
email_sender = 'fulfillment@axway.com'
email_subject = 'April 2022 Monthly Eval Licenses' # for test
# messages = messages.Restrict("[ReceivedTime] >= '"+received_dt+"'")
parentDir = 'C:\\automation\\License-automation\\resultfiles\\'
# date_time = datetime.today()
Lic_path = os.path.join(
    parentDir, target_date.strftime("%Y-%m-%d"))
os.mkdir(Lic_path)
print("Directory '% s' created" % Lic_path)

#another confirmation that files are downloaded from attachements already, assuming there are no files today -> setting a flag to false
Flag = False

try:
    for message in list(messages):
        if message.subject.endswith("Monthly Eval Licenses") and message.Senton.date() == target_date:

            try:
                s = message.sender
                for attachment in message.Attachments:

                    if attachment.FileName.startswith('ST'):
                        attachment.SaveASFile(os.path.join(
                            Lic_path, attachment.FileName))
                        print(
                            f"attachment {attachment.FileName} from {s} saved")

                    Flag = True   #Setting flag to true since files are availble 

            except Exception as e:
                print("Error when saving the attachment:" + str(e))

except Exception as e:
    print("Error when processing emails messages:" + str(e))


#ST_core_tmp = Lic_path + "\\ST Core Temp.txt" //filename changed from ST core temp.txt to ST core temp [oracle]
ST_core_tmp = Lic_path + "\\ST Core Temp.txt"
ST_feature_mysql = Lic_path + "\\ST2 Features Temp [MSQL].txt"
ST_feature_postgres = Lic_path + "\\ST2 Features Temp [PostgreSQL].txt"
ST_feature_oracle = Lic_path + "\\ST2 Features [Oracle].txt"
#ST_feature_oracle = Lic_path + "\\ST2 Features Temp.txt"

# Rename or copy ST core temp.txt to filedrive.license
# Rename or copy ST2 Features Temp [MSQL].txt to st.license
# connect to SFTP remotes and upload files to SecureTransport/conf
core_lic_exists = exists(ST_core_tmp)
feat_lic_exists = exists(ST_feature_mysql)
#condition below checks that the path for St_core_tmp and ST_features_mysql (this does not gareuntee file availability) is not null and Flag for file availability is also set to true.

if (ST_core_tmp and ST_feature_mysql) and Flag == True:
    for i in range(len(list_of_servers["servers"])):
        current_host = list_of_servers["servers"][i]["host"]
        with pysftp.Connection(host=list_of_servers["servers"][i]["host"], username=list_of_servers["servers"][i]["username"], password=list_of_servers["servers"][i]["password"], cnopts=None) as sftp:
            print(
                f'\nConnection successfully established ...to {current_host} ')

            sftp.cwd(list_of_servers["servers"][i]["remote_path"])

            sftp.put(
                ST_core_tmp, list_of_servers["servers"][i]["remote_path"]+"conf/filedrive.license")
            print(f"Added filedrive.licene to host {current_host} :)")
            if list_of_servers["servers"][i]["install_type"] == "mysql":
                sftp.put(ST_feature_mysql,
                         list_of_servers["servers"][i]["remote_path"]+"conf/st.license")
                print(f"Added st.license for mysql to host {current_host}")
                print("##########Seperator###########")
            elif list_of_servers["servers"][i]["install_type"] == "oracle":
                sftp.put(
                    ST_feature_oracle, list_of_servers["servers"][i]["remote_path"]+"conf/st.license")
                print(
                    f"Added st.license for oracle to the host {current_host}")
                print("##########Seperator###########")
else:
    print("no files today!!")
    os.rmdir(Lic_path)
    print(f"removed {Lic_path}")
