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