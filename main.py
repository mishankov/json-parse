import pjson
import json


if __name__ == "__main__":
    text = ""
    with open("./patient.json", newline="\n") as file:
        text = file.read()

    # print(pjson.parse(text, print_tokens=True))
    # print(json.loads(text))
    print(pjson.parse('"\\n"', print_tokens=True))
    print(json.loads('"\\n"'))
