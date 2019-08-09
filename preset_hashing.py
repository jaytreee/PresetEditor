import base64
from lxml import etree
from hashlib import sha1

presetfilename = '2D_Masterpreset_v2.0_Hb HbO2 Melanin_multipanel.XML'

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
# Serialize (contenttree is already without blanks and comments)
xmlbytes = etree.tostring(presetelem)
chash = sha1()
chash.update(xmlbytes)
# Hex output
hashstr = chash.hexdigest()
print(hashstr)
# Base64 output
# hashstr = base64.b64encode(chash.digest()).decode('utf-8')
# print(hashstr)
