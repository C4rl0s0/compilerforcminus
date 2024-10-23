keywords = {"else", "if", "int", "return", "void", "while"}
special_symbols = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "<": "LT", "<=": "LE", ">": "GT",
                   ">=": "GE", "==": "EQ", "!=": "NE", "=": "STR", ";": "EOL", ",": "ENUM", 
                   "(": "OP", ")": "CP", "[": "OB", "]": "CB", "{": "OCB", "}": "CCB", "/*": "", "*/": ""}
symbol_label = {"arithmop": {"+", "-", "*", "/"}, "relop": {"<", "<=", ">", ">=", "==", "!="},
                "storeop": {"="}, "endline": {";"}, "enum": {","}, "container": {"(", ")", "[", "]", "{", "}"}}
white_space = {" ","\t","\n"}

f = open("prg1.c-") # configurar para abrir programa correto
program = f.read()

def get_label(token):
    if token in keywords:
        return "keyword"
    if token in special_symbols:
        return "special symbol"
    if token in white_space:
        return "white space"
    if token.isalpha():
        return "id"
    if token.isnumeric():
        return "int"
    return "error"

def get_symbol_label(symbol):
    for k in symbol_label.keys():
        if symbol in symbol_label[k]:
            return k
    return ""

def get_list_of_tokens(text):
    token = ""
    tokens = []
    i = 0
    while i < len(text):
        token += text[i]
        if i + 1 < len(text) and (not text[i + 1].isalnum() or not token.isalnum()):
            if text[i] + text[i + 1] in special_symbols:
                i += 1
                continue
            match token:
                case "/*":
                    try:
                        i = text.index("*/", i) + 1
                    except:
                        raise SyntaxError("Erro de sintaxe, comentário foi iniciado mas não fechado.")
                case "*/":
                    raise SyntaxError("Erro de sintaxe, comentário foi fechado mas não iniciado.")
                case _:
                    token_info = (token, get_label(token))
                    tokens.append(token_info)
            token = ""
        i += 1
    token_info = (token, get_label(token))
    tokens.append(token_info)
    return tokens

def lexer(text):
    token_list = get_list_of_tokens(text)
    table = []
    for token in token_list:
        match (token[1]):
            case "white space":
                table.append(tuple(token[0]))
            case "keyword":
                table.append((token[0], token[0]))
            case "id":
                table.append((token[0], "id"))
            case "int":
                table.append((token[0], "number"))
            case "special symbol":
                table.append((token[0], get_symbol_label(token[0]), special_symbols[token[0]]))
            case _:
                table.append((token[0], "ERROR"))
    return table

def main(): # o parser
    tokens = lexer(program)
    for token in tokens:
        print(token)

if __name__ == '__main__':
    main()
f.close()