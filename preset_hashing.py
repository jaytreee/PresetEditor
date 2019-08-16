import base64
from lxml import etree
from hashlib import sha1

presetfilename = r'testdata\2D_Masterpreset_v2.0_Hb HbO2 Melanin_multipanel.XML'

def recursively_empty(e):
   if e.text:
       return False
   return all((recursively_empty(c) for c in e.iterchildren()))

reducedparser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
tree = etree.parse(presetfilename, reducedparser)  # Parses Preset File
for item in tree.getroot():     # Find DataModelStudyPreset
    if item.tag == 'DataModelStudyPreset':
        presetelem = item
        break
# Remove contentHash from attribute
if 'contentHash' in presetelem.attrib:
    del presetelem.attrib['contentHash']
# Remove Preset Name, Preset Identifier, Preset Version for "functional content" only hash
for item in presetelem:
    if item.tag in ('PresetIdentifier', 'Name', 'PresetType', 'PresetVersion', 'IsDefaultPreset'):
        presetelem.remove(item)

# Remove empty nodes
context = etree.iterwalk(presetelem)
for action, elem in context:
    parent = elem.getparent()
    if recursively_empty(elem):
        parent.remove(elem)

# Serialize (contenttree is already without blanks and comments)
xmlbytes = b'<?xml version="1.0" encoding="utf-8"?>' + etree.tostring(presetelem, xml_declaration=False, encoding="utf-8", pretty_print=False)
with open('prehash_out.xml', 'w') as f:
    f.write(xmlbytes.decode('utf-8'))

chash = sha1()
chash.update(xmlbytes)
# Hex output
hashstr = chash.hexdigest()
print(hashstr)

# Pretty XML output (for debugging)
xmlbytes_pretty = b'<?xml version="1.0" encoding="utf-8"?>\n' + etree.tostring(presetelem, xml_declaration=False, encoding="utf-8", pretty_print=True)
with open('prehash_out_pretty.xml', 'w') as f:
    f.write(xmlbytes_pretty.decode('utf-8'))
