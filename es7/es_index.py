import json
import os
import elasticsearch
from elasticsearch import helpers
import time
import logging
import datetime
import re
import csv
# Initialize coloredlogs.
import coloredlogs

coloredlogs.install(level='INFO')

logger = logging.getLogger(__name__)

# 索引名称
_index = 'projectdata'
# ES地址
es_url = 'localhost:9200'

# 连接es
es = elasticsearch.Elasticsearch([es_url])

answer_index = 'baidu_answer'
answer_type = 'doc'
answer_mapping = {
        "doc": {
            "properties": {
                "qtitle": {
                    "type": "text",
                    # "index": True
                },
                "rContent": {
                    "type": "text",
                    # "analyzer": "ik_max_word"
                }
            }
        }
    }
# 创建索引
# es.indices.create(answer_index)
# 设置mapping
# es.indices.put_mapping(index=answer_index,doc_type=answer_type,body=answer_mapping)

# 查看所有索引
alias = es.indices.get_alias()
print(alias)

# 查询所有index名称
result = es.indices.get_alias().keys()
print(result)

# 查询index信息,包含mapping  settings信息
result = es.indices.get(_index)
print(result)

# 查看指定index的mapping信息
result = es.indices.get_mapping(_index)
print(result)

# 查看指定index的mapping信息
result = es.indices.get_settings(_index)
print(result)
