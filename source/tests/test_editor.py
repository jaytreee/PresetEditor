""" Unittest for Preset Editor
"""
import unittest
import pickle
from preset_editor import PresetEditor
from xmlfileparser import XmlFileParser
import pytest
slow = pytest.mark.slow

class TestPresetEditor(unittest.TestCase):
    """TestCase subclass"""

    #@slow
    def test_loadxmlfile(self):
        """testing load of XmlFileParser and getViewingPresets(), 
            the viewlist should be the same   """

        path = 'H:/Code/com.itheramedical.PresetEditor/testdata/256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml'
        with open('H:/Code/com.itheramedical.PresetEditor/testdata/settings.pickle','rb') as f:
            test_settings = pickle.load(f)
        example_tree = XmlFileParser.read(self, path)
        preset = PresetEditor
        preset.viewlist.clear()
        preset.tree = example_tree
        preset.getViewingPresets(preset)
        
        self.assertEqual(preset.viewlist, test_settings)
        del test_settings[0][1]
        self.assertNotEqual(PresetEditor.viewlist, test_settings)

    def test_writexmlfile(self):
        """read xmlfile, write it and read again, settings should still be the same"""

        self.assertTrue(False)

    

if __name__ == '__main__':
    unittest.main()
