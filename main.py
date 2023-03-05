import pjson
import json


if __name__ == "__main__":
    text = ""
    with open("./patient.json") as file:
        text = file.read()

    print(pjson.parse(text, print_tokens=True))
    print(json.loads(text))
    # print(pjson.parse('["\\\\"]'))
    # print(json.loads('["\\\\"]'))

    # s = "\\"
    # print(s)
    # l = [s]
    # l.append(s)
    # print(l)

    print("\\")
