"""
qt designer test
"""
# pylint: disable=E1101
# pylint: disable=C0103

import sys
#from pprint import pprint
from xmlfileparser import XmlFileParser
from lxml import etree
from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QFileDialog
from preset_editor_gui import Ui_MainWindow
from viewsetting import ViewSetting




class PresetEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Editor for Settings
    """
    tree = etree

    defaultspectra = ['OPUS', 'Background']

    allspectra = ['HbO2', 'Hb', 'Melanin', 'ICG', 'Test1', 'Test2']

    """selected spectra"""
    spectralist = []

    """ unselected spectra"""
    unselectedspectra = list(set(allspectra)-set(spectralist))


    """dimensions = #views; containing corresponing viewsetting objects """
    settingslist = [[], [], [], []]

    def __init__(self):
        super(PresetEditor, self).__init__()
        self.setupUi(window)

        #self.addBtn.clicked.connect(self.addInputTextToListbox)
        self.loadButton.clicked.connect(self.loadxmlFile)


        self.tabWidget.tabBarClicked.connect(self.applySettings)
        self.view1Button.clicked.connect(self.applySettings)
        self.view2Button.clicked.connect(self.applySettings)
        self.view3Button.clicked.connect(self.applySettings)
        self.view4Button.clicked.connect(self.applySettings)
        self.viewSpectraList.clicked.connect(self.applySettings)

        self.addButton.clicked.connect(self.addspectra)
        self.deleteButton.clicked.connect(self.removespectra)

        self.visibleCheck.clicked.connect(self.changeSettings)
        self.transparentCheck.clicked.connect(self.changeSettings)
        self.minBox.editingFinished.connect(self.changeSettings)
        self.maxBox.editingFinished.connect(self.changeSettings)




        self.radioButtons = [self.view1Button, self.view2Button, self.view3Button, self.view4Button]

        self.unselectedList.addItems(self.unselectedspectra)
        self.viewSpectraList.addItems(self.defaultspectra)

        #self.treeWidget.itemDoubleClicked.connect(self.setTreeItem)

    def loadxmlFile(self):
        """ load xml File """

        self.cleanup()

        if False:
            path = QtWidgets.QFileDialog.getOpenFileName()

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
        #TODO:

        pass


    def displayTreetoGUI(self):
        """ Updat the GUI  with the information in the xml file"""
        self.nameBox.setPlainText(self.tree.find('.//Name').text)
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
        """ clean GUI before reading new file"""
        self.selectedList.clear()
        self.viewSpectraList.clear()
        self.viewSpectraList.addItems(self.defaultspectra)
        self.spectralist.clear()
        self.unselectedspectra = self.allspectra
        self.settingslist.clear()


    def getViewingPresets(self):
        """get the presets of the spectra for the four view panels"""

        viewingpresets = self.tree.find('.//ViewingPresets')
        #print(etree.tostring(viewingpresets))
        views = viewingpresets.findall('.//DataModelViewingPreset')

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
        """called when addButton is clicked"""

        #remove from unselected list and view and add to list and view
        row = self.unselectedList.currentRow()
        if row == -1:
            return
        item = self.unselectedList.takeItem(row)
        self.selectedList.addItem(item)
        self.spectralist.append(item.text())
        self.unselectedspectra.remove(item.text())
        #an item can only belong to one widget at a time
        self.viewSpectraList.addItem(item.text())
        #pprint(item)

        #add viewsettings object for the new spectrum
        new = ViewSetting(item.text())

        for i in range(0, len(self.settingslist)):
            self.settingslist[i].append(new)


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
        #the item to remove is 2 rows below, after OPUS and background """
        self.viewSpectraList.takeItem(row+2)

        #remove settingsobject"
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

    app = QtWidgets.QApplication(sys.argv)

    style = 'iLabs.css'

    ''' with open(style, mode='r') as ss:
        app.setStyleSheet(ss.read()) '''

    window = QtWidgets.QMainWindow()

    prog = PresetEditor()

    window.show()
    sys.exit(app.exec_())
