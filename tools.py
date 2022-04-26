import re
import copy

from sympy import dotprint, Not

def iter_over_xs(xs):
    '''перебирате все x-ы
    возвращает пару (значения x-ов, номер y)
    x-ы должны быть упорядочены (и порядок их сохраняется - в питонах с 3.7'''

    dct = {}
    for x in xs:
        dct[x] = 0
    dct[xs[0]] = -1

    while True:
        # TODO переписать на численное
        # увеличиваем число на 1
        for x in xs:
            if dct[x] <= 0:
                dct[x] += 1
                break
            else:
                dct[x] = 0
        else:
            break

        yield copy.copy(dct)


def x_num_to_y(x):
    '''переводит список значений x-ов в название переменной y'''
    return 'y' + ''.join(map(str, x))


def xs_to_y(symbols, x_values):
    '''по xs выдаёт номер y'''
    return symbols[x_num_to_y(x_values.values())]


def verify_formula(formula, symbols):
    '''проверяет формулу на корректность, перебирая все значения.'''
    xs = []  # переменные иксы

    for var_name, value in symbols.items():
        if var_name[0] == 'x':
            xs.append(var_name)


    for x_values in iter_over_xs(xs):
        if formula.subs(x_values) != xs_to_y(symbols, x_values):
            return False
    else:
        return True


def iter_over_bits(n=2):
    '''перебирает все значения из n бит'''
    arr = [0] * n
    arr[0] = -1
    while True:
        # TODO переписать на численное
        # увеличиваем число на 1
        for i in range(n):
            if arr[i] <= 0:
                arr[i] += 1
                break
            else:
                arr[i] = 0
        else:
            break

        yield list(map(str, arr))


def is_var(value):
    '''определяет, переменная это или функция'''
    # TODO уточнить регексп
    return value not in ['^', 'V', ''] and re.match(r'!?(x\d+|y[01]+)', value)


def get_depth_formula(expr):
    '''определяет глубину выражения sympy
    (учитывая в т.ч. переменные и отрицания как 1)
    expr - выражение sympy'''

    something_flag = False  # флаг показывает, есть ли что-то в потомках

    d = []

    for arg in expr.args:
        d.append(get_depth_formula(arg))
        something_flag = True

    if something_flag:
        if expr.func == Not:
            return max(d)
        else:
            return max(d) + 1
    else:
        return 0


def get_depth_tree(root):
    '''определяет глубину дерева без оптимизаций вершин с 1 потомком'''
    if root.name == '':
        return 0
    else:
        if len(root.children) == 0:
            return 0
        elif len(root.children) == 1:
            return 1 + get_depth_tree(root.children[0])
        elif len(root.children) == 2:
            return 1 + max(get_depth_tree(root.children[0]),
                           get_depth_tree(root.children[1]))
        else:
            raise Exception('Should be from 0 to 2 childrens')
