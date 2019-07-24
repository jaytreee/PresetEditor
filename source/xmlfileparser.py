"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os, glob, sys, re
from hashlib import blake2s
from base64 import b64encode
from lxml import etree
from copy import deepcopy
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
        logging.debug('Loading {}'.format(path))
        # TODO: remove comment to remove whitespace to add linebreaks
        
        try:
            tree = etree.parse(path)
        except etree.XMLSyntaxError as err:
            logging.debug('Exception while parsing {}'.format(path), exc_info=err)
            logging.error('File invalid: ' + str(err))
            return None
        
        # Load schema
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
        
        # Check if this file was saved using the preset editor by scanning for auto-tag
        filehash = None
        compat = None
        hashwarning = False
        for item in tree.getroot():  # First parse and take out auto comment
            if isinstance(item, etree._Comment):
                match = re.search("^ Content hash: ([A-Za-z0-9+/]+) # Compatible: <=([0-9\.]+) $", item.text)
                if match is not None:  # save content hash
                    filehash = match[1]
                    compat = match[2]
                    logging.debug('Found auto-tag in file (Content-hash: {}, Compat: {})'.format(filehash, compat))
                    tree.getroot().remove(item)  # Take out, we will add a new one when saving

        # copy of tree to take all other comments and tails out
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        contenttree = etree.parse(path, parser) 
        # Get hash of the file content (reduced tree)
        hsh = int.from_bytes(blake2s( etree.tostring(contenttree) , digest_size=12).digest(),'little')
        hashstr = b64encode(hsh.to_bytes(12,'little')).decode('utf-8')
        # Compare Hash and show warning
        if filehash is None or filehash != hashstr:
            logging.debug('Content hash is: {} (in file: {})'.format(hashstr, filehash))
            logging.warning('Preset is not authentic - Please contact iThera for a valid template!')
            hashwarning = True

        logging.info('Successfully parsed and validated file {}'.format(path))
        return tree, hashwarning, compat



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
