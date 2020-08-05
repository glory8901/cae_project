import json
import xmltodict


# 定义xml转json的函数
def xmltojson(xmlstr):
    # parse是的xml解析器
    xmlparse = xmltodict.parse(xmlstr)
    # json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    # dumps()方法的ident=1，格式化json
    # AttributeError: 'dict' object has no attribute 'dumps'
    jsonstr = json.dumps(xmlparse, indent=1)
    print(jsonstr)


# json转xml函数
def jsontoxml(jsonstr):
    # xmltodict库的unparse()json转xml
    xmlstr = xmltodict.unparse(jsonstr)
    print(xmlstr)


if __name__ == "__main__":
    json_str_dict = {'student': {'course': {'name': 'math', 'score': '90'},
                        'info': {'sex': 'male', 'name': 'name'}, 'stid': '10213'}}
    jsontoxml(json_str_dict)

    # 需要转换json格式的xml
    xml = """
<student>
  <stid>10213</stid>
  <info>
    <name>name</name>
    <sex>male</sex>
  </info>
  <course>
    <name>math</name>
    <score>90</score>
  </course>
</student>
  """
    xmltojson(xml)  # 调用转换函数
