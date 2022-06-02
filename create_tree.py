#!/usr/bin/env python3
'''Версия построителя протокола с созданием нод'''

from sys import argv, exit
import re
import pickle
import argparse

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


def create_tree(transcripts, player_0, player_1):
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

    return root


def simplify_tree(root, parent=None, was_two=False):
    '''упрощает дерево функции, убирая вершины с одним потомком
    was_two - было ли на пути к данному root сверху хоть одно разветвление на 2'''
    if root is None:
        return None

    if len(root.children) == 2:
        if (root.children[0].name != '' and
            root.children[1].name != ''):
            # если реальное разветвление
            new_root = Node(root.name, parent=parent)

            simplify_tree(root.children[0], parent=new_root)
            simplify_tree(root.children[1], parent=new_root)
            return new_root
        else:
            # только один потомок по факту
            if root.children[0].name != '':
                return simplify_tree(root.children[0], parent=parent)
            elif root.children[1].name != '':
                return simplify_tree(root.children[1], parent=parent)
            else:
                raise Exception()

    elif len(root.children) == 0:
        return Node(root.name, parent=parent)

    else:
        raise Exception()


def get_formula_main(n, player_0, player_1, get_tree=False):
    '''основная функция, возвращает (опционально дерево), формулу и символы'''
    tree = create_tree(get_transcripts_from_protocol(n, player_0, player_1), player_0, player_1)

    formula, symbols = fc.tree_to_formula(n, tree)

    if get_tree:
        simplified_tree = simplify_tree(tree)
        formula_from_simplified, symbols_from_simplified = fc.tree_to_formula(n, simplified_tree)
        return tree, simplified_tree, formula, formula_from_simplified, symbols, symbols_from_simplified
    else:
        return formula, symbols

def get_tree_and_formula(*args, **kwargs):
    '''то же что и get_formula_main, но с деревом'''
    return get_formula_main(*args, **kwargs, get_tree=True)

old_print = print

def print(*args):
    for el in args:
        old_print(el, end=' ')
        old_print('')
    with open('log.txt', 'a') as log:
        for el in args:
            log.write(str(el) + ' ')
        log.write('\n')

def main():
    with open('log.txt', 'w') as log:  # создание файла
        log.write('')

    parser = argparse.ArgumentParser(description='Выбор протокола')

    parser.add_argument('type', nargs='?', default='1')
    parser.add_argument('n', nargs='?', default=4)

    args = parser.parse_args()

    arg = args.type
    n = int(args.n)

    # if len(argv) == 1:
    #     arg = '1'
    # else:
    #     arg = argv[1]

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
        print('Первым аргументом должно быть название протокола из списка: 1, 2, 3, na2, simple')
        exit()


    if arg != 'simple':
        n = protocol_to_arr[player_0]

    tree, simplified_tree, formula, formula_from_simplified, symbols, symbols_from_simplified = get_tree_and_formula(n, player_0, player_1)

    print('Исходное дерево:')
    render_tree(tree)

    print('Упрощённое дерево:')
    render_tree(simplified_tree)

    print('Формула:')
    print(formula)

    if (verify_formula(formula, symbols) and
        verify_formula(formula_from_simplified, symbols_from_simplified)): # тут
        print('Проверка формул завершена, формула корректна.')

        print(f'n = {n}')

        depth_of_tree = get_depth_tree(tree)
        print(f'Глубина исходного дерева: {depth_of_tree}')

        elements_of_tree = get_elements_tree(tree)
        print(f'Элементов в исходном дереве: {elements_of_tree}')

        depth_of_tree = get_depth_tree(simplified_tree)
        print(f'Глубина упрощённого дерева: {depth_of_tree}')

        elements_of_tree = get_elements_tree(simplified_tree)
        print(f'Элементов в упрощённом дереве: {elements_of_tree}')

        depth_of_formula = get_depth_formula(formula)
        print(f'Глубина формулы (не обязательно с унарно-бинарным деревом): {depth_of_formula}')

        depth_of_formula = get_depth_formula(formula_from_simplified)
        print(f'Глубина формулы из упрощённого дерева (не обязательно с унарно-бинарным деревом): {depth_of_formula}')

        print('Запись формулы в файл...')
        with open('output_formula.txt', 'w') as formula_file:
            formula_file.write(str(formula))
        print('...завершена.')

        print('Запись упрощённой формулы в файл...')
        with open('output_simplified_formula.txt', 'w') as formula_file:
            formula_file.write(str(formula_from_simplified))
        print('...завершена.')

        print('Запись дерева формулы в файл...')
        with open('output_formula.dot', 'w') as dot_file:
            dot_file.write(dotprint(formula))
        print('...завершена.')

        print('Запись дерева упрощённой формулы в файл...')
        with open('output_simplified_formula.dot', 'w') as dot_file:
            dot_file.write(dotprint(formula_from_simplified))
        print('...завершена.')
    else:
        print('Ошибка: построенная по дереву формула некорректна.')


if __name__ == '__main__':
    main()
