from lxml import html
from lxml import etree
import requests


def only_whitespaces(str):
    for symbol in str:
        if symbol is not " ":
            continue
        else:
            return 1
    return 0


def parse_html():
    root = etree.Element('data')

    doc = etree.ElementTree(root)

    page = requests.get('http://korrespondent.net/')
    tree = html.fromstring(page.content)
    link = tree.xpath('//a[not(@class)]/@href')

    counter, i = 0, 0

    while counter != 20:
        if "javascript" in link[i]:
            i += 1
            continue
        page = requests.get(link[i])
        tree = html.fromstring(page.content)
        images = tree.xpath('//img/@src')
        text = tree.xpath('//*[text()]')

        if text and images:
            # print link[i]
            page_element = etree.SubElement(root, 'page',
                                            url=link[i])
            for t in text:
                if t.tag != "script" and t.text and not only_whitespaces(t.text):
                    text_fragment = etree.SubElement(page_element, 'fragment',
                                                     type='text')
                    text_fragment.text = t.text
                    # print t.text
            for image in images:
                image_fragment = etree.SubElement(page_element, 'fragment',
                                                  type='image')
                image_fragment.text = image
            # print images
            counter += 1
        i += 1

    doc.write('task1.xml', xml_declaration=True, encoding='utf-8')


parse_html()




