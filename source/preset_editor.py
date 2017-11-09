"""
qt designer test
"""
# pylint: disable=E1101
# pylint: disable=C0103

import sys
import os
import uuid
from copy import deepcopy
#from pprint import pprint
from xmlfileparser import XmlFileParser
from lxml import etree
from PyQt5 import QtWidgets, QtCore
#from PyQt5.QtWidgets import QFileDialog
from preset_editor_gui import Ui_MainWindow
from viewsetting import ViewSetting

from addWavelengthDialog import Ui_AddWLDialog





class PresetEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Editor for Settings
    """
    tree = None

    defaultspectra = ['OPUS', 'Background']

    allspectra = []
    """ all available spectra"""

    spectralist = []
    """selected spectra"""

    unselectedspectra = list(set(allspectra)-set(spectralist))
    """ unselected spectra at the start"""

    fsf = 'C:\ProgramData\iThera\ViewMSOTc\Factory Spectra'
    """factory spectra folder"""

    settingslist = [[], [], [], []]
    """dimensions = #views; containing corresponing viewsetting objects """

    def __init__(self):
        super(PresetEditor, self).__init__()
        self.setupUi(window)

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
        self.viewSpectraList.clicked.connect(self.applySettings)

        self.nameBox.textChanged.connect(self.generateGUID)

        self.addButton.clicked.connect(self.addspectra)
        self.deleteButton.clicked.connect(self.removespectra)

        self.visibleCheck.clicked.connect(self.changeSettings)
        self.transparentCheck.clicked.connect(self.changeSettings)
        self.minBox.editingFinished.connect(self.changeSettings)
        self.maxBox.editingFinished.connect(self.changeSettings)
        

        self.radioButtons = [self.view1Button, self.view2Button, self.view3Button, self.view4Button]

        self.browseFactorySpectra.clicked.connect(self.changeFactorySpectra)

        self.loadFactorySpectra()
        self.unselectedspectra = list(set(self.allspectra)-set(self.spectralist))

        self.unselectedList.addItems(self.unselectedspectra)
        self.viewSpectraList.addItems(self.defaultspectra)

        #self.treeWidget.itemDoubleClicked.connect(self.setTreeItem)


    def changeFactorySpectra(self):
        """ opens Windows File Dialog, to select folder for the FactorySpectra"""
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.fsf))
        if not os.path.isdir(folder):
            return
        self.loadFactorySpectra(folder)
        self.unselectedspectra = list(set(self.allspectra)-set(self.spectralist))
        self.unselectedList.clear()
        self.unselectedList.addItems(self.unselectedspectra)
        # TODO: clean gui, settingslist from old settings, that are not avaiable now?



    def loadFactorySpectra(self, folder=fsf):
        """load Factory Spectra from folder (default:  C:\ProgramData\iThera\ViewMSOTc\Factory Spectra) and cuts file 
        extension. This is the allspectra list"""
        self.allspectra = os.listdir(folder)
        # cut fileextension
        for i, s in enumerate(self.allspectra):
            self.allspectra[i] = os.path.splitext(s)[0]

        self.FactorySpectraTextBox.setPlainText(folder)


    def generateGUID(self):
        """gernerate GUID from the Preset Name"""
        hash = uuid.uuid5(uuid.NAMESPACE_DNS,self.nameBox.toPlainText())
        self.PresetIDTextBox.setPlainText(str(hash))

    def loadxmlFile(self):
        """ load xml File """

        self.cleanup()

        if True:
            path = QtWidgets.QFileDialog.getOpenFileName(self, filter='XML Files (*.xml)')
            if not os.path.isfile(path[0]):
                return

        else:
            path = ['', '']
            path[0] = ('C:/Users/thomas.hartmann/Desktop/xml files/'
                       '256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml')
        #self.nameBox.setText(path[0])
        self.tree = XmlFileParser.read(self, path[0])

        '''  test = self.tree.find('.//CompatibleDetectorGUID')
        print(test.text)
        print(etree.tostring(test))
        print(test.tag) '''

        self.displayTreetoGUI()

        #pprint(self.settingslist)

    def writexmlFile(self):
        """apply changes to lxml tree and then write it"""

        if self.tree is None:
            return

        path = QtWidgets.QFileDialog.getSaveFileName(self, filter='XML Files (*.xml)')

        if path[0] == '':
            return
        # ====== General Information ===========
        self.tree.find('.//PresetType').text = self.presetTypeBox.currentText()
    
        # ====== Acquisition Tab =======
        self.tree.find('.//DisplayAllWavelengths').text = str(self.displayAllWLBox.isChecked()).lower()
        self.tree.find('.//USVisible').text = str(self.usvisibleBox.isChecked()).lower()
        self.tree.find('.//PreferredBackgroundWL').text = self.prefWLBox.currentText()

        # ====== Processing Tab ==========
        self.tree.find('.//UserSoundTrim').text = str(self.userSoundBox.value())
        self.tree.find('.//FRAMECORRTHRES').text = str(self.SFAFrameThreshBox.value())
        self.tree.find('.//BackgroundAbsorption').text = str(self.backgroundAbsorptionBox.value())
        self.tree.find('.//BackgroundOxygenation').text = str(self.backgroundOxyBox.value())
        
        
        # Selected Wavlengeth List, delete all and and current
        wlset = self.tree.find('.//WavelengthSet/Items')

        for wl in wlset:
            wl.getparent().remove(wl)
        
        for x in range(0, self.WLList.count()):
            e = etree.Element('double')
            e.text = self.WLList.item(x).text()
            wlset.append(e)         
        wlset.text = None
        self.tree.xpath('./DataModelStudyPreset/Name')[0].text = self.nameBox.toPlainText()
        self.tree.xpath('./DataModelStudyPreset/CompatibleDetectorGUID')[0].text = self.detectorBox.toPlainText()
        self.tree.xpath('./DataModelStudyPreset/PresetVersion')[0].text = self.versionTextBox.toPlainText()
        
        
        
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

            #get  for all layers
            layers = views[i].findall('.//DataModelImagingLayer')
            # set for spectra
            sset = set(self.spectralist)
            sset |= set(self.defaultspectra)
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





        XmlFileParser.write(self, self.tree, path)


    def addWavelength(self):
        """ add Wavelength to the Wavelength Set, opens a new Dialog"""
        AddWLDialog = QtWidgets.QDialog()
        ui = Ui_AddWLDialog()
        ui.setupUi(AddWLDialog)
        if AddWLDialog.exec():
            v = str(ui.spinBox.value())
            self.WLList.addItem(v)
            self.prefWLBox.addItem(v)
        # TODO: set spin box as selected, for easier keyboard input
        # TODO: set sorting order numerically
        
    def removeWavelength(self):
        """ remove selected Wavelength from the Wavelength Set and from the PrefferedWL Combobox"""
        # 
        try :
            t = self.WLList.takeItem(self.WLList.currentRow()).text()
            self.prefWLBox.removeItem(self.prefWLBox.findText(t))
        except AttributeError:
            # if there is no element in the list
            pass

    def displayTreetoGUI(self):
        """ Update the GUI  with the information in the xml file"""
        # TODO: sort after Tab?

        # ====== General Information =============
        self.presetTypeBox.setCurrentText(self.tree.find('.//PresetType').text)




        # ======== Acquisition Tab ===========
        self.displayAllWLBox.setChecked(self.tree.find('.//DisplayAllWavelengths').text == 'true')
        self.usvisibleBox.setChecked(self.tree.find('.//USVisible').text == 'true')
        wlset = self.tree.find('.//WavelengthSet/Items')
        for wl in wlset:
            # dont include comments
            try:
                w = (str(int(wl.text)))
                self.WLList.addItem(w)
                self.prefWLBox.addItem(w)
            except ValueError:
                pass

        # ========= Processing Tab ===========
        self.userSoundBox.setValue(int(self.tree.find('.//UserSoundTrim').text))
        self.SFAFrameThreshBox.setValue(float(self.tree.find('.//FRAMECORRTHRES').text))
        self.backgroundAbsorptionBox.setValue(float(self.tree.find('.//BackgroundAbsorption').text))
        self.backgroundOxyBox.setValue(int(self.tree.find('.//BackgroundOxygenation').text))




        self.prefWLBox.setCurrentText(self.tree.find('.//PreferredBackgroundWL').text)
        # ==================================
        self.nameBox.setPlainText(self.tree.find('.//Name').text)
        self.versionTextBox.setPlainText(self.tree.find('//PresetVersion').text)
        self.detectorBox.setPlainText(self.tree.find('.//CompatibleDetectorGUID').text)
        #add spectra to selectedList
        spectra = self.tree.find('.//UserSelectedSpectra')
        self.defaultspectra = ['OPUS', 'Background']
        #print(etree.tostring(spectra))
        for children in spectra:
            #print(children.text)
            self.spectralist.append(children.text)

        self.selectedList.addItems(self.spectralist)
        self.viewSpectraList.addItems(self.spectralist)

        self.unselectedspectra = list(set(self.allspectra)-set(self.spectralist))
        self.unselectedList.clear()
        self.unselectedList.addItems(self.unselectedspectra)

        #self.viewSpectraList.SelectItems(0)

        self.getViewingPresets()

        #self.applySettings()

        




    def cleanup(self):
        """ clean GUI, called before reading a new file"""
        self.selectedList.clear()
        self.WLList.clear()
        self.prefWLBox.clear()
        self.viewSpectraList.clear()
        self.viewSpectraList.addItems(self.defaultspectra)
        self.spectralist.clear()
        self.unselectedspectra = self.allspectra
        self.settingslist.clear()


    def getViewingPresets(self):
        """get the presets of the spectra for the four view panels"""

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

            settings = []

            #get settings for all layers
            layers = views[i].findall('.//DataModelImagingLayer')

            for j in range(0, len(layers)):

                spectrum = layers[j].find('.//ComponentTagIdentifier').text

                visible = True if(layers[j].find('.//Visible').text) == 'true' else False

                #print(layers[j].find('.//Visible').text)

                #print(layers[j].find('.//Semitransparent').text)


                transparent = True if (layers[j].find(
                    './Semitransparent').text) == 'true' else False

                mint = float(layers[j].find('.//GainMin').text)

                maxt = float(layers[j].find('.//GainMax').text)


                #add to settings of this view
                settings.append(ViewSetting(spectrum, visible, transparent, mint, maxt))


            # add the list of one view to the complete list
            self.settingslist.append(settings)



    def applySettings(self):
        """update gui with settings according to the current selected item"""
        # get selected view
        k = 0
        for i in range(0, len(self.radioButtons)):
            if self.radioButtons[i].isChecked():
                k = i
                break

        # get selected spectrum
        if self.viewSpectraList.count() == 0:
            return

        selected = self.viewSpectraList.currentItem()

        if selected is not None:
            #pprint(selected.text())
            selected = selected.text()

        else:
            selected = self.viewSpectraList.item(0).text()

        #print('View:'+ str(i)+ selected)
        settings = self.settingslist[k]

        for i in range(0, len(settings)):
            #pprint(selected)
            if settings[i].spectrum == selected:

                self.visibleCheck.setChecked(settings[i].visible)
                self.transparentCheck.setChecked(settings[i].transparent)
                self.minBox.setValue(settings[i].minthresh)
                self.maxBox.setValue(settings[i].maxthresh)

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
        new = [ViewSetting(item.text()),ViewSetting(item.text()),ViewSetting(item.text()),ViewSetting(item.text())]

        for i in range(0, len(self.settingslist)):
            self.settingslist[i].append(new[i])


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


    def changeSettings(self):
        """ save the changes made in the gui to the ViewSettings object,
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
                self.settingslist[view][j].visible = self.visibleCheck.isChecked()
                self.settingslist[view][j].transparent = self.transparentCheck.isChecked()
                self.settingslist[view][j].minthresh = self.minBox.value()
                self.settingslist[view][j].maxthresh = self.maxBox.value()
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
