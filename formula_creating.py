'''модуль, содержащий функции, используемые для создания формулы по дереву'''

import copy

from sympy import symbols, true, false, And, Or, UnevaluatedExpr
from sympy import dotprint


from tools import *

def create_symbols(n):
    '''создаёт все необходимые символы.'''
    result = {}

    names = []

    for i in range(n):
        names.append(f'x{i}')

    for lst in iter_over_bits(n):
        names.append('y' + ''.join(lst))

    for nm in names:
        result[nm] = symbols(nm)

    assert len(result) == 2**n + n
    return result


def get_formula(node, symbs):
    '''выдаёт формулу по корневой вершине поддерева: рекурсия'''

    if is_var(node.name):
        if node.name[0] == '!':
            return ~ (symbs[node.name[1:]])
        else:
            return symbs[node.name]

    elif node.name == '^':
        assert node.children[0].name != '' or node.children[1].name != ''

        if node.children[0].name == '':
            f0 = true  # переменная из sympy
        else:
            f0 = get_formula(node.children[0], symbs)

        if node.children[1].name == '':
            f1 = true
        else:
            f1 = get_formula(node.children[1], symbs)

        return f0 & f1

    elif node.name == 'V':
        assert node.children[0].name != '' or node.children[1].name != ''

        if node.children[0].name == '':
            f0 = false
        else:
            f0 = get_formula(node.children[0], symbs)

        if node.children[1].name == '':
            f1 = false
        else:
            f1 = get_formula(node.children[1], symbs)

        return f0 | f1

    else:
        raise Exception('Почему-то что-то не то встретилось при разборе дерева')

def tree_to_formula(n, tree_root):
    '''обёртка над get_formula, нужна, чтобы создать символы'''
    symbs = create_symbols(n)
    return get_formula(tree_root, symbs), symbs

