"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os, glob, sys
from lxml import etree
from  PyQt5 import QtWidgets
import logging


class XmlFileParser:
    """Class for Read and Write of XML files"""
    def __init__(self):
        # schema folder
        self.sf  = 'schemata'
        if hasattr(sys, '_MEIPASS'):
            self.sf = os.path.join(sys._MEIPASS, self.sf)
        # schema name
        self.sn = 'ArrayOfDataModelStudyPreset.xsd'


    def read(self, path):
        """parse xml file and xsd file in the same folder and validate
            returns: lxml.etree 
        """
        print(path)
        # TODO: remove comment to remove whitespace to add linebreaks
        
        try:
            tree = etree.parse(path)
        except etree.XMLSyntaxError as err:
            logging.debug('Exception while parsing {}'.format(path), exc_info=err)
            logging.error('File invalid: ' + str(err))
            return None
        
        schemafile = os.path.join(self.sf, self.sn)
        if not os.path.isfile(schemafile):
            logging.error('Schema file {} not found'.format(schemafile))
            logging.debug('Current dir contains: {}'.format(','.join(glob.glob('*'))))
            return None
        xmlschema = etree.XMLSchema(etree.parse(schemafile))
        
        try:
            xmlschema.assertValid(tree)
        except etree.DocumentInvalid as err:
            logging.debug('Exception while validating {}'.format(path), exc_info=err)
            logging.error('XML Schema validation error: ' + str(err))
            return None
            # sys.exit(-1)
        
        logging.info('Successfully parsed and validated file {}'.format(path))
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
