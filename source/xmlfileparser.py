"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os, glob, sys
from lxml import etree
from  PyQt5 import QtWidgets


class XmlFileParser:
    """Class for Read and Write of XML files"""



    def read(self, path):
        """parse xml file and xsd file in the same folder and validate
            returns: lxml.etree 
        """
        print(path)
        # TODO: remove comment to remove whitespace to add linebreaks
        
        # parser = etree.XMLParser(remove_blank_text=True)
        # tree = etree.parse(path, parser)
        tree = etree.parse(path)

        # get first xsd file in directory
        # xsdpath = (os.path.splitext(path)[0]+'.xsd')
        
        # use schema saved under %appdata%/...

        xmlschema = etree.XMLSchema(etree.parse(r'C:\Users\thomas.hartmann\AppData\Roaming\iThera\Schemata\Types.xsd'))


        try:
            xmlschema.assertValid(tree)
            print('valid schema')
        except etree.DocumentInvalid as err:

            print('Schema invalid: ' + str(err))
            msg = QtWidgets.QMessageBox()
            msg.setText('Schema invalid/ XML file is not supported\n'+
            str(err))
            msg.exec()
            # sys.exit(-1)
        

        return tree



    def write(self, settings, path):
        """ write the Settings to an xml file"""
        # print(etree.tostring(settings, pretty_print=True))
        settings.write(path[0], pretty_print=True)
        msg = QtWidgets.QMessageBox()
        msg.setText('Saved')
        msg.exec()
