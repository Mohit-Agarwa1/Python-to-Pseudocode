import tokenize


def log(i):
    pass


def py_to_ps():
    global indent
    indent = 0
    global thenner
    thenner = True
    global iffer
    iffer = []
    global subroutine
    subroutine = []
    global forloop
    forloop = []
    global whiler
    whiler = []
    with open('code.py', 'rb') as f:
        q = tokenize.tokenize(f.readline)
        ps = ''
        count = 0

        list_lex = []

        for i in q:
            list_lex.append({'type': i.type, 'string': i.string, 'line': i.start[0], 'full_line': i.line})
            print(i)

        while count != len(list_lex):

            i = list_lex[count]

            line = []
            for pyt in list_lex:
                if i['line'] == pyt['line']:
                    line.append(pyt['string'])
            log(i)

            for qut in subroutine:
                if qut[0] == indent:
                    if qut[1] != i['line'] and qut[1] + 1 != i['line']:
                        ps += '\n'

                        ps += 'ENDSUBROUTINE\n'

                        subroutine.remove(qut)

            if i['type'] == 53:
                if i['string'] == '=':
                    ps += ' ← '
                    log('deqfound')
                elif i['string'] == '==':
                    ps += '== '
                elif i['string'] == ':':
                    if thenner != False:
                        ps += ' THEN '
                    thenner = True
                elif i['string'] == '%':
                    ps += ' MOD '
                elif i['string'] == '//':
                    ps += ' DIV '
                else:
                    ps += i['string'] + ' '
            elif i['type'] == 57:
                ps += i['string']
                ps += '\n'
            elif i['type'] in [3]:
                ps += i['string']

            elif i['type'] == 5:
                ps += '    '
                indent += 1
                log('indent')
            elif i['type'] == 1:
                if i['string'] == 'print':
                    ps += 'OUTPUT '
                    count += 2
                    fl = list_lex[count]

                    ps += fl['string']
                    count += 1
                elif i['string'] == 'input':
                    ps += 'USERINPUT '
                    count += 2
                    fl = list_lex[count]

                    ps += fl['string']
                    count += 1
                elif i['string'] == 'and':
                    ps += ' AND '
                elif i['string'] == 'or':
                    ps += ' OR '
                elif i['string'] == 'not':
                    ps += ' NOT '
                elif i['string'] == 'if':
                    ps += 'IF '
                    iffer.append(indent)
                elif i['string'] == 'while':
                    ps += 'WHILE  '
                    whiler.append(indent)
                    thenner = False
                elif i['string'] == 'append' or 'remove':

                    q = i['string']
                    ps += q

                elif i['string'] == 'elif':
                    ps += 'ELSE IF '
                elif i['string'] == 'else':
                    ps += 'ELSE '
                    count += 1
                elif i == 'len':
                    ps += 'LEN'
                elif i['string'] == 'for' and 'range' in i['full_line']:
                    ps += 'FOR '
                    count += 1
                    ps += list_lex[count]['string']
                    count += 1
                    ps += ' <-- '
                    thenner = False
                    count += 3
                    ps += list_lex[count]['string']
                    count += 1
                    ps += ' TO '
                    count += 1
                    ps += list_lex[count]['string']
                    count += 1
                    forloop.append(indent)
                elif i['string'] == 'for' and 'in' in i['full_line']:
                    print('INVALID FOR TYPE: must be in form with range function or use different loop')
                    ps += 'FOR '
                    count += 1
                    ps += list_lex[count]['string']
                    ps += ' IN '
                    count += 1
                    thenner = False
                    forloop.append(indent)


                elif i['string'] == 'def':
                    ps += 'SUBROUTINE\n'
                    thenner = False

                    subroutine.append([indent, i['line']])

                else:
                    ps += i['string']
            elif i['type'] == 4:
                ps += '\n'
                ps += '    ' * indent
                log('newlinefound')

            elif i['type'] == 6:
                indent -= 1
                ps += '\b\b\b\b'
                if len(iffer) > 0:
                    for tfi in iffer:
                        if indent == tfi:
                            if 'elif' not in i['full_line'] and 'else' not in i['full_line']:
                                iffer.remove(tfi)
                                print(tfi, i['full_line'])
                                ps += '\n'
                                ps += '    ' * tfi
                                ps += 'ENDIF\n'
                                ps += '    ' * tfi

                for tfi in forloop:
                    if indent == tfi:
                        forloop.remove(tfi)
                        ps += '\n'
                        ps += '    ' * tfi
                        ps += 'ENDFOR\n'
                        ps += '    ' * tfi
                for tfi in whiler:
                    if indent == tfi:
                        whiler.remove(tfi)
                        ps += '\n'
                        ps += '    ' * tfi
                        ps += 'ENDWHILE\n'
                        ps += '    ' * tfi


            elif i['type'] == 2:
                ps += i['string']
                ps += ' '

            count += 1

        print(ps)
        with open('code.txt', 'w') as file:
            file.write(ps)


py_to_ps()
