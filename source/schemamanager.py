from shutil import copyfile
import os
import sys

class iXMLSchemaManager:
    """ XML Schema Manager class that controls the availability of the most recent schemata
    At first start, store packaged schemata to APPDATA\iThera\Schemata
    Always use schema at this spot, with the same name as in the xmlmodel Respository (ArrayofDataModelStudyPreset.xsd)
    ---> refers to the Types.xsd, that should also be up to date
    """
    
    folder = os.path.join(os.environ['APPDATA'], 'iThera\\Schemata')

    def writeSchema(self):
        """ write the packaged schema to APPDATA\iThera\Schemata"""
        if  hasattr(sys, "_MEIPASS"): # TMP folder in exceutable
            src =  os.path.join(sys._MEIPASS, 'SchemaV1.0.xsd')
        else:
            src = r'H:\Code\com.itheramedical.PresetEditor\source\resources\SchemaV1.0.xsd'
        
        dest = self.folder
        if not os.path.isfile(dest+'\Types.xsd'):
            if not os.path.exists(dest):
                os.makedirs(dest)
            copyfile(src, dest+'\Types.xsd')
        


