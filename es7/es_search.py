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

# 搜索（按照条件来搜索）
res = es.search(index=_index, body={'query': {'match': {'Project.exchangeID': '4ecf9d96-7349-4c66-8f89-3b028b067def'}}})
result = res['hits']['hits']
# print(result)
for r in result:
    print(r['_id'])
    print(r['_source'])

# doc = {'id': 7, 'schoolId': '007', 'schoolName': '大明1'}
# # 赠
# es.index(index=_index, body=doc, id=doc['id'])
# # 查
# res = es.get(index=_index, id='QlUHvXIBLqdlntM8oUJD')
# print(res)
# # 改
# es.update(index='indexName', id=7, body=doc)
# # 删
# es.delete(index=_index, id=7)

res = es.delete_by_query(index=_index, body={'query': {'match': {'Project.exchangeID': '4ecf9d96-7349-4c66-8f89-3b028b067def'}}})
print(res)

