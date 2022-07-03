import json

personDict = {
    'bill': 'tech',
    'federer': 'tennis',
    'ronaldo': 'football',
    'woods': 'golf',
    'ali': 'boxing'
}

with open('person.txt', 'w') as json_file:
    json.dump(personDict, json_file)
    print("something:")
