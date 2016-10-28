from lxml import etree

tree = etree.parse('task1.xml')

for item in tree.xpath('//page'):
    subfields = item.getchildren()
    count = len([subfield.attrib["type"] for subfield in subfields if subfield.attrib["type"] == "text"])
    print item.attrib["url"], " - ", count
