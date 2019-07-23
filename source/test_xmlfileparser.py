from unittest import TestCase
from xmlfileparser import XmlFileParser
import os
import tempfile
from lxml import etree


class Test_XMLFileParser(TestCase):
    
    def test_init(self):
        x = XmlFileParser()
        # strings not empty
        self.assertTrue(x.sf)
        self.assertTrue(x.sn)
        self.assertTrue(os.path.isfile(os.path.join(x.sf, x.sn)))

    def test_read_error(self):
        # Needs Schema for tree validation
        path = 'testdata'
        fn = '2D_Masterpreset_singleWL800_dual panel_ERROR.XML'
        x = XmlFileParser()
        tree = x.read(path+'\\'+fn)
        self.assertIsNone(tree)

    def test_readwrite(self):
        # test consistency between read write
        path = 'testdata'
        fn = '2D_Masterpreset_Hb HbO2 Melanin_multipanel.XML'
        x = XmlFileParser()
        tree = x.read(path+'\\'+fn)
        (oh, of) = tempfile.mkstemp()
        os.close(oh)
        # delete previous testoutput
        x.write(tree, of, message=False)
        tree2 = x.read(of)
        self.assertEqual(etree.tostring(tree), etree.tostring(tree2))
        os.remove(of)
        
