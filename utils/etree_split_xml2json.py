# -*- coding: utf-8 -*-
import os
import xmltodict
import json
import xml.etree.ElementTree as ET
from utils.fileUtil import append_json, write_json


def remove_xml_special_chars(d):
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            value = remove_xml_special_chars(value)
        elif isinstance(value, list):
            value = [remove_xml_special_chars(x) if isinstance(x, dict) else x for x in value]

        # 去掉其中的命名空间
        if ':' in key:
            new_key = key[key.index(':') + 1:]
            result[new_key] = value
        elif ('@' in key) or ('#' in key):
            new_key = key.replace('#', '').replace('@', '')
            result[new_key] = value
    return result


# 定义xml转json的函数
def xmltojson(xmlstr):
    # parse是的xml解析器
    xmlparse = xmltodict.parse(xmlstr)
    parse_dict = remove_xml_special_chars(xmlparse)
    # print(parse_dict)
    # json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    # dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(parse_dict, ensure_ascii=False)
    return jsonstr


def readXml(filepath, loop_xpath, ns):
    '''read xml by elementTree
    input: xml filepath
    output: xml linelist to csv'''

    try:
        # prase to tree
        tree = ET.parse(filepath)
    except:
        print('xml损坏无法解析：', filepath)
        return None

    # loop_xpath
    root = tree.getroot()
    nodes = root.findall(loop_xpath, ns)
    # print(list(nodes))
    return [ET.tostring(node, encoding='utf-8', method='xml') for node in nodes]


def parse_xml_part(xml_ele_str):
    return xmltojson(xml_ele_str)


def handle_one_xml(xml_path):
    xml_name = os.path.basename(xml_path)
    xml_name_noext = os.path.splitext(xml_name)[0]
    # 读取xml
    nodes = readXml(xml_path, loop_xpath, ns)
    first_time = True
    for node in nodes:
        # 将该node转为json
        json_str = parse_xml_part(node)
        json_file = '%s/%s.json' % (json_dir, xml_name_noext)
        # 第一次覆盖写入，以后append进去
        if first_time:
            write_json(json_str, json_file)
            first_time = False
        else:
            append_json(json_str, json_file)


if __name__ == '__main__':
    # xml文件中一个里面有500个项目数据，需要先拆分开，然后使用xmltodict转为json，并保存下来
    # 配置
    xml_dir = r'F:\全球项目库数据\280_xml_3'
    json_dir = r'F:\全球项目库数据\json_all'
    ns = {'istic': 'http://matadata.istic.ac.cn/elements/2019',
          'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
          'xsd': 'http://www.w3.org/2001/XMLSchema'}
    loop_xpath = './istic:ProjectData/istic:Project'

    for base_dir, dir_names, xml_names in os.walk(xml_dir):
        for xml_name in xml_names:
            xml_path = os.path.join(base_dir, xml_name)
            handle_one_xml(xml_path)
