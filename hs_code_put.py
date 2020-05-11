"""
  上传海关编码信息到应用后台
  @author zhy
  @since 1.0
"""
import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

# 线程池
EXCETOR = ThreadPoolExecutor(30)

HS_CODE_LATEST_DIR = os.environ['HOME'] + '/hscode_file/latest'
# API 网关地址
API_URL = "http://localhost:10011/hscode"

def all_files():
    """
        获取所有文件
    """
    if not os.path.isdir(HS_CODE_LATEST_DIR):
        print('waring: no this directory [' + HS_CODE_LATEST_DIR + ']')
        return []
    for root, dirs, files in os.walk(HS_CODE_LATEST_DIR):
        return files

def read_tax_info(tax_info, field):
    """
        读取税率信息
    """
    if field not in tax_info:
        return ''
    val = tax_info[field]
    val = val.replace(' ', '')
    if '%' in val:
        val = val[0:-1]
    return val

def send(line):
    """
        发送 code 信息
    """
    obj = json.loads(line)
    tax_info = obj['tax_info']
    data = {
        'name': obj.get('name', ''),
        'code': obj['code'],
        'outdated': obj['outdated'],
        'unit': read_tax_info(tax_info, 'unit'),
        'export_rate': read_tax_info(tax_info, 'export'),
        'export_rebate': read_tax_info(tax_info, 'ex_rebate'),
        'export_provisional': read_tax_info(tax_info, 'ex_provisional'),
        'vat': read_tax_info(tax_info, 'vat'),
        'import_preferential': read_tax_info(tax_info, 'im_provisional'),
        'import_provisional': read_tax_info(tax_info, 'provisional'),
        'import_rate': read_tax_info(tax_info, 'import'),
        'consumption': read_tax_info(tax_info, 'consumption'),
        'declarations': obj.get('declarations', []),
        'supervisions': obj.get('supervisions', []),
        'quarantines': obj.get('quarantines', []),
        'ciq_codes': obj.get('ciq_codes', [])
        }
    # print(str(data))
    response = requests.put(API_URL, data=json.dumps(data), headers={'Content-Type':'application/json'})
    if response.status_code is not 200:
        print("------------------"+str(response.status_code))
        print(data)
    else :
        cont = json.loads(response.content)
        if 'code' not in cont or cont.get('code') is not 0:
            print(str(cont))

def read_and_send(file_name):
    """
        读取文件
    """
    file_path = HS_CODE_LATEST_DIR + '/' + file_name
    if not os.path.exists(file_path):
        print('warning: file [' + file_path + '] not exists')
    with open(file_path, 'r') as file:
        for line in file.readlines():
            EXCETOR.submit(send, line)
        

def main():
    """
        主函数
    """
    files = all_files()
    for file in files:
        read_and_send(file)

main()
