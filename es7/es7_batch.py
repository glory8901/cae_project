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
# json文件夹路径
dir_path = r'F:\全球项目库数据\json_all\280-630'
# 错误数统计
err_count = 0
# 连接es
es = elasticsearch.Elasticsearch([es_url])

# 项目库规定的日期格式：2019、2019-01、2019-01-01
p_date = re.compile(r'(\d{4})(-(\d{2})(-(\d{2}))?)?')
p_fund = re.compile(r'[\d.]+')

# 记录文件
json_record_file = 'es_import_record.tsv'
json_error_file = 'es_import_error.tsv'


def bulk_insert(es, actions):
    # 批量插入
    res = helpers.bulk(es, actions)
    print(res)


def time_format_to_es(date_format):
    m = p_date.match(date_format)
    if m:
        groups = m.groups()
        year = int(groups[0])
        month = int(groups[2]) if groups[2] else 1
        day = int(groups[4]) if groups[4] else 1
        date_ = datetime.date(year, month, day).strftime('%Y-%m-%d')
        return date_
    return None


# 每行一个json
def read_one_json_file(file_path, file_name):
    file_content = []
    with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as f:
        # next(f)  # 有header时跳过
        for line in f:
            # 加载json
            json_dict = json.loads(line.strip())
            # 处理json中的特殊字段
            if json_dict['Project'].get('StartDate'):
                json_dict['Project']['StartDate']['text'] = time_format_to_es(
                    json_dict['Project']['StartDate']['format'])
            if json_dict['Project'].get('EndDate'):
                json_dict['Project']['EndDate']['text'] = time_format_to_es(json_dict['Project']['EndDate']['format'])
            if not p_fund.fullmatch(json_dict['Project']['Fund'].get('text')):
                temp_fund = json_dict['Project']['Fund'].get('text')
                if temp_fund.endswith(',00'):
                    json_dict['Project']['Fund']['text'] = int(temp_fund[:-3])
                else:
                    logger.error('error fund : %s', temp_fund)
            file_content.append({
                "_index": _index,
                "_id": json_dict['Project']['exchangeID'].strip(),
                "_source": json_dict
            })
    return file_content


def gendata(file_dir):
    for file_name in os.listdir(file_dir):
        yield (file_name, read_one_json_file(file_dir, file_name))


def filter_error_jsonfile(dir, error_record):
    # 筛选出入库错误的json
    err_file = os.path.join(dir, error_record)
    all_errors = []
    with open(err_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            if row[1] == '0':
                all_errors.append((dir_path, row[0]))
    return all_errors


def import_to_es():
    order = 0
    with open(json_record_file, 'w', encoding='utf-8') as f:
        for file_name, jsons in gendata(dir_path):
            order += 1
            try:
                res = helpers.bulk(es, jsons, request_timeout=60)
                print(order, res)
                f.write('%s\t%d\n' % (file_name, res[0]))
            except Exception as e:
                logger.exception(e)
                f.write('%s\t0\n' % (file_name))


def import_error_datas_to_es():
    # 读取输入有误的记录
    errors = filter_error_jsonfile('.', json_record_file)
    num = 0
    # 仍然有错误的，输出到控制台及文件中
    with open(json_error_file, 'w', encoding='utf-8') as f:
        for dir, file_name in errors:
            num += 1
            jsons = read_one_json_file(dir, file_name)
            try:
                res = helpers.bulk(es, jsons, request_timeout=60)
                print(num, res)
                f.write('%s\t%d\n' % (file_name, res[0]))
            except Exception as e:
                logger.exception(e)
                f.write('%s\t0\n' % (file_name))


def del_by_exchangeid():
    # 读取输入有误的记录
    errors = filter_error_jsonfile('.', json_record_file)
    num = 0
    # 找到错误的id
    for dir, file_name in errors:
        num += 1
        jsons = read_one_json_file(dir, file_name)
        for j in jsons:
            exc_id = j['_source']['Project']['exchangeID']
            res = es.delete_by_query(index=_index, body={'query': {'match': {'Project.exchangeID': exc_id}}})
            print(res['deleted'])


if __name__ == '__main__':
    # 将json导入es中，每行一个json
    # import_to_es()
    # 处理错误的json数据
    # import_error_datas_to_es()
    # 删除错误的数据
    del_by_exchangeid()
