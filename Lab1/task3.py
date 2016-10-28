from lxml import html
from lxml import etree
import requests

page = requests.get('http://hotline.ua/bt/holodilniki/')
tree = html.fromstring(page.content)

links = tree.xpath('//b[@class="m_r-10"]/a/@href')

root = etree.Element('data')
doc = etree.ElementTree(root)

page_element = etree.SubElement(root, 'page',
                                     url="http://hotline.ua/bt/holodilniki/")

counter = 0
i = 0
while counter != 20:
    page = requests.get('http://hotline.ua' + links[i])
    tree = html.fromstring(page.content)
    price = tree.xpath('//a[@class="range-price orng g_statistic"]/strong/text()')
    description = tree.xpath('//p[@class="full-desc text-14"]/text()')
    image = tree.xpath('//img[@class="max-250 ma p_r-15 g_statistic"]/@src')
    if description:
        product_element = etree.SubElement(root, 'product')
        name_element = etree.SubElement(product_element, 'price')
        name_element.text = price[0]
        desc_element = etree.SubElement(product_element, 'description')
        desc_element.text = description[0]
        image_element = etree.SubElement(product_element, 'image')
        image_element.text = 'http://hotline.ua'+ image[0]
        counter += 1
    i += 1

doc.write('task3.xml', xml_declaration=True, encoding='utf-8')

