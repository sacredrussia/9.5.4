text = 'сын Кадыров получил награду'

cen = ['кадыров', 'Медведев'
       ]
x = ''


def censor(value):
    i = list(value.split())
    global x
    for c in i:
        if c in cen or c.lower() in cen:
            x = x + c[0] + ('*' * (len(c) - 1)) + ' '
        else:
            x = x + c + ' '
    return print(x)


censor('сын Кадыров получил награду')

