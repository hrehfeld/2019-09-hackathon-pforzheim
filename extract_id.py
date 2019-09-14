import json
import re


def extract_id(datastore):
    filtered = ""

    # print the keys and values
    for lines in datastore["recognitionResult"]["lines"]:
        print(lines["text"].replace)

    with open("orders.json", 'w') as f:
        json.dump(filtered, f)

if __name__ == '__main__':
    with open("out.jpg.2.json", 'r') as f:
        datastore = json.load(f)
        extract_id(datastore)
    

