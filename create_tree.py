#!/usr/bin/env python3
'''Версия построителя протокола с созданием нод'''

from sys import argv
import re
import pickle

from anytree import Node, RenderTree
from sympy import symbols, simplify, Symbol

import formula_creating as fc
from protocols import *
from tools import *

def function_by_player(player, player_0, player_1):
    ''' возвращает функцию по игроку'''
    if player is player_1:
        return 'V'
    elif player is player_0:
        return '^'
    else:
        raise Exception('Неизвестный игрок, невозможно вернуть символ')


def create_function_node(this_player, parent, player_0, player_1):
    return Node(function_by_player(this_player, player_0, player_1),
                parent=parent)




def assert_none(value):
    if value is not None:
        raise AssertionError('Ошибка: одновременная посылка сообщений!')



def get_message_from_setting(x, y, player_0, player_1, n):
    '''получение message по протоколам+наборам
    x, y - наборы
    first_player, second_player - протоколы
    n - длина сообщения
    возвращает message
    '''
    p0 = player_0(x)
    p1 = player_1(y)

    gamer_1 = p0
    gamer_2 = p1

    messages = []

    ## 0 итерация цикла - отличается тем, что первый игрок не получает ничего
    message = next(gamer_1)
    messages.append(message)
    assert_none(next(gamer_2))

    gamer_1, gamer_2 = gamer_2, gamer_1

    while True:
        try:
            message = gamer_1.send(message)
            messages.append(message)
            assert_none(next(gamer_2))  # этот игрок ждёт

            gamer_1, gamer_2 = gamer_2, gamer_1
        except StopIteration as e1:
            try:
                assert_none(next(gamer_2))
            except StopIteration as e2:

                if gamer_1 is not p0:  # порядок ходов
                    e1, e2 = e2, e1


                return (messages, e1.value, e2.value)
                # print('OK: Успешный конец обмена сообщениями')
            else:
                print('Ошибка: обмен не окончен, один игрок закончил свой протокол, а другой нет')
                raise
            # finally:
                # print('strange')
                # break

    # return messages


def get_transcripts_from_protocol(n, player_0, player_1):
    '''получение транскриптов с результатами СФЭ по протоколам'''
    transcripts = []

    for x in iter_over_bits(n):
        for y in iter_over_bits(n):
            # setting - пара протоколов + пара наборов
            transcript = get_message_from_setting(x, y, player_0, player_1, n)
            transcripts.append(transcript)
            # print(f'x={x}', f'y={y}', transcript)

    return transcripts


def render_tree(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


def create_tree(transcripts, player_0, player_1, print_tree=False):
    '''строит дерево по транскриптам и протоколам'''
    root = Node(function_by_player(player_0, *(player_0, player_1)))
    Node('', parent=root)  # заранее создаём дочерние вершины, но пустые
    Node('', parent=root)

    for trscr in transcripts:
        parent = None
        node = root
        current_player, other_player = player_0, player_1

        messages, result, _ = trscr

        last_flag = False  # флаг для контроля что переменные на листьях

        for msg in messages:  # для каждого сообщения
            if last_flag:
                raise Exception
                break
            func = function_by_player(current_player, *(player_0, player_1))

            for c in msg:
                c = int(c)

                if node.name == '':
                    node.name = func
                    # заранее создаём дочерние вершины, но пустые
                    Node('', parent=node)
                    Node('', parent=node)
                elif node.name == func:
                    pass
                elif is_var(node.name):
                    last_flag = True
                else:
                    raise Exception('Что-то не так.')

                parent = node
                node = parent.children[c]

            current_player, other_player = other_player, current_player

        # самый нижний слой - переменные или их отрицания
        node.name = result

    if print_tree:
        render_tree(root)

    return root


def check_var(tree):
    '''проверяет, что все переменные - существующие'''
    raise NotImplementedError


def get_formula_main(n, player_0, player_1,
                     print_tree=False, print_formula=True,
                     get_tree=False):
    '''основная функция, возвращает формулу и символы'''
    tree = create_tree(get_transcripts_from_protocol(n, player_0, player_1), player_0, player_1, print_tree=print_tree)

    formula, symbols = fc.tree_to_formula(n, tree)

    if print_formula:
        print(formula)

    if get_tree:
        return tree, formula, symbols
    else:
        return formula, symbols

def get_tree_and_formula(*args, **kwargs):
    '''то же что и get_formula_main, но с деревом'''
    return get_formula_main(*args, **kwargs, get_tree=True)

def main():
    if len(argv) == 1:
        arg = '1'
    else:
        arg = argv[1]

    if arg == '1':
        player_0, player_1 = a1, b1
    elif arg == '2':
        player_0, player_1 = a2, b2
    elif arg == '3':
        player_0, player_1 = a3, b3
    elif arg == 'na2':
        player_0, player_1 = a2_no_alter, b2_no_alter
    elif arg == 'simple':
        player_0, player_1 = simple_star_n_a, simple_star_n_b  # для них задаётся позднее
    else:
        print('Only 1, 2, 3, na2 for protocols a/b1, a/b2, a/b3, a/b2_no_alter')
        return

    if arg == 'simple':
        if len(argv) > 2:
            n = int(argv[2])  # может быть произвольно для данного протокола
        else:
            n = 4
    else:
        n = protocol_to_arr[player_0]

    tree, formula, symbols = get_tree_and_formula(n, player_0, player_1, print_tree=True)

    if verify_formula(formula, symbols):
        print('formula is OK!')

        depth_of_tree = get_depth_tree(tree)
        print(f'depth of tree: {depth_of_tree}')

        depth_of_formula = get_depth_formula(formula)
        print(f'depth of formula: {depth_of_formula}')

        print('writing formula into the file...')
        with open('output_formula.txt', 'w') as formula_file:
            formula_file.write(str(formula))
        print('Done.')

        print('Writing tree into the file...')
        with open('output_formula.dot', 'w') as dot_file:
            dot_file.write(dotprint(formula))
        print('Done.')
    else:
        print('error, formula incorrect! ;=(')


if __name__ == '__main__':
    main()
