import pytest

import create_tree
from formula_creating import iter_over_xs, verify_formula
from protocols import *
from tools import *

def test_iter_xs():
    '''тестирует присваивание всех значений переменным по очереди'''
    result = list(iter_over_xs(['x0', 'x1']))


    x1, x2 = 'x0', 'x1'  # для удобства
    assert len(result) == 2 ** 2
    assert result == [{x1:0, x2:0},
                        {x1:1, x2:0},
                        {x1:0, x2:1},
                         {x1:1, x2:1}]


def test_simple_protocols():
    '''верифицирует простые протоколы'''
    for arg in ['1', '2', '3', 'na2']:
        if arg == '1':
            player_0, player_1 = a1, b1
        elif arg == '2':
            player_0, player_1 = a2, b2
        elif arg == '3':
            player_0, player_1 = a3, b3
        elif arg == 'na2':
            player_0, player_1 = a2_no_alter, b2_no_alter
        else:
            print('Only 1, 2, 3, na2 for protocols a/b1, a/b2, a/b3, a/b2_no_alter')
            raise NotImplementedError

        n = protocol_to_arr[player_0]

        formula, symbols = create_tree.get_formula_main(n, player_0, player_1)

        assert verify_formula(formula, symbols)


def test_simple_n():
    '''верифицирует протокол simple* для разных n'''
    for n in range(1, 6+1):
        formula, symbols = create_tree.get_formula_main(n, simple_star_n_a, simple_star_n_b)

        assert verify_formula(formula, symbols)


# долго работает, поэтому скипнут
@pytest.mark.skip
def test_big_n_simple():
    for i in [7]:
        n = i

        formula, symbols = create_tree.get_formula_main(n, simple_star_n_a, simple_star_n_b)

        assert verify_formula(formula, symbols)


def test_depth():
    '''проверяет глубины протоколов'''
    for pl_a, pl_b, real_depth in [(a1, b1, 2),
                                   (a2, b2, 4),
                                   (a2_no_alter, b2_no_alter, 4),
                                   (a3, b3, 6)]:
        tree, formula, _ = create_tree.get_tree_and_formula(protocol_to_arr[pl_a],
                                                      pl_a, pl_b)

        # get_depth_formula закомментировано, т.к. элементы в формуле sympy могут иметь фактически больше 2 входов (a | b | c реализуется одним элементом)
        assert get_depth_tree(tree) == real_depth  # == get_depth_formula(formula)

    for n in range(1, 6+1):
        tree, _, _ = create_tree.get_tree_and_formula(n,
                                                      simple_star_n_a,
                                                      simple_star_n_b)

        assert get_depth_tree(tree) == n + 3
