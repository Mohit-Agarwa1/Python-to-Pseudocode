def splitCount(s, count):
    return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]


def decompress(string):
    string = string.split('\n')
    print(string)
    pl = []
    for i in string:
        pl.append(splitCount(i,3))

    output =''
    for i in pl:
        for m in i:
            print(m)
            output = output + (m[2]*int(m[0:2]))
        output = output + '\n'
    print(output)


if __name__ == '__main__':
    decompress('08n05q\n01236f')

