from Tokens import Tokens
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter


global content_index
global content
content_index = 0

global root
global nodetpm
global data

def peek():
    global content
    global content_index
    return content[content_index]

def advance():
    global content_index
    val = peek()
    content_index = content_index + 1
    return val

def eof():
    global content
    global content_index
    return content_index >= len(content)

# ====================== Scanner ======================

def scanner():
    ans = {}
    while not eof() and (peek() == ' ' or peek() == '\n'):
        advance()
    if eof():
        ans['type'] = '$'
    else:
        if peek() in '0123456789':
            ans = scan_digits()
        else:
            ch = advance()
            if ch in 'abcdeghjklmnoqrstuvwxyz':
                ans['type'] = 'id'
                ans['val'] = ch
            elif ch == 'f':
                ans['type'] = 'floatdcl'
            elif ch == 'i':
                ans['type'] = 'intdcl'
            elif ch == 'p':
                ans['type'] = 'print'
            elif ch == '=':
                ans['type'] = 'assign'
            elif ch == '+':
                ans['type'] = 'plus'
            elif ch == '-':
                ans['type'] = 'minus'
            else:
                print('Error Lexico')
                exit()
    return ans

def scan_digits():
    ans = {
        'val': ''
    }

    while peek() in '0123456789':
        ans['val'] = ans['val'] + advance()
    if peek() != '.':
        ans['type'] = 'inum'
    else:
        ans['type'] = 'fnum'
        ans['val'] = ans['val'] + advance()
        while peek() in '0123456789':
            ans['val'] = ans['val'] + advance()
    return ans


# ====================== Parser code ======================

def prog(tokens):
    global root
    root = Node("Program")
    dcls(tokens)
    stmts(tokens)
    # Imprimimos el árbol
    print("=====================")
    print("Imprimiendo árbol")
    print("=====================")
    print(RenderTree(root, style=AsciiStyle()).by_attr())
    # Imprimimos el código de 3 direcciones
    print("=====================")
    print("Generando archivo 3 direcciones...")
    print("=====================")
    threeAdddressCode(root)
    print("¡Archivo creado!")


def dcls(tokens):
    if tokens.peek()['type'] == 'intdcl' or tokens.peek()['type']  == 'floatdcl':
        dcl(tokens)
        dcls(tokens)

def dcl(tokens):
    #print(tokens.peek()) #type
    cadena = tokens.peek()["type"]
    tokens.next()
    #print(tokens.peek()) #id - val
    cadena2 = tokens.peek()["val"]
    tokens.next()
    result = f'{cadena} {cadena2}'
    #agregamos al root
    childdlc = Node(result, parent=root)

def stmts(tokens):
    if tokens.peek()['type'] == 'id' or tokens.peek()['type'] == 'print':
        stmt(tokens)
        stmts(tokens)
    else:
        if tokens.peek()['type'] == '$':
            pass
        else:
            print('Error stmsts')
            exit()

def stmt(tokens):

    if tokens.peek()['type'] == 'id':
        node = tokens.peek()['type'] + " " + tokens.peek()['val']
        node2 = node
        tokens.next()
        if tokens.peek()['type'] == 'assign':
            parent = Node(tokens.peek()['type'], parent=root)
            child = Node(node2, parent=parent)
            tokens.next()

            val(tokens, parent)
            expr(tokens, parent)

    else:
        if tokens.peek()['type'] == 'print':
            name = tokens.peek()['type']
            tokens.next()
            tprint = Node(name + " " + tokens.peek()['val'], parent=root)
        else:
            print('Error stmsts')
            exit()


def expr(tokens, child):
    global nodetpm

    if tokens.peek()['type'] == 'plus' or tokens.peek()['type'] == 'minus':
        parent = Node(tokens.peek()['type'], parent=child)
        #print(tokens.peek())
        tokens.next()
        childdlc = Node(nodetpm, parent=parent)
        val(tokens, parent)
        expr(tokens, parent)
    else:
        pass
    #    print('Error expr token')


def val(tokens, child):
    global data
    global nodetpm
    if tokens.peek()['type'] == 'id' or tokens.peek()['type'] == 'inum' or tokens.peek()['type'] == 'fnum':
        data = tokens.peek()["type"] + " " +tokens.peek()["val"]
        #print(tokens.peek())
        tokens.next()
        if tokens.peek()['type'] == 'plus' or tokens.peek()['type'] == 'minus':
            nodetpm = data
        else:
            childdlc = Node(data, parent=child)
    else:
        exit()
    #    print('Error val token')


# ====================== Código de 3 direcciones ======================

def threeAdddressCode(root):

    tokens = [node.name for node in PreOrderIter(root)]
    dclssChilds = []
    stmtsChilds = []
    for node in tokens:
        if node=='Program' or node.startswith('intdcl') or node.startswith('floatdcl'):
            dclssChilds.append(node)
        else:
            stmtsChilds.append(node)

    #print(dclssChilds)
    #print(stmtsChilds)


    # ['assign', 'id a', 'inum 5', 'assign', 'id c', 'inum 2', 'assign', 'id b', 'plus', 'id a', 'plus', 'inum 3', 'id c', 'print b']

    # ['id a', 'assign', 'inum 5']
    # ['id c', 'assign', 'inum 2']
    # ['id b', 'assign', 'id a ', 'plus', 'inum 3', 'plus', 'id c']
    # ['print b']
    i = 0
    while i < len(stmtsChilds):

        if stmtsChilds[i] == 'assign' or stmtsChilds[i] == 'plus' or stmtsChilds[i] == 'minus':
            tmp = stmtsChilds[i]
            stmtsChilds[i] = stmtsChilds[i+1]
            stmtsChilds[i+1] = tmp
            i+=1
        i+=1

    sentence = ""
    tac= ""
    tac2 = ""
    count = 0
    var_tmp = 0
    operator = ""
    flag = 0
    while len(stmtsChilds)>0:

        stmt = stmtsChilds.pop()

        if stmt.startswith('print'):
            tmpdata = stmt.lstrip("print")
            sentence = 'p' +" "+ tmpdata
            tac2 = tac2 + sentence+'\n'
            sentence = ""

        if count >= 2:
            flag = 1
            if stmt != 'assign':
                stmtsChilds.append(stmt)
                sentence = 'x'+str(var_tmp)+ " = " + sentence
                if flag == 1:
                    tac = tac +'\n' + sentence
                else:
                    tac = sentence +'\n' + tac

                if operator == 'plus':
                    sentence = " + " + 'x'+str(var_tmp)
                if operator == 'minus':
                    sentence = " - " + 'x'+str(var_tmp)
                count = 1

                var_tmp = var_tmp +1
                continue

            else:
                count = 0

        if stmt.startswith('inum') or stmt.startswith('fnum') or stmt.startswith('id'):
            if stmt.startswith('inum'):
                tmpdata = stmt.lstrip("inum")
                sentence = tmpdata + ' ' + sentence
            elif stmt.startswith('fnum'):
                tmpdata = stmt.lstrip("fnum")
                sentence = tmpdata + ' ' + sentence
            elif stmt.startswith('id'):
                tmpdata = stmt.lstrip("id")
                sentence = tmpdata + ' ' + sentence

        if stmt == "assign":
            stmt = stmtsChilds.pop()

            if flag == 1:
                if stmt.startswith('id'):
                    tmpdata = stmt.lstrip("id")
                    sentence = tmpdata + " = " + sentence
                    tac = tac +'\n' + sentence
                    sentence = ""
                    flag = 0
            else:
                if stmt.startswith('id'):
                    tmpdata = stmt.lstrip("id")
                    sentence = tmpdata + " = " + sentence
                    tac = sentence +'\n' + tac
                    sentence = ""

        if stmt == 'plus':
            operator = 'plus'
            count+=1
            if count!=2:
                sentence =  ' + ' + sentence

        if stmt == 'minus':
            operator = 'minus'
            count+=1
            if count!=2:
                sentence =  ' - ' + sentence


    dcllist = ""
    i = 0
    for i in range(0, len(dclssChilds)):
        if dclssChilds[i] == "Program":
            pass
        else:
            if dclssChilds[i].startswith("intdcl"):
                tmpdata = dclssChilds[i].lstrip("intdcl")
                dcllist += "i" + tmpdata + '\n'
            if dclssChilds[i].startswith("floatdcl"):
                tmpdata = dclssChilds[i].lstrip("floatdcl")
                dcllist += "f" + tmpdata + '\n'


    with open('tac.txt', 'w') as f:
        f.write(dcllist + tac+ '\n' + tac2)





# ====================== Archivo ======================

with open('input.txt') as f:
    content = f.read()

tokens = Tokens()
while not eof():
    tokens.append(scanner())
tokens.append(scanner())

prog(tokens)
