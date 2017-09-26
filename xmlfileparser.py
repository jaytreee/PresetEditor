"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os
from lxml import etree
from  PyQt5 import QtWidgets


class XmlFileParser:
    """Class for Read and Write of XML files"""



    def read(self, path):
        """parse xml file and xsd file in the same folder and validate
            returns: lxml.etree 
        """
        print(path)
        tree = etree.parse(path)

        # get xsd file
        xsdpath = (os.path.splitext(path)[0]+'.xsd')
        if os.path.isfile(xsdpath):
            schema_doc = etree.parse((os.path.splitext(path)[0]+'.xsd'))
            xmlschema = etree.XMLSchema(schema_doc)
            #Validate
            if xmlschema.validate(tree):
                print('valid schema')
            else:
                print('invalid schema')
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('XML Schema could not be found')
            msg.exec()




        #print(etree.tostring(tree, pretty_print=False))
        return tree



    def write(self, settings, path):
        """ write the Settings to an xml file"""
        settings.write(path[0], pretty_print=True)
        msg = QtWidgets.QMessageBox()
        msg.setText('Saved')
        msg.exec()
