"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os, glob
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

        # get first xsd file in directory
        # xsdpath = (os.path.splitext(path)[0]+'.xsd')
        direc = os.path.dirname(path)
        oldpath = os.getcwd()
        os.chdir(direc)
        xsdfile = glob.glob('*.xsd')
        if xsdfile:
            #schema_doc = etree.parse((os.path.splitext(path)[0]+'.xsd'))
            schema_doc = etree.parse(direc+'/'+xsdfile[0])
            xmlschema = etree.XMLSchema(schema_doc)
            #Validate
            '''   if xmlschema.validate(tree):
                print('valid schema')
            else:
                print('invalid schema' )'''
            try:
                xmlschema.assertValid(tree)
                print('valid schema')
            except etree.DocumentInvalid as err:
                print('Schema invalid: ' + str(err))

            
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('XML Schema could not be found')
            msg.exec()




        #print(etree.tostring(tree, pretty_print=False))
        os.chdir(oldpath)
        return tree



    def write(self, settings, path):
        """ write the Settings to an xml file"""
        settings.write(path[0], pretty_print=True)
        msg = QtWidgets.QMessageBox()
        msg.setText('Saved')
        msg.exec()
