# -*- coding: utf-8 -*-
import json
import os
import elasticsearch

# 索引名称
_index = 'projectdata'
# ES地址
es_url = 'localhost:9200'
# 文件路径
file_path = r'E:\Dataset\cae-project-data\test_json'
# 错误数统计
err_count = 0


# 存入数据
def put_json(file_name, err_count):
    file = open(os.path.join(file_path, file_name), 'r', encoding='utf-8')
    if file is None:
        return
    text = json.load(file)
    # print(text)
    try:
        es = elasticsearch.Elasticsearch([es_url])
        es.index(index=_index, id=None, body=text)
    except:
        print("插入异常")
        err_count += 1


# 读取所有文件的列表【测试：一次入一条数据】
for i in os.listdir(file_path):
    print(i)
    put_json(i, err_count)
    print('finish')

print('err count ' + str(err_count))
