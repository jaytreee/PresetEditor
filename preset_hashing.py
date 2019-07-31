import uuid
from lxml import etree

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
xmlstring = etree.tostring(presetelem, encoding='unicode')
# Generate Hash
chash = str(uuid.uuid5(uuid.NAMESPACE_DNS, xmlstring))
