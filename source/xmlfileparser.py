"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os, glob, sys, re
from hashlib import sha1
from lxml import etree
from copy import deepcopy
from  PyQt5 import QtWidgets, QtCore
import logging
import datetime


class XmlFileParser:
    """Class for Read and Write of XML files"""
    def __init__(self):
        # schema folder
        self.sf  = 'schemata'
        if hasattr(sys, '_MEIPASS'):
            self.sf = os.path.join(sys._MEIPASS, self.sf)
        # schema name
        self.sn = 'ArrayOfDataModelStudyPreset.xsd'

    def read(self, path, xmlstring=None):
        """parse xml file and xsd file in the same folder and validate
            returns: lxml.etree 
        """
        logging.debug('Loading {}'.format(path))
        
        try:
            if path is not None:
                tree = etree.parse(path)
            else: 
                root = etree.fromstring(xmlstring)
                tree = etree.ElementTree(root)
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
        
        # Check if this file was saved using the preset editor by scanning for auto-tag
        filehash = None
        compat = None
        hashwarning = False
        for item in tree.getroot():  # First parse and take out auto elements
            # Find and take out contentHash (only for validation)
            if item.tag == 'DataModelStudyPreset':  # 
                if 'contentHash' in item.attrib:
                    filehash = item.attrib['contentHash']
                    logging.debug('Found content hash in file: {}'.format(filehash))
                    del item.attrib['contentHash']
            # Find compatibility tag
            elif isinstance(item, etree._Comment):
                match = re.search("^ Compatible Software Version: <=([0-9.]+) $", item.text)
                if match is not None:  # save content hash
                    compat = match[1]
                    logging.debug('Found compatibility-tag in file: {}'.format(compat))
                    # Comments will be removed anyways

        # Compare Hash and show warning (if not importing from Scan)
        hashstr = self.get_contenthash(tree)
        if (filehash is None or filehash != hashstr) and xmlstring is None:
            logging.debug('Content hash is: {} (in file: {})'.format(hashstr, filehash))
            logging.warning("This doesn't look like a Master Preset, please ask an Application Specialist as this preset might produce unexpected behaviours")
            hashwarning = True
        if compat is None:
            logging.warning('Missing software version compatibility tag - Please use a verified template!')

        logging.info('Successfully parsed and validated file {}'.format(path))
        return tree, hashwarning, compat, hashstr

    @staticmethod
    def get_contenthash(tree):
        """ copy of tree to take all other comments and tails out, get the hash """
        presetelem = None  # isolate the preset element
        for item in tree.getroot():
            if item.tag == 'DataModelStudyPreset':
                presetelem = item
                break
        if presetelem is None:
            logging.error('Preset Element not found in tree')
            return None
        # At this point, there is o contentHash attribute anymore
        # This creates a tree copy without blanks and comments
        contentparser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        contenttree = etree.fromstring(etree.tostring(presetelem), contentparser) 
        
        # Remove Preset Name, Preset Identifier, Preset Version for "functional content" only hash
        for item in contenttree:
            if item.tag in ('PresetIdentifier', 'Name', 'PresetType', 'PresetVersion', 'IsDefaultPreset'):
                contenttree.remove(item)

        xmlbytes = etree.tostring(contenttree)
        chash = sha1()
        chash.update(xmlbytes)
        # Hex output
        hashstr = chash.hexdigest()
        logging.debug('Content hash is now {}'.format(hashstr))
        return hashstr


    def write(self, origtree, path, message=True, version='Y.YY-revZZ', compat='x.x.xx', initials='XX', presetversion='Q'):
        """ write the Settings to an xml file and add comment to the top of the file"""
        # copy of tree to take all other comments and tails out, get the hash
        hashstr = self.get_contenthash(origtree)

        # Copy to make sure modifications don't propagate to working tree
        settings = deepcopy(origtree)

        # Change Log
        comment = ' * '.join((
            QtCore.QDateTime(datetime.datetime.now()).toString("yyyy-MM-dd HH:mm:ss"),
            '{:<3}'.format(initials),
            'v' + presetversion,
            '#' + hashstr,
            'PE ' + version
        ))
        comment = etree.Comment(' ' + comment + ' ')
        comment.tail = '\n'

        presetelem = None  # isolate the preset element
        for item in settings.getroot():
            if item.tag == 'DataModelStudyPreset':
                presetelem = item
                break
        if presetelem is None:
            logging.error('Preset Element not found in tree')
            return None
        presetelem.set('contentHash', hashstr)
        presetelem.insert(0, comment)
        settings.write(path, pretty_print=True, xml_declaration=True, encoding='utf-8')
        if message:
            msg = QtWidgets.QMessageBox()
            msg.setText('Saved as {}'.format(os.path.basename(path)))
            msg.setInformativeText('Content hash: {}'.format(hashstr))
            msg.exec()
        
        return hashstr

    def readGUILockingOptions(self):
        schemafile = os.path.join(self.sf, 'Types.xsd')
        if not os.path.isfile(schemafile):
            logging.error('Schema file {} not found'.format(schemafile))
            logging.debug('Current dir contains: {}'.format(','.join(glob.glob('*'))))
            return None
        xmlschema = etree.parse(schemafile)

        ret = []
        for el in xmlschema.getroot():
            if 'name' in el.attrib and el.attrib['name'] == 'ControlsEnablingProperty':
                for subel in el[0]:
                    if subel.attrib['value'] in ('None', 'All'):
                        continue
                    ret.append(subel.attrib['value'])
                break
        return ret


