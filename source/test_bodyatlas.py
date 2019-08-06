from bodyatlas import BodyAtlasModel
from lxml import etree
from PyQt5.QtCore import Qt


def test_empty_model():
    ba = BodyAtlasModel(None)
    assert ba.rowCount() == 0
    assert ba.columnCount() == 0

def test_model():
    ba = BodyAtlasModel(None)
    root = etree.parse('testdata\\bodyAtlas.xml').getroot()
    ba.setRootNode(root)
    rootidx = ba.index(0, 0)
    assert ba.data(rootidx) == 'Body'
    assert ba.rowCount(rootidx) == 11

    assert ba.data(ba.index(0, 0, rootidx)) == 'Abdomen back'
    assert ba.data(ba.index(0, 0, rootidx)) == ba.data(rootidx.child(0, 0))

    chestidx = ba.index(7, 0, rootidx)
    assert chestidx.parent() == rootidx

    subindex = ba.index(1, 0, chestidx)
    assert subindex.parent() == chestidx
    assert ba.data(subindex) == 'Breast front right'
    assert ba.data(subindex, Qt.UserRole)[0:6] == 'iVBORw'

