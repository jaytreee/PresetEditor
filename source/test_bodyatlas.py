from bodyatlas import BodyAtlasModel
from lxml import etree
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets


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

def test_export():
    ba = BodyAtlasModel(None)
    root = etree.parse('testdata\\bodyAtlas.xml').getroot()
    ba.setRootNode(root)
    contentparser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    cleantree = etree.fromstring(etree.tostring(root), contentparser) 

    # No change needs to returen the same tree
    newroot = ba.toXML()
    assert etree.tostring(cleantree) == etree.tostring(newroot)

    # Delete an item should make the tree shorter
    rootidx = ba.index(0, 0)
    delidx = ba.index(0, 0, rootidx)
    nodename = ba.data(delidx)
    ba.removeRow(delidx.row(), delidx.parent())

    newroot = ba.toXML()
    assert len(etree.tostring(cleantree)) > len(etree.tostring(newroot))
    assert nodename not in etree.tostring(newroot).decode('utf-8')

def test_image(qapp):
    ba = BodyAtlasModel(None)
    root = etree.parse('testdata\\bodyAtlas.xml').getroot()
    ba.setRootNode(root)
    rootidx = ba.index(0, 0)
    chestidx = ba.index(7, 0, rootidx)
    qimg = ba.getImage(chestidx)

