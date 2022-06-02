# Программа из выпускной квалификационной работы Ивана Белашкина (2022)

## Описание возможностей

Данная программа позволяет построить по протоколу строгого универсального отношения длины k мультиплексорную функцию такой же (или меньшей) глубины методом, описанным в [1] и [2]. К программе приложены некоторые протоколы, в том числе из описанных в [1], в частности SIMPLE\*.

## Установка

Требуется Python 3 и установка всех зависимостей из requirements.txt. Например, так:

Linux:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

После этого программу можно запустить.

## Интерфейс

Для построения протокола и визуализации дерева требуется ввести 

`./create_tree [ИМЯ ПРОТОКОЛА]`

`[ИМЯ ПРОТОКОЛА]` может равняться `1`, `2`, `3` (наиболее наивные протоколы - передача всех бит обоими игроками по очереди, с размерностями `1`, `2`, `3`), `na2` (то же, для размерности 2, но без альтернирования), и `simple` (протокол `SIMPLE*` с заданной по умолчанию размерностью `4`).

При запуске программы без имени протокола будет использовано имя протокола по умолчанию (`1`).

Для протокола `SIMPLE*` можно запустить программу ещё и таким образом:

`./create_tree simple [ЧИСЛО АДРЕСНЫХ ПЕРЕМЕННЫХ]`

Программа выводит дерево СФЭ (в терминале представлении ASCII) и упрощённое дерево СФЭ (в котором убраны СФЭ с одним сыном). А также формулу, получаемую по дереву и некоторые её характеристики.

Также формула записывается в файл `output_formula.txt` и дерево формулы в формате `.dot` `output_formula.dot` (что позволяет отобразить его наглядно; впрочем, обеспечить его бинарность пока не удалось). Упрощённая формула и её дерево записываются в файлы `output_simplified_formula.txt` и `output_simplified_formula.dot`.

## Реализация протоколов

Протоколы реализованы как функции-генераторы. Через next и send реализован обмен информацией между ними. Это может вызвать проблемы с производительностью (в частности, программа, по-видимому, может не очень быстро работать при $n$ начиная с 8), однако повышает лёгкость написания протоколов.

## Программные зависимости

Библиотека anytree - для построения дерева и его визуализации в терминале. Sympy - для построения формулы по дереву. Pytest - для комфортного запуска тестов.

## Тестирование

Команда

`pytest .` 

запускает тесты на вспомогательные функции и на корректность построенных СФЭ. 

## Ссылки на литературу 

[1] _G. Tardos and U. Zwick_, "The communication complexity of the universal relation," _Proceedings of Computational Complexity. Twelfth Annual IEEE Conference, 1997, pp. 247-259._ https://doi.org/10.1109/CCC.1997.612320

[2] _Karchmer, M., Raz, R. & Wigderson, A._ Super-logarithmic depth lower bounds via the direct sum in communication complexity. _Comput Complexity 5, 191–204 (1995)._ https://doi.org/10.1007/BF01206317
