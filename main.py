import pjson


if __name__ == "__main__":
    text = ""
    with open("./patient.json") as file:
        text = file.read()

    print(pjson.parse(text))
