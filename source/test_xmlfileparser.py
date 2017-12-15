from unittest import TestCase
from xmlfileparser import XmlFileParser
import os
from lxml import etree


class Test_ViewSetting(TestCase):
    
    def test_init(self):
        x = XmlFileParser()
        # strings not empty
        self.assertTrue(x.sf)
        self.assertTrue(x.sn)
        # schema name has xsd as file ending
        self.assertEqual(x.sn[-4:], '.xsd')


    def test_read(self):
        # Needs Schema for tree validation
        path = r'H:\Code\com.itheramedical.PresetEditor\source\tests\testdata'
        fn = r'256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml'
        x = XmlFileParser()
        tree = x.read(path+'\\'+fn)
        self.assertFalse(tree is None)

    def test_write(self):
        path = r'H:\Code\com.itheramedical.PresetEditor\source\tests\testdata'
        fn = r'256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml'
        x = XmlFileParser()
        tree = x.read(path+'\\'+fn)
        of = path+'\\'+'testout.xml'
        # delete previous testoutput
        if os.path.isfile(of):
            os.remove(of)
        x.write(tree, of, message=False)
        self.assertTrue(os.path.isfile(of))


    def test_readwrite(self):
        # test consistency between read write
        path = r'H:\Code\com.itheramedical.PresetEditor\source\tests\testdata'
        fn = r'256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml'
        x = XmlFileParser()
        tree = x.read(path+'\\'+fn)
        of = path+'\\'+'testout.xml'
        # delete previous testoutput
        x.write(tree, of, message=False)
        tree2 = x.read(of)
        self.assertEqual(etree.tostring(tree), etree.tostring(tree2))
        
