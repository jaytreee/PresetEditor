"""
qt designer test
"""
# pylint: disable=E1101
# pylint: disable=C0103

import sys
import datetime
import os
import uuid
import bisect
import subprocess, re
import logging
import logging.handlers
from copy import deepcopy
#from pprint import pprint
from xmlfileparser import XmlFileParser
from lxml import etree
from PyQt5 import QtWidgets, QtCore
#from PyQt5.QtWidgets import QFileDialog
from preset_editor_gui import Ui_MainWindow
from viewsetting import LayerSetting, ViewSettings
from typechecker import ScalingValidator
from functools import partial
from errorhandler import ErrorLogHandler
from excelExporter import ExcelExporter

from addWavelengthDialog import Ui_AddWLDialog
#from schemamanager import iXMLSchemaManager
from viewEnum import ViewEnum


COLORMAPS = [
    'Gray',
    'Bone',
    'Hot',
    'Red',
    'Light-Red',
    'Green',
    'Light-Green',
    'Blue',
    'Light-Blue',
    'Cyan',
    'Magenta',
    'Yellow',
    'HSB_HSL',
    'Jet',
    'Union Jack',
    'RedBlueBlack',
    'Contrast'
]


class PresetEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Editor for Settings
    """
    tree = None

    originalSpectra = []
    # defaultspectra = ['OPUS', 'Background']

    allspectra = []
    """ all available spectra"""

    spectralist = []
    """selected spectra"""

    unselectedspectra = list(set(allspectra)-set(spectralist))
    """ unselected spectra at the start"""

    fsf = 'C:\ProgramData\iThera\ViewMSOTc\Factory Spectra'
    """factory spectra folder"""

    viewlist = [[], [], [], []]
    """dimensions = #views; containing corresponing layersetting objects """

    viewsettings = []
    """ settings for each view panel"""

    loadeddata = False
    """ was data loaded (for saving and displaying gui)"""

    xmlfp = XmlFileParser()

    version = ''
    """current version, is shown in GUI statusbar and added as comment in resulting xml files"""

    bgfound = False
    """ If the BGWavlength entry is found in preset"""

    sortedwvlist = []
    """ sorted wavelength list"""

    contentHashChanged = QtCore.pyqtSignal(str)

    def __init__(self, autoload=True):
        super(PresetEditor, self).__init__()
        self.window = QtWidgets.QMainWindow()
        self.setupUi(self.window)
        self.window.show()
        self.tabWidget.setEnabled(False)
        self.groupBox_5.setEnabled(False)

        self.muted = True
        self.excel_dict = dict()
        """Dictionary for easier excel export"""
        
        self.connectGUItoFunctionalty()
        for cmap in sorted(COLORMAPS):
            self.paletteType.addItem(cmap)

        # self.schemamanager = iXMLSchemaManager()
        # self.schemamanager.main()

        self.typechecker = ScalingValidator(0, 1, 5, None, -1)

        self.displayVersion()

        if autoload:
            self.loadxmlFile()
        


    def connectGUItoFunctionalty(self):
        """add Signals to Functions"""
                #self.addBtn.clicked.connect(self.addInputTextToListbox)
        self.loadButton.clicked.connect(self.loadxmlFile)
        self.saveAsButton.clicked.connect(self.writexmlFile)
        
        

        self.addWL.clicked.connect(self.addWavelength)
        self.removeWL.clicked.connect(self.removeWavelength)

        self.tabWidget.tabBarClicked.connect(self.applySettings)
        self.view1Button.clicked.connect(self.applySettings)
        self.view2Button.clicked.connect(self.applySettings)
        self.view3Button.clicked.connect(self.applySettings)
        self.view4Button.clicked.connect(self.applySettings)
        self.viewSpectraList.currentItemChanged.connect(self.applySettings)
        
        self.detectorBox.editingFinished.connect(self.UItoTree)
        self.nameBox.textChanged.connect(self.UItoTree)  # also live typing
        self.nameBox.editingFinished.connect(self.UItoTree)
        self.versionTextBox.textChanged.connect(self.UItoTree) # also live typing
        self.versionTextBox.editingFinished.connect(self.UItoTree)

        self.prefWLBox.currentIndexChanged.connect(self.UItoTree)
        self.displayAllWLBox.toggled.connect(self.UItoTree)
        self.usvisibleBox.toggled.connect(self.UItoTree)

        self.userSoundBox.editingFinished.connect(self.UItoTree)
        self.userSoundBox.valueChanged.connect(self.UItoTree)
        self.backgroundOxyBox.editingFinished.connect(self.UItoTree)
        self.backgroundOxyBox.valueChanged.connect(self.UItoTree)
        self.maxavgframes.editingFinished.connect(self.UItoTree)
        self.maxavgframes.valueChanged.connect(self.UItoTree)
        self.SFAFrameThreshBox.editingFinished.connect(self.UItoTree)
        self.SFAFrameThreshBox.valueChanged.connect(self.UItoTree)
        self.backgroundAbsorptionBox.editingFinished.connect(self.UItoTree)
        self.backgroundAbsorptionBox.valueChanged.connect(self.UItoTree)
        self.sfabuffersize.editingFinished.connect(self.UItoTree)
        self.sfabuffersize.valueChanged.connect(self.UItoTree)
        self.addButton.clicked.connect(self.addspectra)
        self.deleteButton.clicked.connect(self.removespectra)

        self.visibleCheck.clicked.connect(self.changeLayerSettings)
        self.loadCheck.clicked.connect(self.changeLayerSettings)
        self.logarithmicScalingCheck.clicked.connect(self.changeLayerSettings)
        self.paletteType.activated.connect(self.changeLayerSettings)
        self.paletteType.currentIndexChanged.connect(self.changeLayerSettings)
        self.transparentCheck.clicked.connect(self.changeLayerSettings)
        # self.minBox.editingFinished.connect(self.changeLayerSettings)
        # self.maxBox.editingFinished.connect(self.changeLayerSettings)
        self.maxBox.editingFinished.connect(self.maxThreshCheck)
        self.maxBox.valueChanged.connect(self.maxThreshCheck)
        self.minBox.editingFinished.connect(self.maxThreshCheck)
        self.minBox.valueChanged.connect(self.maxThreshCheck)
        
        self.enableMultiPanel.toggled.connect(self.toggleMultiPanel)

        self.radioButtons = [self.view1Button, self.view2Button, self.view3Button, self.view4Button]

        self.browseFactorySpectra.clicked.connect(self.changeFactorySpectra)

        self.loadFactorySpectra()
        self.unselectedspectra = list(set(self.allspectra)-set(self.spectralist))

        self.unselectedList.addItems(self.unselectedspectra)
        # self.viewSpectraList.addItems(self.defaultspectra)

        # ===== Processing========
        

        # ======== View Settings ===========
        self.autoScalingCheck.clicked.connect(self.changeViewSettings)
        self.bgWavelength.activated.connect(self.changeViewSettings)
        self.bgWavelength.currentIndexChanged.connect(self.changeViewSettings)
        self.usmin.editingFinished.connect(partial(self.scalingTypeCheck, self.usmin))
        self.usmax.editingFinished.connect(partial(self.scalingTypeCheck, self.usmax))
        self.bgmin.editingFinished.connect(partial(self.scalingTypeCheck, self.bgmin))
        self.bgmax.editingFinished.connect(partial(self.scalingTypeCheck, self.bgmax))
        self.fgmin.editingFinished.connect(partial(self.scalingTypeCheck, self.fgmin))
        self.fgmax.editingFinished.connect(partial(self.scalingTypeCheck, self.fgmax))

        # =========================================
        #self.treeWidget.itemDoubleClicked.connect(self.setTreeItem)

        # ===== GeneratePresetID =========
        self.detectorBox.editingFinished.connect(self.generatePresetID)
        self.nameBox.editingFinished.connect(self.generatePresetID)
        self.loadCheck.clicked.connect(self.generatePresetID)


    def displayVersion(self):
        # if exe
        if hasattr(sys, "_MEIPASS"):
            vf = os.path.join(sys._MEIPASS, 'version.txt')
            with open(vf,'r') as f:
                v = f.read()
            revf = os.path.join(sys._MEIPASS, 'revision.txt')
            with open(revf,'r') as f:
                rev = f.read()    
        else:
            with open('version.txt') as f:
                v = str(f.read()).strip()

            hgoutput = subprocess.run(['hg','id','-n'], stdout=subprocess.PIPE)
            hgoutput = hgoutput.stdout.decode('utf-8').strip()
            match = re.search('^([0-9]+)(\+)?$', hgoutput)

            rev = match.group(1)

        self.version = 'v'+v+ '-rev'+rev
        self.statusbar.showMessage(self.version)
        logging.info('PresetEditor started ({})'.format(self.version))

    def changeFactorySpectra(self):
        """ opens Windows File Dialog, to select folder for the FactorySpectra"""
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.fsf))
        if not os.path.isdir(folder):
            return
        self.loadFactorySpectra(folder)
        self.unselectedspectra = list(set(self.allspectra)-set(self.spectralist))
        self.unselectedList.clear()
        self.unselectedList.addItems(self.unselectedspectra)
        
    def scalingTypeCheck(self, field):
        """set Validator for TextInputs"""
        str = field.text()
        field.setText(self.typechecker.fixup(str))
        self.changeViewSettings()

    def maxThreshCheck(self):
        """ set Validator for UpperThreshold (has to be higher than lower threshold)"""
        if not self.maxBox.value() > self.minBox.value():
            self.maxBox.setValue(self.minBox.value()+0.5)
        self.changeLayerSettings()

    def loadFactorySpectra(self, folder=fsf):
        """load Factory Spectra from folder (default:  C:\ProgramData\iThera\ViewMSOTc\Factory Spectra) and cuts file 
        extension. This is the allspectra list"""
        if not os.path.isdir(folder):
            self.FactorySpectraTextBox.setText('No Factory Preset Folder Found')
            return

        self.allspectra = os.listdir(folder)
        # cut fileextension
        for i, s in enumerate(self.allspectra):
            self.allspectra[i] = os.path.splitext(s)[0]

        self.FactorySpectraTextBox.setText(folder)

    @QtCore.pyqtSlot()
    def loadxmlFile(self, fn=None):
        """ load xml File """

        if fn is None:
            path = QtWidgets.QFileDialog.getOpenFileName(self,caption='Select a template preset to load', filter='XML Files (*.xml)')
            fn = path[0]
            if fn == '':
                return
        if not os.path.isfile(fn):
            logging.error('File not found: {}'.format(fn))
            raise FileNotFoundError(fn)

        self.cleanup()

        ret = self.xmlfp.read(fn)
        if ret is None:
            return False
        (self.tree, self.hashwarning, self.compat, chash) = ret

        # Apply to UI, then apply UI to tree - to check if content hash after saving without changes will be identical
        self.checkBGWLfield()
        self.displayTreetoGUI()
        self.UItoTree(True)
        newhash = self.xmlfp.get_contenthash(self.tree)
        if newhash != chash:
            logging.error('Consistency error: Preset Editor changes content hash - please check template.')
            return False

        self.loadeddata = True
        self.tabWidget.setEnabled(True)
        self.groupBox_5.setEnabled(True)
        self.contentHashBox.setText(chash)

        return True

    def checkBGWLfield(self):
        """ check if the BGWavelength entry is found in xml file, disable gui element if not"""
        f = self.tree.find('.//ViewingPresets//DataModelViewingPreset//BgWavelength')
        if f is None:
            self.bgfound = False
            self.bgWavelength.setEnabled(False)
            self.bgWavelength.addItem('Not defined')
            self.bgWavelength.setCurrentText('Not defined')
            self.bgWavelength.setToolTip('Was not found \ncan be set manually')
            self.bgWavelength.setStyleSheet('color : rgb(120, 120, 120)')
            self.bgwllabel.setStyleSheet('color : rgb(120, 120, 120)')
        else:
            self.bgfound = True
            self.bgWavelength.setEnabled(True)
            self.bgWavelength.removeItem(self.bgWavelength.findText('Not defined'))
            self.bgWavelength.setToolTip('')
            self.bgWavelength.setStyleSheet('color: #cccccc')
            self.bgwllabel.setStyleSheet('color: #cccccc')
        
            
    def writexmlFile(self):
        """apply changes to lxml tree and then write it""" 

        if self.tree is None:
            return

        if self.appscientistname.text() =='':
            msg = QtWidgets.QMessageBox()
            msg.setText('Insert the Application Scientist Name')
            msg.exec()
            return
        
        # path = QtWidgets.QFileDialog.getSaveFileName(self,directory=self.presetIDBox.text(), filter='XML Files (*.xml)')
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if path == '':
            return
        # === Construct the filename
        path += '/' + self.presetIDBox.text().split('#')[0]
        path += '_v' + self.versionTextBox.text()
        date = datetime.datetime.now()
        c ='{:04d}{:02d}{:02d}'.format(date.year, date.month, date.day) 
        path += '_' +c
        path += '_' + self.appscientistname.text()
        path += '.xml'

        # ====== Warning for Overwriting =========
        if os.path.isfile(path):
            qm = QtWidgets.QMessageBox
            ret = qm.question(self,'', "File already exists \n Overwrite?", qm.Yes | qm.No)
            if ret == qm.No:
                return

        # Write XML
        chash = self.xmlfp.write(
            self.tree, 
            path, 
            version=self.version, 
            compat=self.compat, 
            initials=self.appscientistname.text(), 
            presetversion=self.versionTextBox.text()
        )

        # Update content Hash to Excel
        self.excel_dict.update({'Hash':  chash})
        ExcelExporter.writeToExcel(path, self.excel_dict, chash)

    @QtCore.pyqtSlot()
    def UItoTree(self, force=False):

        if (not self.loadeddata or self.muted) and not force:
            return

        sender = self.sender()
        if sender is not None:
            logging.debug('Element triggered a Tree change: {} ({})'.format(sender.objectName(), sender))

        excel_dict = dict()

        excel_dict.update({'Scientist': self.appscientistname.text()})

        # ====== General Information ===========
        self.tree.find('.//PresetType').text = self.PresetType.text()
        excel_dict.update({'PresetType': self.PresetType.text()})
        self.tree.xpath('./DataModelStudyPreset/Name')[0].text = self.nameBox.text()
        excel_dict.update({'Name in ViewMSOTc': self.nameBox.text()})
        self.tree.xpath('./DataModelStudyPreset/PresetIdentifier')[0].text = self.presetIDBox.text()
        excel_dict.update({'Preset ID': self.presetIDBox.text()})
        self.tree.xpath('./DataModelStudyPreset/CompatibleDetectorGUID')[0].text = self.detectorBox.text()
        excel_dict.update({'Detector': self.detectorBox.text()})
        self.tree.xpath('./DataModelStudyPreset/PresetVersion')[0].text = self.versionTextBox.text()
        excel_dict.update({'PresetVersion':  self.versionTextBox.text()})
        

    
        # ====== Acquisition Tab =======
        self.tree.find('.//DisplayAllWavelengths').text = str(self.displayAllWLBox.isChecked()).lower()
        excel_dict.update({'Cycle Wavelengths':  str(self.displayAllWLBox.isChecked()).lower()})
        self.tree.find('.//USVisible').text = str(self.usvisibleBox.isChecked()).lower()
        excel_dict.update({'Show Ultrasound':  str(self.usvisibleBox.isChecked()).lower()})
        self.tree.find('.//PreferredBackgroundWL').text = self.prefWLBox.currentText()
        excel_dict.update({'Preferred Wavelength':  self.prefWLBox.currentText()})

        # ====== Processing Tab ==========
        self.tree.find('.//UserSoundTrim').text = str(self.userSoundBox.value())
        excel_dict.update({'Speed of Sound':  str(self.userSoundBox.value())})
        self.tree.find('.//FRAMECORRTHRES').text = str(self.SFAFrameThreshBox.value())
        excel_dict.update({'SFA Frame Threshold':  str(self.SFAFrameThreshBox.value())})
        self.tree.find('.//BackgroundAbsorption').text = str(self.backgroundAbsorptionBox.value())
        excel_dict.update({'BackgroundAbsorption':  str(self.backgroundAbsorptionBox.value())})
        self.tree.find('.//BackgroundOxygenation').text = str(self.backgroundOxyBox.value())
        excel_dict.update({'BackgroundOxygenation':  str(self.backgroundOxyBox.value())})
        self.tree.find('.//MAXAVERAGES').text = str(self.maxavgframes.value())
        excel_dict.update({'Max Averaged Frames':  str(self.maxavgframes.value())})
        self.tree.find('.//MAXPASTSWEEPS').text = str(self.sfabuffersize.value())
        excel_dict.update({'SFA Buffer Size':  str(self.sfabuffersize.value())})
        # self.tree.find('.//BgWavelength').text = self.bgWL.currentText()
        
        # ====== Visualization Tab =======
        self.tree.find('.//IsMultipleMspLivePreviewEnabled').text = str(self.enableMultiPanel.isChecked()).lower()
        excel_dict.update({'enable MultiPanel':  str(self.enableMultiPanel.isChecked()).lower()})

        # Selected Wavlengeth List, delete all and current
        wlset = self.tree.find('.//WavelengthSet/Items')

        for wl in wlset:
            wl.getparent().remove(wl)
        wavelengths = ""

        for x in range(0, self.WLList.count()):
            e = etree.Element('double')
            e.text = self.WLList.item(x).text()
            wavelengths +=  self.WLList.item(x).text() +', '
            wlset.append(e)         
        wlset.text = None

        excel_dict.update({'Wavelengths':  wavelengths})  
        
        
        # write spectra/ first remove existing data in xml, write new list
        spectra = self.tree.find('.//UserSelectedSpectra')

        for child in spectra:
            child.getparent().remove(child)

        spectraString = ""

        for s in self.spectralist:
            e = etree.Element('string')
            e.text = s
            spectraString += s + ", "
            spectra.append(e)

        excel_dict.update({'Spectra':  spectraString})  

        # change view settings
        viewingpresets = self.tree.find('.//ViewingPresets')
        #print(etree.tostring(viewingpresets))
        views = viewingpresets.findall('.//DataModelViewingPreset')

        

        showedwarning = None

        #get all layers for all views
        for i in range(0, len(views)):

            # ===== Write Settings of each View ===============
            v = views[i]
            viewString = ViewEnum(i).name+' View'
            s = self.viewsettings[i]
            v.find('.//AutoScaling').text = str(s.autoscaling).lower()
            excel_dict.update({viewString+' AutoScaling':  str(s.autoscaling).lower()})  
            v.find('.//UltrasoundMinimumScaling').text = str(s.usscalingmin)
            excel_dict.update({viewString+' UltrasoundMinimumScaling':  str(s.usscalingmin)})  
            v.find('.//UltrasoundMaximumScaling').text = str(s.usscalingmax)
            excel_dict.update({viewString+' UltrasoundMaximumScaling':  str(s.usscalingmax)})  
            v.find('.//BackgroundMinimumScaling').text = str(s.backgroundscalingmin)
            excel_dict.update({viewString+' BackgroundMinimumScaling':  str(s.backgroundscalingmin)})  
            v.find('.//BackgroundMaximumScaling').text = str(s.backgroundscalingmax)
            excel_dict.update({viewString+' BackgroundMaximumScaling':  str(s.backgroundscalingmax)})  
            v.find('.//ForegroundMinimumScaling').text = str(s.foregroundscalingmin)
            excel_dict.update({viewString+' ForegroundMinimumScaling':  str(s.foregroundscalingmin)})  
            v.find('.//ForegroundMaximumScaling').text = str(s.foregroundscalingmax)
            excel_dict.update({viewString+' ForegroundMaximumScaling':  str(s.foregroundscalingmax)})  
            if self.bgfound:
                v.find('.//BgWavelength').text = str(s.bgWL)
                excel_dict.update({viewString+' BgWavelength':  str(s.bgWL)})  


            # ===================================================

            #get  layers for each view
            layers = views[i].findall('.//DataModelImagingLayer')

            

            # set for spectra
            sset = set(self.spectralist)  # set to determine new layers
            sset |= set(self.originalSpectra)
            # Hb settings in this layer for blueprint of new layers
            hbdummy = None

            panelString =''

            for j in range(0, len(layers)):

                spectrum = layers[j].find('.//ComponentTagIdentifier')
                #delete from xml if not found in settings
                found = False

                for k in range(0, len(self.viewlist[i])):
                    if self.viewlist[i][k].spectrum == spectrum.text:
                        panelString = spectrum.text
                        found = True
                        sset.remove(spectrum.text)
                        s = self.viewlist[i][k]
                        p = spectrum.getparent()
                        p.find('.//GainMax').text = str(s.maxthresh)
                        excel_dict.update({viewString+' '+ panelString+ ' '+ 'Upper Threshold':  str(s.maxthresh)}) 
                        p.find('.//GainMin').text = str(s.minthresh)
                        excel_dict.update({viewString+' '+ panelString+ ' '+ 'Lower Threshold':  str(s.minthresh)})
                        p.find('.//Semitransparent').text = str(s.transparent).lower()
                        excel_dict.update({viewString+' '+ panelString+ ' '+ 'Transparency':  str(s.transparent).lower()})
                        p.find('.//Visible').text = str(s.visible).lower()
                        excel_dict.update({viewString+' '+ panelString+ ' '+ 'Visible':  str(s.visible).lower()})
                        p.find('.//PaletteType').text = str(s.palette)
                        excel_dict.update({viewString+' '+ panelString+ ' '+ 'PaletteType':  str(s.palette)})
                        p.find('.//LogarithmicScaling').text = str(s.logarithmic).lower()
                        excel_dict.update({viewString+' '+ panelString+ ' '+ 'LogarithmicScaling':  str(s.logarithmic).lower()})
                        p.find('.//Load').text = str(s.load).lower()
                        excel_dict.update({viewString+' '+ panelString+ ' '+ 'Load':  str(s.load).lower()})


                        if spectrum.text == 'Hb':
                            hbdummy = deepcopy(spectrum.getparent())

                        break

                if not found:
                    p = spectrum.getparent()
                    p.getparent().remove(p)

            # add new spectra to xml
            if hbdummy is None and sset:
                if not showedwarning:
                    msg = QtWidgets.QMessageBox()
                    msg.setText('Cannot create new spectra, because of no Hb template')
                    msg.exec()
                    showedwarning = True
            else:
                for item in sset:
                    for k in range(0, len(self.viewlist[i])):
                        if self.viewlist[i][k].spectrum == item:
                            s = self.viewlist[i][k]
                            panelString = item
                            # TODO: Why is here no load, or pallette type, logrithmicscaling?
                            hbdummy.find('.//ComponentTagIdentifier').text = item
                            excel_dict.update({viewString+' '+ panelString+' '+ 'ComponentTagIdentifier':  item}) 
                            hbdummy.find('.//GainMax').text = str(s.maxthresh)
                            excel_dict.update({viewString+' '+ panelString+' '+  'Upper Threshold':  str(s.minthresh)})
                            hbdummy.find('.//GainMin').text = str(s.minthresh)
                            excel_dict.update({viewString+' '+ panelString+ ' '+ 'Lower Threshold':  str(s.minthresh)})
                            hbdummy.find('.//Semitransparent').text = str(s.transparent).lower()
                            excel_dict.update({viewString+' '+ panelString+ ' '+ 'Transparency':  str(s.transparent).lower()})
                            hbdummy.find('.//Visible').text = str(s.visible).lower()
                            excel_dict.update({viewString+' '+ panelString+ ' '+ 'Visible':  str(s.visible).lower()})
                            layers[0].getparent().append(hbdummy)
                            hbdummy = deepcopy(hbdummy)

        self.excel_dict = excel_dict
        self.generatePresetID()

    def toggleMultiPanel(self, **kwargs):
        """ toggle Multipanel Option to state(True, False)"""

        if 'state' in kwargs: 
            self.enableMultiPanel.setChecked(kwargs['state'])
        if not self.enableMultiPanel.isChecked():
            
            self.radioButtons[0].setChecked(True)
            self.radioButtons[1].setCheckable(False)
            self.radioButtons[1].setStyleSheet('color : rgb(120, 120, 120)')
            self.radioButtons[2].setCheckable(False)
            self.radioButtons[2].setStyleSheet('color : rgb(120, 120, 120)')
            self.radioButtons[3].setCheckable(False)
            self.radioButtons[3].setStyleSheet('color : rgb(120, 120, 120)')
            self.applySettings()

        else:
            self.radioButtons[1].setCheckable(True)
            self.radioButtons[1].setStyleSheet('color: #cccccc')
            self.radioButtons[2].setCheckable(True)
            self.radioButtons[2].setStyleSheet('color: #cccccc')
            self.radioButtons[3].setCheckable(True)
            self.radioButtons[3].setStyleSheet('color: #cccccc')

        self.UItoTree()
            
        

    def addWavelength(self):
        """ add Wavelength to the Wavelength Set, opens a new Dialog"""
        AddWLDialog = QtWidgets.QDialog()
        ui = Ui_AddWLDialog()
        ui.setupUi(AddWLDialog)
        if AddWLDialog.exec():
            
            q = QtWidgets.QListWidgetItem()
            q.setData(0, ui.spinBox.value())
            self.WLList.addItem(q)

            p = bisect.bisect_left(self.sortedwvlist, ui.spinBox.value())
            bisect.insort_left(self.sortedwvlist,ui.spinBox.value())


            
            self.prefWLBox.insertItem(p, str(ui.spinBox.value()))
            self.bgWavelength.insertItem(p, str(ui.spinBox.value()))
            # self.bgWL.addItem(str(ui.spinBox.value()))

            self.UItoTree()

        
    def removeWavelength(self):
        """ remove selected Wavelength from the Wavelength Set and from the PrefferedWL Combobox"""
        # 
        try :
            t = self.WLList.takeItem(self.WLList.currentRow()).text()
            self.prefWLBox.removeItem(self.prefWLBox.findText(t))
            self.bgWavelength.removeItem(self.bgWavelength.findText(t))
            self.sortedwvlist.remove(int(t))

            self.UItoTree()
        except AttributeError:
            # if there is no element in the list
            pass

    def displayTreetoGUI(self):
        """ Update the GUI  with the information in the xml file"""

        self.muted = True  # Prevents execution of ID generation

        # ====== General Information =============
        self.PresetType.setText(self.tree.find('.//PresetType').text)
        self.nameBox.setText(self.tree.find('.//Name').text)
        self.presetIDBox.setText(self.tree.find('.//PresetIdentifier').text)
        self.versionTextBox.setText(self.tree.find('//PresetVersion').text)
        self.detectorBox.setText(self.tree.find('.//CompatibleDetectorGUID').text)

        # ======== Acquisition Tab ===========
        self.displayAllWLBox.setChecked(self.tree.find('.//DisplayAllWavelengths').text == 'true')
        self.usvisibleBox.setChecked(self.tree.find('.//USVisible').text == 'true')
        wlset = self.tree.find('.//WavelengthSet/Items')
        for wl in wlset:
            # dont include comments by casting 
            try:
                w = (str(int(wl.text)))
                q = QtWidgets.QListWidgetItem()
                q.setData(0, int(w))
                p = bisect.bisect_left(self.sortedwvlist, int(w))
                bisect.insort_left(self.sortedwvlist, int(w))
                self.WLList.addItem(q)
                self.prefWLBox.addItem(w)
                self.bgWavelength.addItem(w)
                # self.bgWL.addItem(w)
            except ValueError:
                pass
        # Disable multispectral features for single WL presets (otherwise no layer template exists)
        multispectral = not len(self.WLList) == 1
        self.addWL.setEnabled(multispectral)
        self.removeWL.setEnabled(multispectral)
        self.addButton.setEnabled(multispectral)
        self.deleteButton.setEnabled(multispectral)

        # ========= Processing Tab ===========
        self.userSoundBox.setValue(int(self.tree.find('.//UserSoundTrim').text))
        self.SFAFrameThreshBox.setValue(float(self.tree.find('.//FRAMECORRTHRES').text))
        self.backgroundAbsorptionBox.setValue(float(self.tree.find('.//BackgroundAbsorption').text))
        self.backgroundOxyBox.setValue(int(self.tree.find('.//BackgroundOxygenation').text))
        self.maxavgframes.setValue(int(self.tree.find('.//MAXAVERAGES').text))
        self.sfabuffersize.setValue(int(self.tree.find('.//MAXPASTSWEEPS').text))
        # self.bgWL.setCurrentText(self.tree.find('.//BgWavelength').text)



        self.prefWLBox.setCurrentText(self.tree.find('.//PreferredBackgroundWL').text)
        # ===============Visualization Tab==================
        
        self.getViewingPresets()
        spectra = self.tree.find('.//UserSelectedSpectra')
        # self.defaultspectra = ['OPUS', 'Background']
        #print(etree.tostring(spectra))
        for children in spectra:
            #print(children.text)
            self.spectralist.append(children.text)

        self.selectedList.addItems(self.spectralist)
        self.addSpectratoViewPanel()

        self.unselectedspectra = list(set(self.allspectra)-set(self.spectralist))
        self.unselectedList.clear()
        self.unselectedList.addItems(self.unselectedspectra)

        #self.viewSpectraList.SelectItems(0)

        self.enableMultiPanel.setChecked(self.tree.find('.//IsMultipleMspLivePreviewEnabled').text =='true')

        self.disableMultipanel()  # disable multipanel if preset is 3D

        # If no panel is activated, activate the first one
        k = -1
        for i in range(0, len(self.radioButtons)):
            if self.radioButtons[i].isChecked():
                k = i
                break
        if k == -1:
            self.view1Button.setChecked(True)
        # If no layer is selected, select the first one
        row = self.viewSpectraList.currentRow()
        if row == -1:
            self.viewSpectraList.setCurrentRow(0)
        self.applySettings(True)  # Make sure the new tree propagates to view settings, also unmutes

        # self.muted = False  # Prevents execution of ID generation

        self.generatePresetID()


    def addSpectratoViewPanel(self):
        """ Add the spectra into the view panels in the visualization tab"""
        
        for idx, val  in enumerate(self.viewlist[0]):
            self.viewSpectraList.addItem(self.viewlist[0][idx].spectrum)
            self.originalSpectra = self.originalSpectra + [self.viewlist[0][idx].spectrum]




    def disableMultipanel(self):
        """ disable Multipanel if 3D is enabled == 3D depth is greater than 1"""
        
        if int(self.tree.find('.//Nz').text) > 1 or len(self.viewsettings) == 1:

            self.enableMultiPanel.setStyleSheet('color : rgb(120, 120, 120)')
            self.enableMultiPanel.setToolTip('Multipanel disabled for Dual-Panel templates and 3D presets ')
            self.enableMultiPanel.setEnabled(False)

        else:
            self.enableMultiPanel.setEnabled(True)
            self.enableMultiPanel.setToolTip('')
            self.enableMultiPanel.setStyleSheet('color: #cccccc')



        
    def generatePresetID(self):
        """ auto generate PresetID """
        if not self.loadeddata or self.muted:
            return

        text = self.detectorBox.text()
        text += '_' + self.nameBox.text()

        for s in self.spectralist:
            text += '_' + s

        for s in self.viewlist[0]:
            if s.spectrum == 'OPUS':
                if s.load:
                    text += '_' + 'US'
                break


        if self.enableMultiPanel.isChecked():
            text += '_' + 'MP'
        else:
            text += '_' + 'SP'

        chash = self.xmlfp.get_contenthash(self.tree)
        text += '#' + chash
        
        self.presetIDBox.setText(text)
        self.contentHashBox.setText(chash)
        self.contentHashChanged.emit(chash)




    def cleanup(self):
        """ clean GUI, called before reading a new file"""
        self.selectedList.clear()
        self.WLList.clear()
        
        # self.bgWL.clear()
        self.prefWLBox.clear()
        self.bgWavelength.clear()
        self.viewSpectraList.clear()
        # self.viewSpectraList.addItems(self.defaultspectra)
        self.spectralist.clear()
        self.unselectedspectra = self.allspectra
        self.viewlist.clear()
        self.originalSpectra = []


    def getViewingPresets(self):
        """get the presets of the layer for each of the four view panels
        and get the settings of each view"""

        try:
            viewingpresets = self.tree.find('.//ViewingPresets')
            #print(etree.tostring(viewingpresets))
            views = viewingpresets.findall('.//DataModelViewingPreset')
        except AttributeError:
            msg = QtWidgets.QMessageBox()
            msg.setText('Support only for Multipanel Views')
            msg.exec_()
            sys.exit(-1)

        #get all settings for all views
        self.viewsettings.clear()
        for i in range(0, len(views)):
            
            # === get the Settings of each view panel =====
            autosc = views[i].find('.//AutoScaling').text == 'true'
            usmin = views[i].find('.//UltrasoundMinimumScaling').text
            usmax = views[i].find('.//UltrasoundMaximumScaling').text
            bgmin = views[i].find('.//BackgroundMinimumScaling').text
            bgmax = views[i].find('.//BackgroundMaximumScaling').text
            foremin = views[i].find('.//ForegroundMinimumScaling').text
            foremax = views[i].find('.//ForegroundMaximumScaling').text
            if self.bgfound:
                bgWl = views[i].find('.//BgWavelength').text
            else:
                bgWl = 0
            self.viewsettings.append(ViewSettings(autosc, usmin, usmax, bgmin, bgmax, foremin, foremax, bgWl))
            # print('View '+str(i)+'\n'+str(self.viewsettings[i])+'\n')





            settings = []

            #get settings for all layers
            layers = views[i].findall('.//DataModelImagingLayer')

            for j in range(0, len(layers)):

                spectrum = layers[j].find('.//ComponentTagIdentifier').text
                colormap = layers[j].find('.//PaletteType').text
                load = layers[j].find('.//Load').text == 'true'
                lgsc = layers[j].find('.//LogarithmicScaling').text == 'true'

                visible = layers[j].find('.//Visible').text == 'true' 

                #print(layers[j].find('.//Visible').text)

                #print(layers[j].find('.//Semitransparent').text)


                transparent = (layers[j].find('./Semitransparent').text) == 'true' 

                mint = float(layers[j].find('.//GainMin').text)

                maxt = float(layers[j].find('.//GainMax').text)


                #add to settings of this view
                settings.append(LayerSetting(spectrum, colormap,load,lgsc, visible, transparent, mint, maxt))


            # add the list of one view to the complete list
            self.viewlist.append(settings)


    def applySettings(self, force=False):
        """update gui with settings according to the current selected item"""
        # get selected view

        if not self.loadeddata and not force:
            return

        k = 0
        for i in range(0, len(self.radioButtons)):
            if self.radioButtons[i].isChecked():
                k = i
                break

        # apply current view settings
        self.muted = True
        cv = self.viewsettings[k]
        self.autoScalingCheck.setChecked(cv.autoscaling)
        self.usmin.setText(cv.usscalingmin)
        self.usmax.setText(cv.usscalingmax)
        self.bgmin.setText(cv.backgroundscalingmin)
        self.bgmax.setText(cv.backgroundscalingmax)
        self.fgmin.setText(cv.foregroundscalingmin)
        self.fgmax.setText(cv.foregroundscalingmax)
        if self.bgfound:
            self.bgWavelength.setCurrentText(str(cv.bgWL))


        # get selected spectrum
        if self.viewSpectraList.count() == 0:
            self.muted = False
            return

        selected = self.viewSpectraList.currentItem()

        # when no panel is selected (first call) select the first index
        if selected is not None:
            #pprint(selected.text())
            selected = selected.text()

        else:
            selected = self.viewSpectraList.item(0).text()
            self.viewSpectraList.setCurrentRow(0)

        #print('View:'+ str(i)+ selected)
        settings = self.viewlist[k]

        for i in range(0, len(settings)):
            #pprint(selected)
            if settings[i].spectrum == selected:
                s = settings[i]
                self.paletteType.setCurrentText(s.palette)
                self.loadCheck.setChecked(s.load)
                self.logarithmicScalingCheck.setChecked(s.logarithmic)
                self.visibleCheck.setChecked(s.visible)
                self.transparentCheck.setChecked(s.transparent)
                self.minBox.setValue(s.minthresh)
                self.maxBox.setValue(s.maxthresh)

                # self.generatePresetID()
                self.muted = False
                return

    def addspectra(self):
        """called when addButton is clicked; removes selected spectrum 
        from unselected list, adds it to the selected list and 
        create default ViewSetting object of it for all views
        """

        #remove from unselected list and view and add to list and view
        row = self.unselectedList.currentRow()
        if row == -1:
            return
        item = self.unselectedList.takeItem(row)
        self.selectedList.addItem(item)
        self.spectralist.append(item.text())
        self.unselectedspectra.remove(item.text())
        # an item can only belong to one widget at a time
        self.viewSpectraList.addItem(item.text())
        # pprint(item)

        # add viewsettings object for the new spectrum for each view
        new = [LayerSetting(item.text()),LayerSetting(item.text()),LayerSetting(item.text()),LayerSetting(item.text())]

        for i in range(0, len(self.viewlist)):
            self.viewlist[i].append(new[i])

        self.UItoTree()

    def removespectra(self):
        """remove item from selected list and add it to unselected list,
         is called when deleteButton is pressed"""
        row = self.selectedList.currentRow()
        if row == -1:
            return
        item = self.selectedList.takeItem(row)
        self.unselectedList.addItem(item)
        self.spectralist.remove(item.text())
        self.unselectedspectra.append(item.text())
        # find Spectra to be removed in Spectralist and remove it
        match = self.viewSpectraList.findItems(item.text(), QtCore.Qt.MatchExactly)
        r = self.viewSpectraList.row(match[0])
        self.viewSpectraList.takeItem(r)

        # remove settingsobject"
        for i in range(0, len(self.viewlist)):
            for j in range(0, len(self.viewlist[i])):
                if self.viewlist[i][j].spectrum == item.text():
                    del self.viewlist[i][j]
                    break

        self.UItoTree()
    
    @QtCore.pyqtSlot()
    def changeViewSettings(self):
        """ save changes to viewsettings object, called after modifying the the settings in the view settings box """
        if not self.loadeddata:
            return
        view = 0
        for i in range(0, len(self.radioButtons)):
            if self.radioButtons[i].isChecked():
                view = i
                break

        v = self.viewsettings[view]

        v.autoscaling = self.autoScalingCheck.isChecked()
        v.backgroundscalingmin = self.bgmin.text()
        v.backgroundscalingmax = self.bgmax.text()
        v.usscalingmin = self.usmin.text()
        v.usscalingmax = self.usmax.text()
        v.foregroundscalingmin = self.fgmin.text()
        v.foregroundscalingmax = self.fgmax.text()
        if self.bgfound:
            v.bgWL = self.bgWavelength.currentText()

        self.UItoTree()
        
    @QtCore.pyqtSlot()
    def changeLayerSettings(self):
        """ save the changes made in the gui to the LayerSettings object,
        called by clicking Visible/Transparent checkboxes
        and changing the threshold
        """
        if self.muted:
            return

        row = self.viewSpectraList.currentRow()
        if row == -1:
            return

        item = self.viewSpectraList.item(row)

        view = 0
        for i in range(0, len(self.radioButtons)):
            if self.radioButtons[i].isChecked():
                view = i
                break

        for j in range(0, len(self.viewlist[view])):
            if self.viewlist[view][j].spectrum == item.text():
                s = self.viewlist[view][j]
                s.visible = self.visibleCheck.isChecked()
                s.transparent = self.transparentCheck.isChecked()
                s.minthresh = self.minBox.value()
                s.maxthresh = self.maxBox.value()
                s.load = self.loadCheck.isChecked()
                s.logarithmic = self.logarithmicScalingCheck.isChecked()
                s.palette = self.paletteType.currentText()
                break

        self.UItoTree()



def handle_error(exctype, val, trace):
    logging.debug('Critical Error Occurred', exc_info=(exctype, val, trace))
    logging.critical(str(val), exc_info=(exctype, val, trace))
    sys.exit(1)

if __name__ == '__main__':

    # sys.stdout = open('log.txt', 'w')

    app = QtWidgets.QApplication(sys.argv)

    # Log to console with debug level - largely for debugging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    consolehandler = logging.StreamHandler(sys.stdout)
    consolehandler.setLevel(logging.DEBUG)
    consolehandler.setFormatter(formatter)
    logger.addHandler(consolehandler)

    # Always log to file with DEBUG level
    logdir = os.path.join(
        os.environ['APPDATA'], 
        'iThera', 
        'PresetEditor'
    )
    if not os.path.isdir(logdir):
        os.mkdir(logdir)
    logfn = os.path.join(
        logdir,
        'log_' + QtCore.QDateTime(datetime.datetime.now()).toString("yyyy-MM-dd_HH-mm-ss") + '.log'
    )
    logging.info('Logging to {}'.format(logfn))
    filehandler = logging.FileHandler(logfn)
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    # Log to UI for warnings and errors
    hand = ErrorLogHandler()
    formatter2 = logging.Formatter('%(levelname)s - %(message)s')
    hand.setFormatter(formatter2)
    logger.addHandler(hand)

    # Exception handler
    sys.excepthook = handle_error

    ''' style = 'iLabs.css'

    with open(style, mode='r') as ss:
        app.setStyleSheet(ss.read()) '''

    # f = open('log.txt', 'w')
    
    prog = PresetEditor()
    exitcode=app.exec_()
    
    #     f.write(e)
    
    sys.exit(exitcode)
