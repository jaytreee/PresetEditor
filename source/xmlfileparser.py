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
            

        # when no Schema is in Directory of the xml File load it from internally    
        else:
            print('could not find local schema \n using SchemaV1.0')
            if hasattr(sys, "_MEIPASS"):
                
                
                xmlschema = etree.XMLSchema(etree.parse(os.path.join(sys._MEIPASS, 'SchemaV1.0.xsd')))
            
            else:
                xmlschema = etree.XMLSchema(etree.parse(r'H:\Code\com.itheramedical.PresetEditor\source\resources\SchemaV1.0.xsd'))
                

        try:
            xmlschema.assertValid(tree)
            print('valid schema')
        except etree.DocumentInvalid as err:

            print('Schema invalid: ' + str(err))
            msg = QtWidgets.QMessageBox()
            msg.setText('Schema invalid/ XML file is not supported')
            msg.exec()
            sys.exit(-1)
        
         




        #print(etree.tostring(tree, pretty_print=False))
        os.chdir(oldpath)
        return tree



    def write(self, settings, path):
        """ write the Settings to an xml file"""
        # print(etree.tostring(settings, pretty_print=True))
        settings.write(path[0], pretty_print=True)
        msg = QtWidgets.QMessageBox()
        msg.setText('Saved')
        msg.exec()
