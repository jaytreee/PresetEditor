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
        fn = '2D_Masterpreset_v2.0_800nm_dualpanel_XMLERROR.XML'
        x = XmlFileParser()
        tree = x.read(path+'\\'+fn)
        self.assertIsNone(tree)

    def test_read_nohash(self):
        """ Should return a warning if the preset is not authentic """
        path = 'testdata'
        fn = '2D_Masterpreset_v2.0_Hb HbO2 Melanin_multipanel_NOHASH.XML'
        x = XmlFileParser()
        (tree, warn, compat, chash) = x.read(path+'\\'+fn)
        self.assertTrue(warn)
        self.assertIsNone(compat)

    def test_readwrite(self):
        """ test consistency between read write """
        path = 'testdata'
        fn = '2D_Masterpreset_v2.0_Hb HbO2 Melanin_multipanel.XML'
        x = XmlFileParser()

        # read file
        (tree, warn, compat, inithash) = x.read(path+'\\'+fn)
        self.assertFalse(warn)

        # temp file
        (oh, of) = tempfile.mkstemp()
        os.close(oh)
        # delete previous testoutput
        wrhash = x.write(tree, of, message=False, version='TEST', compat=compat)
        self.assertEqual(inithash, wrhash)  # written hash should be equivalent to read hash

        # Read written file and check contentis identcal
        (tree2, warn, compat, readhash) = x.read(of)
        self.assertFalse(warn)
        self.assertEqual(inithash, readhash)

        os.remove(of)
        
    def test_readGUILocking(self):
        x = XmlFileParser()
        ret = x.readGUILockingOptions()
        assert len(ret) > 0
        assert isinstance(ret[0], str)