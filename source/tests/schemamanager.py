# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 10:19:00 2017

@author: thomas.hartmann
"""

from lxml import etree
from shutil import copyfile
import os
import urllib
import ssl
import http.client
path =r'H:\Code\com.itheramedical.PresetEditor\source\resources\SchemaV1.0.xsd'
schema_doc = etree.parse(path)
xmlschema = etree.XMLSchema(schema_doc)
dest = os.path.join(os.environ['APPDATA'], 'iThera\\Schemata')
if not os.path.exists(dest):
    os.makedirs(dest)


copyfile(r'H:\Code\com.itheramedical.PresetEditor\source\resources\SchemaV1.0.xsd',dest+'\Types.xsd')


folder = os.path.join(os.environ['APPDATA'], 'iThera\\Schemata')

ssl._create_default_https_context = ssl._create_unverified_context
response = urllib.request.urlopen('https://dist.ithera-medical.com/pydist/schemata/md5sums')
# file = urllib.request.urlretrieve('https://dist.ithera-medical.com/pydist/schemata/md5sums',dest+'\md5sums.txt')

html = response.read()
# response.data()
string = html.decode('utf8')
# remove last linebreak
string = string[:-1]
d = dict(item.split('  ')[::-1] for item in string.split('\n'))

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def comparemd5sums(self):
        for key in d:
            f= folder+'/'+key
            if os.path.isfile(f):
                if md5(f) == d(key):
                    continue
            # otherwise download file
            urllib.request.urlretrieve('https://dist.ithera-medical.com/pydist/schemata/md5sums',dest+'/'+key+'.xsd')
            
                