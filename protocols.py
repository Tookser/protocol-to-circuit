'''конкретные протоколы'''
# Формат return протоколов: либо выдаётся строка '!xI'/'xI',
# по которой идёт различие, либо выдаётся строка 'yI'.

from tools import xs_to_y, x_num_to_y


def final_sign(num):
    '''с отрицанием или без'''
    return '!' if num == '1' else ''

def invert_final_sign(sign):
    '''заменяет знак на противоположный'''
    return '' if sign == '!' else '!'


def a1(x):
    '''только x'''
    my_x = x[0]
    yield x[0]

    my_y = yield

    if my_x == my_y:
        return 'y'+my_x
    else:
        return final_sign(my_x) + 'x0'
    # print('me is p0', my_x, my_y)


def b1(y):
    my_x = yield

    my_y = y[0]
    yield my_y

    if my_x == my_y:
        return 'y'+my_x
    else:
        return final_sign(my_x) + 'x0'


def a2(x):
    '''параметр x - его слово'''
    my_x = x.copy()
    yield str(my_x[0])

    my_y = [-1, -1]
    my_y[0] = (yield)[0]

    yield str(my_x[1])
    my_y[1] = (yield)[0]

    if my_x == my_y:
        return 'y' + ''.join(map(str, my_x))
    else:
        if my_x[0] != my_y[0]:
            symbol = final_sign(my_x[0])
            return symbol + "x0"
        else:
            symbol = final_sign(my_x[1])
            return symbol + "x1"

def b2(y):
    '''параметр y - его слово'''
    my_x = [-1, -1]

    my_x[0] = (yield)[0]

    my_y = y.copy()
    yield str(my_y[0])

    my_x[1] = (yield)[0]
    yield str(my_y[1])


    if my_x == my_y:
        return 'y' + ''.join(map(str, my_x))
    else:
        if my_x[0] != my_y[0]:
            symbol = final_sign(my_x[0])
            return symbol + "x0"
        else:
            symbol = final_sign(my_x[1])
            return symbol + "x1"



def a3(x):
    '''параметр x - его слово'''
    my_x = x.copy()
    yield str(my_x[0])

    my_y = [-1, -1, -1]
    my_y[0] = (yield)[0]

    yield str(my_x[1])
    my_y[1] = (yield)[0]

    yield str(my_x[2])
    my_y[2] = (yield)[0]

    if my_x == my_y:
        return 'y' + ''.join(map(str, my_x))
    else:
        if my_x[0] != my_y[0]:
            sign = my_x[0]
            return final_sign(sign) + "x0"
        elif my_x[1] != my_y[1]:
            sign = my_x[1]
            return final_sign(sign) + "x1"
        else:
            sign = my_x[2]
            return final_sign(sign) + "x2"

def b3(y):
    '''параметр y - его слово'''
    my_x = [-1, -1, -1]

    my_x[0] = (yield)[0]

    my_y = y.copy()
    yield str(my_y[0])

    my_x[1] = (yield)[0]
    yield str(my_y[1])

    my_x[2] = (yield)[0]
    yield str(my_y[2])

    if my_x == my_y:
        return 'y' + ''.join(map(str, my_x))
    else:
        if my_x[0] != my_y[0]:
            sign = my_x[0]
            return final_sign(sign) + "x0"
        elif my_x[1] != my_y[1]:
            sign = my_x[1]
            return final_sign(sign) + "x1"
        else:
            sign = my_x[2]
            return final_sign(sign) + "x2"


def a2_no_alter(x):
    '''посылает сразу всё'''
    my_x = x.copy()
    yield ''.join(my_x)

    my_y = [-1, -1]
    smt = yield
    my_y = list(smt)

    if my_x == my_y:
        return 'y' + ''.join(map(str, my_x))
    else:
        if my_x[0] != my_y[0]:
            symbol = final_sign(my_x[0])
            return symbol + "x0"
        else:
            symbol = final_sign(my_x[1])
            return symbol + "x1"

def b2_no_alter(y):
    '''параметр y - его слово'''
    my_x = [-1, -1]
    smt = yield
    my_x = list(smt)

    my_y = y.copy()
    yield ''.join(my_y)


    if my_x == my_y:
        return 'y' + ''.join(map(str, my_x))
    else:
        if my_x[0] != my_y[0]:
            symbol = final_sign(my_x[0])
            return symbol + "x0"
        else:
            symbol = final_sign(my_x[1])
            return symbol + "x1"


def last1(dct):
    '''возвращает положение последней единицы'''
    for key in reversed(dct.keys()):
        if dct[key] == '1':
            return key
        elif dct[key] == '0':
            pass
        else:
            raise Exception("Другие элементы в словаре кроме '0' и '1'.")
    else:
        raise Exception("Значения словаря - только '0'")


def simple_star_n_a(x):
    '''протокол SIMPLE* для произвольного n'''

    # делаем протокол протоколом для с.ун.отн.
    # ценой увеличения длины на 1
    x = x + ['0']

    n = len(x)

    a = {}
    b = {}
    lock_A = False

    a[0] = x[0]
    yield a[0]

    lock_A_sended_flag = False
    for i in range(1, n-1, 2):  # учитываем индексацию с 0
        b[i] = yield

        if lock_A:
            a[i+1] = '0'
        else:
            if b[i] == x[i]:
                a[i+1] = x[i+1]
            else:
                lock_A = True
                a[i+1] = '1'

        if n % 2 != 0 and i == n - 2:
            lock_A_str = '1' if lock_A else '0'
            yield a[i+1], lock_A_str
            lock_A_sended_flag = True
        else:
            yield a[i+1]


    if n % 2 == 0:
        b[n-1] = yield

    lock_A_str = '1' if lock_A else '0'
    if not lock_A_sended_flag:
        yield lock_A_str
    lock_B_str = yield

    lock_B = True if lock_B_str == '1' else False

    i_A = (last1(a) - 1) if lock_A else n - 1
    i_B = (last1(b) - 1) if lock_B else n - 1

    result = min(i_A, i_B)

    if result == n - 1:
        return x_num_to_y(x[:-1])
    else:
        return final_sign(x[result]) + 'x' + str(result)



def simple_star_n_b(y):
    '''протокол SIMPLE* для произвольного n'''
    y = y + ['1']  # см. для a
    n = len(y)

    a = {}
    b = {}
    lock_B = False

    for i in range(0, n-1, 2):  # учитываем индексацию с 0
        a[i] = yield

        if lock_B:
            b[i+1] = '0'
        else:
            if a[i] == y[i]:
                b[i+1] = y[i+1]
            else:
                lock_B = True
                b[i+1] = '1'

        yield b[i+1]

    if n % 2 == 1:
        a[n-1], lock_A_str = yield
    else:
        lock_A_str = yield

    lock_B_str = '1' if lock_B else '0'

    yield lock_B_str

    lock_A = True if lock_A_str == '1' else False

    i_A = (last1(a) - 1) if lock_A else n - 1
    i_B = (last1(b) - 1) if lock_B else n - 1

    result = min(i_A, i_B)

    if result == n - 1:
        return x_num_to_y(y[:-1])
    else:
        return invert_final_sign(final_sign(y[result])) + 'x' + str(result)


protocol_to_arr = {}
protocol_to_arr[a1] = protocol_to_arr[b1] = 1
protocol_to_arr[a2] = protocol_to_arr[b2] = 2
protocol_to_arr[a3] = protocol_to_arr[b3] = 3
protocol_to_arr[a2_no_alter] = protocol_to_arr[b2_no_alter] = 2
protocol_to_arr[simple_star_n_a] = protocol_to_arr[simple_star_n_b] = None
