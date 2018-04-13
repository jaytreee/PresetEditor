"""
qt designer test
"""
# pylint: disable=E1101
# pylint: disable=C0103

import sys
import datetime
import os
import uuid
import subprocess, re
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

from addWavelengthDialog import Ui_AddWLDialog
from schemamanager import iXMLSchemaManager





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

    settingslist = [[], [], [], []]
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

    def __init__(self):
        super(PresetEditor, self).__init__()
        self.setupUi(window)

        self.connectGUItoFunctionalty()

        self.schemamanager = iXMLSchemaManager()
        self.schemamanager.main()

        self.typechecker = ScalingValidator(0, 1, 5, None, -1)

        self.loadxmlFile()

        self.displayVersion()


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

        self.nameBox.textChanged.connect(self.generateGUID)

        self.addButton.clicked.connect(self.addspectra)
        self.deleteButton.clicked.connect(self.removespectra)

        self.visibleCheck.clicked.connect(self.changeSettings)
        self.loadCheck.clicked.connect(self.changeSettings)
        self.logarithmicScalingCheck.clicked.connect(self.changeSettings)
        self.paletteType.activated.connect(self.changeSettings)
        self.transparentCheck.clicked.connect(self.changeSettings)
        self.minBox.editingFinished.connect(self.changeSettings)
        self.maxBox.editingFinished.connect(self.changeSettings)
        
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

            with open('source/version.txt') as f:
                v = str(f.read()).strip()

            hgoutput = subprocess.run(['hg','id','-n'], stdout=subprocess.PIPE)
            hgoutput = hgoutput.stdout.decode('utf-8').strip()
            match = re.search('^([0-9]+)(\+)?$', hgoutput)

            rev = match.group(1)

        self.version = 'v'+v+ '-rev'+rev
        self.statusbar.showMessage(self.version)

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


    def generateGUID(self):
        """gernerate GUID from the Preset Name"""
        hash = uuid.uuid5(uuid.NAMESPACE_DNS,self.nameBox.text())
        self.PresetIDTextBox.setText(str(hash))

    def loadxmlFile(self):
        """ load xml File """

        self.cleanup()

        if True:
            path = QtWidgets.QFileDialog.getOpenFileName(self,caption='Select a preset.xml file to modify', filter='XML Files (*.xml)')
            if not os.path.isfile(path[0]):
                return

        else:
            path = ['', '']
            path[0] = ('C:/Users/thomas.hartmann/Desktop/xml files/'
                       '256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml')
        #self.nameBox.setText(path[0])
        self.tree = self.xmlfp.read(path[0])

        '''  test = self.tree.find('.//CompatibleDetectorGUID')
        print(test.text)
        print(etree.tostring(test))
        print(test.tag) '''

        self.loadeddata = True

        #check for newest version, find fields
        self.checkBGWLfield()

        self.displayTreetoGUI()


        #pprint(self.settingslist)

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

        path = QtWidgets.QFileDialog.getSaveFileName(self,directory=self.presetIDBox.text(), filter='XML Files (*.xml)')

        if path[0] == '':
            return
        # ====== General Information ===========
        self.tree.find('.//PresetType').text = self.PresetType.text()
        self.tree.xpath('./DataModelStudyPreset/Name')[0].text = self.nameBox.text()
        self.tree.xpath('./DataModelStudyPreset/PresetIdentifier')[0].text = self.presetIDBox.text()
        self.tree.xpath('./DataModelStudyPreset/CompatibleDetectorGUID')[0].text = self.detectorBox.text()
        self.tree.xpath('./DataModelStudyPreset/PresetVersion')[0].text = self.versionTextBox.text()
      
    
        # ====== Acquisition Tab =======
        self.tree.find('.//DisplayAllWavelengths').text = str(self.displayAllWLBox.isChecked()).lower()
        self.tree.find('.//USVisible').text = str(self.usvisibleBox.isChecked()).lower()
        self.tree.find('.//PreferredBackgroundWL').text = self.prefWLBox.currentText()

        # ====== Processing Tab ==========
        self.tree.find('.//UserSoundTrim').text = str(self.userSoundBox.value())
        self.tree.find('.//FRAMECORRTHRES').text = str(self.SFAFrameThreshBox.value())
        self.tree.find('.//BackgroundAbsorption').text = str(self.backgroundAbsorptionBox.value())
        self.tree.find('.//BackgroundOxygenation').text = str(self.backgroundOxyBox.value())
        self.tree.find('.//MAXAVERAGES').text = str(self.maxavgframes.value())
        self.tree.find('.//MAXPASTSWEEPS').text = str(self.sfabuffersize.value())
        # self.tree.find('.//BgWavelength').text = self.bgWL.currentText()
        
        # ====== Visualization Tab =======
        self.tree.find('.//IsMultipleMspLivePreviewEnabled').text = str(self.enableMultiPanel.isChecked()).lower()
        
        # Selected Wavlengeth List, delete all and current
        wlset = self.tree.find('.//WavelengthSet/Items')

        for wl in wlset:
            wl.getparent().remove(wl)
        
        for x in range(0, self.WLList.count()):
            e = etree.Element('double')
            e.text = self.WLList.item(x).text()
            wlset.append(e)         
        wlset.text = None

          
        
        
        # write spectra/ first remove existing data in xml, write new list
        spectra = self.tree.find('.//UserSelectedSpectra')

        for child in spectra:
            child.getparent().remove(child)

        for s in self.spectralist:
            e = etree.Element('string')
            e.text = s
            spectra.append(e)

        # change view settings
        viewingpresets = self.tree.find('.//ViewingPresets')
        #print(etree.tostring(viewingpresets))
        views = viewingpresets.findall('.//DataModelViewingPreset')

        

        showedwarning = None

        #get all layers for all views
        for i in range(0, len(views)):

            # ===== Write Settings of each View ===============
            v = views[i]
            s = self.viewsettings[i]
            v.find('.//AutoScaling').text = str(s.autoscaling).lower()
            v.find('.//UltrasoundMinimumScaling').text = str(s.usscalingmin)
            v.find('.//UltrasoundMaximumScaling').text = str(s.usscalingmax)
            v.find('.//BackgroundMinimumScaling').text = str(s.backgroundscalingmin)
            v.find('.//BackgroundMaximumScaling').text = str(s.backgroundscalingmax)
            v.find('.//ForegroundMinimumScaling').text = str(s.foregroundscalingmin)
            v.find('.//ForegroundMaximumScaling').text = str(s.foregroundscalingmax)
            if self.bgfound:
                v.find('.//BgWavelength').text = str(s.bgWL)


            # ===================================================

            #get  layers for each view
            layers = views[i].findall('.//DataModelImagingLayer')

            

            # set for spectra
            sset = set(self.spectralist)  # set to determine new layers
            sset |= set(self.originalSpectra)
            # Hb settings in this layer for blueprint of new layers
            hbdummy = None

            for j in range(0, len(layers)):

                spectrum = layers[j].find('.//ComponentTagIdentifier')
                #delete from xml if not found in settings
                found = False

                for k in range(0, len(self.settingslist[i])):
                    if self.settingslist[i][k].spectrum == spectrum.text:
                        found = True
                        sset.remove(spectrum.text)
                        s = self.settingslist[i][k]
                        p = spectrum.getparent()
                        p.find('.//GainMax').text = str(s.maxthresh)
                        p.find('.//GainMin').text = str(s.minthresh)
                        p.find('.//Semitransparent').text = str(s.transparent).lower()
                        p.find('.//Visible').text = str(s.visible).lower()
                        p.find('.//PaletteType').text = str(s.palette)
                        p.find('.//LogarithmicScaling').text = str(s.logarithmic).lower()
                        p.find('.//Load').text = str(s.load).lower()


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
                    for k in range(0, len(self.settingslist[i])):
                        if self.settingslist[i][k].spectrum == item:
                            s = self.settingslist[i][k]
                            hbdummy.find('.//ComponentTagIdentifier').text = item
                            hbdummy.find('.//GainMax').text = str(s.maxthresh)
                            hbdummy.find('.//GainMin').text = str(s.minthresh)
                            hbdummy.find('.//Semitransparent').text = str(s.transparent).lower()
                            hbdummy.find('.//Visible').text = str(s.visible).lower()
                            layers[0].getparent().append(hbdummy)
                            hbdummy = deepcopy(hbdummy)


        c = 'Created with PresetEditor '+self.version
        date = datetime.datetime.now()
        c += ' on '+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+'-'+str(date.minute)+'-'+str(date.second)

        
        self.xmlfp.write(self.tree, path[0], comment=c)

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

        self.generatePresetID()
            
        

    def addWavelength(self):
        """ add Wavelength to the Wavelength Set, opens a new Dialog"""
        AddWLDialog = QtWidgets.QDialog()
        ui = Ui_AddWLDialog()
        ui.setupUi(AddWLDialog)
        if AddWLDialog.exec():
            
            q = QtWidgets.QListWidgetItem()
            q.setData(0, ui.spinBox.value())
            self.WLList.addItem(q)
            
            self.prefWLBox.addItem(str(ui.spinBox.value()))
            self.bgWavelength.addItem(str(ui.spinBox.value()))
            # self.bgWL.addItem(str(ui.spinBox.value()))

        
    def removeWavelength(self):
        """ remove selected Wavelength from the Wavelength Set and from the PrefferedWL Combobox"""
        # 
        try :
            t = self.WLList.takeItem(self.WLList.currentRow()).text()
            self.prefWLBox.removeItem(self.prefWLBox.findText(t))
            self.bgWavelength.removeItem(self.bgWavelength.findText(t))
            # self.bgWL.removeItem(self.prefWLBox.findText(t))
        except AttributeError:
            # if there is no element in the list
            pass

    def displayTreetoGUI(self):
        """ Update the GUI  with the information in the xml file"""


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
                self.WLList.addItem(q)
                self.prefWLBox.addItem(w)
                self.bgWavelength.addItem(w)
                # self.bgWL.addItem(w)
            except ValueError:
                pass

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

        #self.applySettings()

        self.generatePresetID()


    def addSpectratoViewPanel(self):
        """ Add the spectra into the view panels in the visualization tab"""
        
        for idx, val  in enumerate(self.settingslist[0]):
            self.viewSpectraList.addItem(self.settingslist[0][idx].spectrum)
            self.originalSpectra = self.originalSpectra + [self.settingslist[0][idx].spectrum]




    def disableMultipanel(self):
        """ disable Multipanel if 3D is enabled == 3D depth is greater than 1"""
        
        if int(self.tree.find('.//Nz').text) > 1:

            self.enableMultiPanel.setStyleSheet('color : rgb(120, 120, 120)')
            self.enableMultiPanel.setToolTip('Multipanel disabled when 3D Depth > 1 ')
            self.enableMultiPanel.setEnabled(False)

        else:
            self.enableMultiPanel.setEnabled(True)
            self.enableMultiPanel.setToolTip('')
            self.enableMultiPanel.setStyleSheet('color: #cccccc')



        
    def generatePresetID(self):
        """ auto generate PresetID """
        text = self.detectorBox.text()
        text += '_' + self.nameBox.text()

        for s in self.spectralist:
            text += '_' + s

        for s in self.settingslist[0]:
            if s.spectrum == 'OPUS':
                if s.load:
                    text += '_' + 'US'
                break


        if self.enableMultiPanel.isChecked():
            text += '_' + 'MP'
        else:
            text += '_' + 'SP'
        

        self.presetIDBox.setText(text)




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
        self.settingslist.clear()
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
            self.settingslist.append(settings)



    def applySettings(self):
        """update gui with settings according to the current selected item"""
        # get selected view

        if not self.loadeddata:
            return

        k = 0
        for i in range(0, len(self.radioButtons)):
            if self.radioButtons[i].isChecked():
                k = i
                break

        # apply current view settings
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
        settings = self.settingslist[k]

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
                print(s)

                # self.generatePresetID()
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

        for i in range(0, len(self.settingslist)):
            self.settingslist[i].append(new[i])

        self.generatePresetID()

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
        for i in range(0, len(self.settingslist)):
            for j in range(0, len(self.settingslist[i])):
                if self.settingslist[i][j].spectrum == item.text():
                    del self.settingslist[i][j]
                    break

        self.generatePresetID()
    
    def changeViewSettings(self):
        """ save changes to viewsettings object, called after modifying the the settings in the view settings box """
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



        print(v)
        
        
        

    def changeSettings(self):
        """ save the changes made in the gui to the LayerSettings object,
        called by clicking Visible/Transparent checkboxes
        and changing the threshold
        """

        row = self.viewSpectraList.currentRow()
        if row == -1:
            return

        item = self.viewSpectraList.item(row)

        view = 0
        for i in range(0, len(self.radioButtons)):
            if self.radioButtons[i].isChecked():
                view = i
                break

        for j in range(0, len(self.settingslist[view])):
            if self.settingslist[view][j].spectrum == item.text():
                s = self.settingslist[view][j]
                s.visible = self.visibleCheck.isChecked()
                s.transparent = self.transparentCheck.isChecked()
                s.minthresh = self.minBox.value()
                s.maxthresh = self.maxBox.value()
                s.load = self.loadCheck.isChecked()
                s.logarithmic = self.logarithmicScalingCheck.isChecked()
                s.palette = self.paletteType.currentText()
                print('View '+str(view))
                print(self.settingslist[view][j])
                break
        



if __name__ == '__main__':

    # sys.stdout = open('log.txt', 'w')

    app = QtWidgets.QApplication(sys.argv)


    ''' style = 'iLabs.css'

    with open(style, mode='r') as ss:
        app.setStyleSheet(ss.read()) '''

    window = QtWidgets.QMainWindow()
    # f = open('log.txt', 'w')
    
    prog = PresetEditor()

    window.show()
    

    exitcode=app.exec_()
    
    #     f.write(e)
    
    sys.exit(exitcode)
