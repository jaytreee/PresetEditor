import PyQt5.QtWidgets
from unittest import TestCase
from unittest.mock import MagicMock
from preset_editor import PresetEditor
import logging
import time
import sys

class Test_PresetEditor(TestCase):
    def test_load_inconsistent(self):
        app = PyQt5.QtWidgets.QApplication([])
        pe = PresetEditor(False)
        # load inconsistent file
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel_Inconsistent.XML'
        ret = pe.loadxmlFile(testfile)
        assert ret 
        assert pe.loadeddata
        assert pe.consistencywarning
        # load file with XML Error
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel_ERROR.XML'
        ret = pe.loadxmlFile(testfile)
        assert not ret 
        assert not pe.loadeddata
        assert not pe.consistencywarning
        # nonexistent file
        with self.assertRaises(FileNotFoundError):
            ret = pe.loadxmlFile('blabla')  
        assert not pe.loadeddata

    def test_load(self):
        app = PyQt5.QtWidgets.QApplication([])
        pe = PresetEditor(False)
        # load consistent file
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel.XML'
        ret = pe.loadxmlFile(testfile)
        assert ret 
        assert pe.loadeddata

        # Wrong major version
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel_WRONGv2.XML'
        ret = pe.loadxmlFile(testfile)
        assert not ret 
        assert not pe.loadeddata
        assert pe.versionwarning == logging.ERROR

        # Wrong minor version
        testfile = 'testdata\\2D_Masterpreset_Hb HbO2 Melanin_multipanel_WrongMinor.XML'
        ret = pe.loadxmlFile(testfile)
        assert ret 
        assert pe.loadeddata
        assert pe.versionwarning == logging.WARNING

        # No version
        testfile = 'testdata\\2D_Masterpreset_singleWL800_dual panel_NoVersion.XML'
        ret = pe.loadxmlFile(testfile)
        assert ret 
        assert pe.loadeddata
        assert pe.versionwarning == logging.WARNING

    def test_import(self):
        app = PyQt5.QtWidgets.QApplication([])
        pe = PresetEditor(False)
        # load consistent file
        testfile = 'testdata\\Scan_1.msot'
        ret = pe.importscan(testfile)
        assert ret 
        assert pe.loadeddata


def test_bindings_ID(qapp, qtbot):
    mymock = MagicMock()
    pe = PresetEditor(False)
    pe.contentHashChanged.connect(mymock)
    # load inconsistent file
    testfile = 'testdata\\2D_Masterpreset_Hb HbO2 Melanin_multipanel.XML'
    ret = pe.loadxmlFile(testfile)
    pe.viewSpectraList.setCurrentRow(0)
    last_hash = pe.contentHashBox.text()
    qtbot.addWidget(pe.window)
    
    for el in pe.window.findChildren((PyQt5.QtWidgets.QLineEdit, PyQt5.QtWidgets.QSpinBox, PyQt5.QtWidgets.QDoubleSpinBox)):
        if not el.isEnabled():
            continue
        if el.objectName() in ('PresetType', 'appscientistname'):  # excluded from content
            continue
        if isinstance(el.parent(), (PyQt5.QtWidgets.QDoubleSpinBox, PyQt5.QtWidgets.QSpinBox)):  #don't check child widgets ofSpin boxes
            continue
        mymock.reset_mock()

        # No change doesnt change
        el.editingFinished.emit()
        assert mymock.call_count >= 1, 'Edit {} does not fire preset ID update'.format(el.objectName())
        assert mymock.call_args[0][0] == last_hash, 'Edit {} updates preset Hash without content change'.format(el.objectName())

        # Don't check content of these:
        if el.objectName() in ('nameBox', 'versionTextBox', 'SFAFrameThreshBox'):
            continue

        # Chnaging the value impacts hash
        mymock.reset_mock()
        if isinstance(el, PyQt5.QtWidgets.QLineEdit):
            if el.text().isdecimal():
                el.setText(str(int(el.text()) + 1))
                qtbot.keyClick(el, PyQt5.QtCore.Qt.Key_Enter)
            else:
                el.setText(el.text() + 'x')
                qtbot.keyClick(el, PyQt5.QtCore.Qt.Key_Enter)
        else:
            el.stepUp()
            # qtbot.keyClick(el, PyQt5.QtCore.Qt.Key_PageUp)
            # qtbot.keyClick(el, PyQt5.QtCore.Qt.Key_Enter)
        # time.sleep(0.05)
        qapp.processEvents()
        assert mymock.call_count >= 1, 'Edit {} does not fire preset ID update'.format(el.objectName())
        chash = mymock.call_args[0][0]
        assert last_hash != chash, 'Edit {} does not influence preset ID'.format(el.objectName())
        
        last_hash = chash
        logging.debug('Edit fired preset ID generation OK: {}'.format(el.objectName()))

    # Checkboxes
    for el in pe.window.findChildren((PyQt5.QtWidgets.QCheckBox, )):
        mymock.reset_mock()

        # # No change doesnt change
        # el.toggled.emit(el.checkState())
        # assert mymock.call_count >= 1, 'Checkbox {} does not fire preset ID update'.format(el.objectName())
        # assert mymock.call_args[0][0] == last_hash, 'Checkbox {} updates preset Hash without content change'.format(el.objectName())

        # Chnaging the value impacts hash
        mymock.reset_mock()
        qtbot.mouseClick(el, PyQt5.QtCore.Qt.LeftButton)
        qapp.processEvents()
        assert mymock.call_count >= 1, 'Checkbox {} does not fire preset ID update'.format(el.objectName())
        chash = mymock.call_args[0][0]
        assert last_hash != chash, 'Checkbox {} does not influence preset ID'.format(el.objectName())
    
    # Combo Boxes
    for el in pe.window.findChildren(PyQt5.QtWidgets.QComboBox):
        mymock.reset_mock()

        # # No change doesnt change
        # el.toggled.emit(el.checkState())
        # assert mymock.call_count >= 1, 'Checkbox {} does not fire preset ID update'.format(el.objectName())
        # assert mymock.call_args[0][0] == last_hash, 'Checkbox {} updates preset Hash without content change'.format(el.objectName())

        # Chnaging the value impacts hash
        mymock.reset_mock()
        el.setCurrentIndex(el.currentIndex() + 1)
        qapp.processEvents()
        assert mymock.call_count >= 1, 'Checkbox {} does not fire preset ID update'.format(el.objectName())
        chash = mymock.call_args[0][0]
        assert last_hash != chash, 'Checkbox {} does not influence preset ID'.format(el.objectName())

def test_browsing(qapp):
    mymock = MagicMock()
    pe = PresetEditor(False)
    pe.contentHashChanged.connect(mymock)
    # load inconsistent file
    testfile = 'testdata\\2D_Masterpreset_Hb HbO2 Melanin_multipanel.XML'
    ret = pe.loadxmlFile(testfile)
    pe.viewSpectraList.setCurrentRow(0)
    pe.UItoTree()
    init_hash = mymock.call_args[0][0]

    # change panel
    pe.view2Button.clicked.emit()
    assert mymock.call_args[0][0] == init_hash, 'content hash changed when changing view'

    # change spectrum
    pe.viewSpectraList.setCurrentRow(2)
    assert mymock.call_args[0][0] == init_hash, 'content hash changed when changing layer (1)'

    # change spectrum
    pe.viewSpectraList.setCurrentRow(1)
    assert mymock.call_args[0][0] == init_hash, 'content hash changed when changing layer (1)'

    # change panel
    pe.view4Button.clicked.emit()
    assert mymock.call_args[0][0] == init_hash, 'content hash changed when changing view (2)'

def test_load_subsequent(qapp):
    mymock = MagicMock()
    pe = PresetEditor(False)
    pe.contentHashChanged.connect(mymock)
    # load inconsistent file
    testfile = 'testdata\\2D_Masterpreset_Hb HbO2 Melanin_multipanel.XML'
    ret = pe.loadxmlFile(testfile)
    assert ret
    pe.viewSpectraList.setCurrentRow(0)
    pe.UItoTree()
    assert pe.enableMultiPanel.isEnabled()

    testfile2 = 'testdata\\2D_Masterpreset_singleWL800_dual panel.XML'
    ret = pe.loadxmlFile(testfile2)
    assert ret  #make sure it loaded sanely without consistency error
    assert not pe.enableMultiPanel.isEnabled()
