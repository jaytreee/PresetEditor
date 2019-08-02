from lxml import etree
import logging
import os, sys


def import_scan(filename, swcompat=None):
    if not os.path.isfile(filename):
        logging.error('MSOT File not found: {}'.format(filename))
        return None
    imgfile = filename.replace('.msot', '.img')
    if not os.path.isfile(imgfile):
        logging.error('IMG File not found: {}'.format(imgfile))
        return None

    tree = _load_and_verify(filename, 'DataModelMsotProject.xsd')
    if tree is None:
        return None

    imgtree = _load_and_verify(imgfile, 'DataModelImagingSuperSession.xsd')
    if imgtree is None:
        return None

    # Find OAM Preset as a template
    oampreset = tree.find('.//OAMPreset')
    oldviewingpresets = oampreset.find('.//ViewingPresets')

    # Get ViewingPresets from .img File and replace them
    viewingpresets = imgtree.find('.//ViewingPresets')
    oampreset.replace(oldviewingpresets, viewingpresets)

    newtree = etree.Element('ArrayOfDataModelStudyPreset')

    # Add SW Version compatibility tag
    swversion = tree.find('.//SW_Version').text
    if swcompat is not None:  # Check if Version compatible
        PE = LooseVersion(swcompat)
        PE_major = int(swcompat.split('.')[0])
        Scan = LooseVersion(swversion)
        Scan_major = int(swversion.split('.')[0])
        if Scan_major != PE_major:  # Show an error
            msg = 'Preset is from another vMc version - Please use correct Preset Editor'
            logging.error(msg)
            return None
        elif Scan > PE:  # Show a warning
            msg = 'Scan is made for by newer version of the software - check if newer Preset Editor is available. Could work fine though'
            logging.warning(msg)
    comm = etree.Comment(' Compatible Software Version: <={} '.format(swversion))
    newtree.append(comm)

    # Add preset
    oampreset.tag = 'DataModelStudyPreset'
    newtree.append(oampreset)

    return etree.tostring(newtree, pretty_print=True, xml_declaration=True, encoding='utf-8')

def _load_and_verify(filename, schemafile):
    # Load Scan Tree
    try:
        tree = etree.parse(filename)
    except etree.XMLSyntaxError as err:
        logging.debug('Exception while parsing {}'.format(filename), exc_info=err)
        logging.error('File invalid: ' + str(err))
        return None
    
    # Load schema
    schemadir  = 'schemata'
    if hasattr(sys, '_MEIPASS'):
        schemadir = os.path.join(sys._MEIPASS, schemadir)
    schemafile = os.path.join(schemadir, schemafile)
    if not os.path.isfile(schemafile):
        logging.error('Schema file {} not found'.format(schemafile))
        logging.debug('Current dir contains: {}'.format(','.join(glob.glob('*'))))
        return None
    xmlschema = etree.XMLSchema(etree.parse(schemafile))
    
    # Validate Schema
    try:
        xmlschema.assertValid(tree)
    except etree.DocumentInvalid as err:
        logging.debug('Exception while validating {}'.format(filename), exc_info=err)
        logging.error('XML Schema validation error: ' + str(err))
        return None

    return tree