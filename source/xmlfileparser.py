"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os, glob, sys
from lxml import etree
from  PyQt5 import QtWidgets


class XmlFileParser:
    """Class for Read and Write of XML files"""
    def __init__(self):
        # schema folder
        self.sf  = os.path.join(os.environ['APPDATA'], 'iThera\\Schemata')
        # schema name
        self.sn = 'ArrayOfDataModelStudyPreset.xsd'


    def read(self, path):
        """parse xml file and xsd file in the same folder and validate
            returns: lxml.etree 
        """
        print(path)
        # TODO: remove comment to remove whitespace to add linebreaks
        
        # parser = etree.XMLParser(remove_blank_text=True)
        # tree = etree.parse(path, parser)
        try:
            tree = etree.parse(path)
        except etree.XMLSyntaxError as err:
            print('File invalid: ' + str(err))
            msg = QtWidgets.QMessageBox()
            msg.setText('File invalid\n'+
            str(err))
            msg.exec()
            sys.exit()
        # get first xsd file in directory
        # xsdpath = (os.path.splitext(path)[0]+'.xsd')
        
        # use schema saved under %appdata%/...
        
        
        xmlschema = etree.XMLSchema(etree.parse(self.sf+'/'+ self.sn))
        
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



    def write(self, settings, path, message=True, comment=''):
        """ write the Settings to an xml file and add comment to the top of the file"""
        # print(etree.tostring(settings, pretty_print=True))
        # add comment about version and date if the comment has a previous change the existing
        # comment text
        root =settings.getroot()
        p = root.getprevious()
        if not p is None:
            p.text = comment #change text of existing comment
        else :
            root.addprevious(etree.Comment(comment))
        settings.write(path , pretty_print=True)
        if message:
            msg = QtWidgets.QMessageBox()
            msg.setText('Saved')
            msg.exec()
