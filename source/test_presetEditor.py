import PyQt5.QtWidgets
from unittest import TestCase
from preset_editor import PresetEditor


class Test_PresetEditor(TestCase):
    def test_load_inconsistent(self):
        app = PyQt5.QtWidgets.QApplication([])
        pe = PresetEditor(False)
        # load inconsistent file
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel_Inconsistent.XML'
        ret = pe.loadxmlFile(testfile)
        assert not ret 
        assert not pe.loadeddata
        # load file with no hash
        testfile = 'testdata\\2D_Masterpreset_Hb HbO2 Melanin_multipanel_NOHASH.XML'
        ret = pe.loadxmlFile(testfile)
        assert not ret 
        assert not pe.loadeddata
        # load file with XML Error
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel_ERROR.XML'
        ret = pe.loadxmlFile(testfile)
        assert not ret 
        assert not pe.loadeddata
        # nonexistent file
        with self.assertRaises(FileNotFoundError):
            ret = pe.loadxmlFile('blabla')  
        assert not pe.loadeddata

    def test_load(self):
        app = PyQt5.QtWidgets.QApplication([])
        pe = PresetEditor(False)
        # load inconsistent file
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel.XML'
        ret = pe.loadxmlFile(testfile)
        assert ret 
        assert pe.loadeddata

    def test_bindings_ID(self):
        app = PyQt5.QtWidgets.QApplication([])
        pe = PresetEditor(False)
        # load inconsistent file
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel.XML'
        ret = pe.loadxmlFile(testfile)

        for el in pe.window.findChildren((PyQt5.QtWidgets.QLineEdit, PyQt5.QtWidgets.QCheckBox, PyQt5.QtWidgets.QComboBox, PyQt5.QtWidgets.QSpinBox, PyQt5.QtWidgets.QDoubleSpinBox)):
            pass
