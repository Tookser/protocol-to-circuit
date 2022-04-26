import pytest

from create_tree import get_transcripts_from_protocol, iter_over_bits
from protocols import a2, b2


def test_2_basic_protocol_to_transcript():
    n = 2
    transcripts = get_transcripts_from_protocol(n, a2, b2)

    assert len(transcripts) == (2 ** 2) ** 2
    # все возможные пары наборов по 2 бита

    transcripts_iter = iter(transcripts)

    for x in iter_over_bits(2):
        for y in iter_over_bits(2):
            _, var1, var2 = next(transcripts_iter)  # не проверяем
            if x == y:
                assert var1 == var2 == f'y{"".join(map(str, x))}'
            else:
                assert var1 == var2

                if var1[0] == '!':  # с отрицанием
                    # TODO знаки!
                    assert var1[1] == 'x'
                    i = int(var1[2:])

                    assert x[i] == '1'
                    assert y[i] == '0'
                else:  # без отрицания
                    assert var1[0] == 'x'
                    i = int(var1[1:])

                    assert x[i] == '0'
                    assert y[i] == '1'


