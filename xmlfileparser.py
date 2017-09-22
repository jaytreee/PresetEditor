"""
XML/XSD  file parser, for Preset Editor GUI
"""

# pylint: disable=E1101

import os
from lxml import etree


class XmlFileParser:
    """Class for Read and Write of XML files"""



    def read(self, path):
        """parse xml file and xsd file in the same folder and validate
            returns: lxml.etree 
        """
        print(path)
        tree = etree.parse(path)

        # get xsd file
        schema_doc = etree.parse((os.path.splitext(path)[0]+'.xsd'))
        xmlschema = etree.XMLSchema(schema_doc)

        #Validate
        if(xmlschema.validate(tree)):
            print('valid schema')

        else:
            print('invalid schema')

        #print(etree.tostring(tree, pretty_print=False))
        return tree



    def write(self, settings):
        """ write the Settings to an xml file"""
        print(settings)
