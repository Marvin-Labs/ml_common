from unstructured.documents.elements import Text, ElementMetadata

from ml_common.elements import LinearTextCombination


def test_linear_combination_text_join():
    res = LinearTextCombination([Text('test'), Text('test2')])
    assert res.text == 'test test2'
    assert res.metadata.section is None


def test_linear_combination_metadata_join():
    for i in range(1, 4):
        res = LinearTextCombination([
            Text('test', metadata=ElementMetadata(section=f'html/body/p[{k}]')) for k in range(1, i+1)
                 ])

        assert res.metadata.section == ','.join([f'html/body/p[{k}]' for k in range(1, i+1)])


def test_linear_combination_append():
    ltc = LinearTextCombination([Text('test'), Text('test2')])
    ltc.append(Text('test3'))

    assert ltc.text == 'test test2 test3'
    assert len(ltc.elements) == 3

def test_linear_combination_append_many():
    ltc1 = LinearTextCombination([Text('test'), Text('test2')])
    ltc2 = LinearTextCombination([Text('test3'), Text('test4')])
    ltc1.append(ltc2)

    assert ltc1.text == 'test test2 test3 test4'
    assert len(ltc1.elements) == 4


