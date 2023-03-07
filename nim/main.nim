import pjson/parse
import pjson/position
import pjson/lexer

when isMainModule:
    let content = readFile("patient.json")
    echo content

    var myLexer = newLexer(content)
    echo myLexer.tokens()
