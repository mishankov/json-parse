import pjson/parse
import pjson/position

when isMainModule:
    let content = readFile("patient.json")
    echo content

    let p1 = Position(line: 2, column: 3)
    let p2 = p1.copy()
    let p3 = Position(line: 3, column: 3)

    echo p1 == p2
    echo p1 == p3
