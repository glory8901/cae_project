import xml.etree.ElementTree as ET

ns = {'istic': 'http://matadata.istic.ac.cn/elements/2019',
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      'xsd': 'http://www.w3.org/2001/XMLSchema'}

tree = ET.parse('abc.xml')
root = tree.getroot()
print(root.tag)

for neighbor in root.findall('./istic:ProjectData/istic:Project',ns):
    print(neighbor,neighbor.attrib)
