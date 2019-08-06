import PyQt5.QtGui
from PyQt5.QtCore import Qt
from lxml import etree


class BodyAtlasModel(PyQt5.QtGui.QStandardItemModel):
    
    def __init__(self, parent):
        super().__init__(0, 1, parent)

        self.root = None

    def setRootNode(self, node):
        self.root = node    
        self.clear()

        self.addWithChildren(self.root, self.invisibleRootItem(), 0)


        # self.dataChanged.emit(
        #     self.createIndex(0, 0),
        #     self.createIndex(self.rowCount(), 0),
        #     []
        # )

    def addWithChildren(self, node, root, idx):
        name = node.find('./Name').text
        item = PyQt5.QtGui.QStandardItem(name)

        img = node.find('./ImageDataBase64').text
        item.setData(img, Qt.UserRole)

        root.setChild(idx, item)

        for idx, el in enumerate(node.find('./Children')):
            self.addWithChildren(el, item, idx)

    def toXML(self):
        root = etree.Element('Root')
        qitem = self.invisibleRootItem().child(0, 0)

        name = etree.SubElement(root, 'Name')
        name.text = qitem.data(Qt.DisplayRole)

        idata = etree.SubElement(root, 'ImageDataBase64')
        idata.text = qitem.data(Qt.UserRole)

        childroot = etree.SubElement(root, 'Children')

        self.childrenToXML(qitem, childroot)

        return root

    def childrenToXML(self, rootqitem, xmlroot):
        for row in range(rootqitem.rowCount()):
            qitem = rootqitem.child(row, 0)
            item = etree.SubElement(xmlroot, 'DataModelBodyAtlasNode')
            
            name = etree.SubElement(item, 'Name')
            name.text = qitem.data(Qt.DisplayRole)

            idata = etree.SubElement(item, 'ImageDataBase64')
            idata.text = qitem.data(Qt.UserRole)

            childroot = etree.SubElement(item, 'Children')
            self.childrenToXML(qitem, childroot)


    # def columnCount(self, parent=None):
    #     if self.root is None:
    #         return 0
    #     else:
    #         return 1

    # def rowCount(self, parent=None):
    #     if self.root is None:
    #         return 0
    #     elif parent is not None:  # Sub-Element
    #         elem = self.data(parent, PyQt5.QtCore.Qt.UserRole)
    #         return len(elem.find('./Children'))
    #     else:
    #         return 1

    # def getChild(self, idx, row):
    #     ptr = idx.internalPointer()
    #     if ptr is None:
    #         return None
    #     for el in ptr:
    #         if el.tag == 'Children':
    #             return el[row]
    #     return None

    # def getIndexForElement(self, element):
    #     if element is self.root:
    #         return self.createIndex(0, 0)
    #     # All other elements have parents
    #     parent = element.getparent()
    #     row = parent.index(element)

    #     # Get parent - this will go recursively until root
    #     parentidx = self.getIndexForElement(parent.getparent())
    #     return self.index(row, 0, parentidx)

    # def index(self, row, col, parent=None):
    #     if parent is None or not parent.isValid():  # index points to root node (may be None)
    #         ptr = self.root
    #     else:
    #         ptr = self.getChild(parent, row)
    #     idx = self.createIndex(row, 0, ptr)
    #     return idx

    # def parent(self, idx):
    #     if self.root is None or idx.internalPointer() is self.root:  # root item
    #         return PyQt5.QtCore.QModelIndex()  # invalid Index
    #     ptr = idx.internalPointer()
    #     parent = ptr.getparent().getparent()  # parent XML tag
    #     return self.getIndexForElement(parent)
        
    # def data(self, idx, role=PyQt5.QtCore.Qt.DisplayRole):
    #     if self.root is None:
    #         return None

    #     target = idx.internalPointer()

    #     if role == PyQt5.QtCore.Qt.UserRole:
    #         return target
    #     return target.find('./Name').text
