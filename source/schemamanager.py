import os
import sys
from shutil import copyfile
from urllib import request, error
import ssl
import hashlib

class iXMLSchemaManager:
    """ XML Schema Manager class that controls the availability of the most recent schemata
    At first start, store packaged schemata to APPDATA\iThera\Schemata
    Always use schema at this spot, with the same name as in the xmlmodel Respository (ArrayofDataModelStudyPreset.xsd)
    ---> refers to the Types.xsd, that should also be up to date
    """
    
    folder = os.path.join(os.environ['APPDATA'], 'iThera\\Schemata')
    md5sumurl = 'https://dist.ithera-medical.com/pydist/schemata/md5sums'
    md5sums = None

    def writeSchema(self, file):
        """ write the packaged schema to APPDATA\iThera\Schemata"""
        if  hasattr(sys, "_MEIPASS"): # TMP folder in exceutable
            src =  os.path.join(sys._MEIPASS, file)
        else:
            src = 'H:\\Code\\com.itheramedical.PresetEditor\\source\\resources\\'+file
        
        dest = self.folder
        if not os.path.isfile(dest+'\Types.xsd'):
            if not os.path.exists(dest):
                os.makedirs(dest)
            copyfile(src, dest+'\Types.xsd')
        

    def getmd5sums(self):
        """ get current md5sums, indicator for new version"""
        ssl._create_default_https_context = ssl._create_unverified_context
        response = request.urlopen(self.md5sumurl)
        string = response.read().decode('utf8')
        string = string[:-1]
        self.md5sums = dict(item.split('  ')[::-1] for item in string.split('\n'))

    def comparemd5sums(self):
        """ compare md5 sums of (existing) files, if not the same, donwload new version"""
        for key in self.md5sums:
            f= self.folder+'/'+key
            if os.path.isfile(f):
                if self.md5(f) == self.md5sums[key]:
                    continue
            # otherwise download file
                request.urlretrieve('https://dist.ithera-medical.com/pydist/schemata/'+key,self.folder+'/'+key)
                print('Downloaded new version of: '+key)
        print('Schema up to date')

    def md5(self, fname):
        """ calculate md5 checksum for a file"""
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
           for chunk in iter(lambda: f.read(4096), b""):
               hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def main(self):
        self.writeSchema('SchemaV1.0.xsd')
        self.writeSchema('ArrayOfDataModelStudyPreset.xsd')
        try:
            self.getmd5sums()
            self.comparemd5sums()
        except error.URLError as e:
            print(e)