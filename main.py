"""
    https://www.hsbianma.com/
    海关编码爬虫程序
    参数列表：
        --help或-h：查看帮助信息
        --search或-s [chapter]：爬取具体章节(商品编码前两位)的内容，默认01
        --all或-a：爬取所有章节的内容。该开关开启时，-s 无效
        --file-root [dir]: 设置保存文件的根路径，默认值[HOME]/hascode_file。\
          文件命名hscode_[chapter]_YYYYMMDD_HH:mm.txt，以及hscode_[chapter]_latest.txt
        --no-latest：不生成(或覆盖原有的)latest文件
    @author zhy
    @version 1.0
"""

import json
import os
import sys
import time

import requests

from bs4 import BeautifulSoup
from hs_record import BaseInfo, HsRecord, TaxInfo

BASE_URL = 'https://www.hsbianma.com'


def parse_argv():
    """
      解析系统参数
      python hscode.py -s 85
    """
    argv = sys.argv
    lenth = len(argv)
    result = {
        'search': '01',
        'file_root': os.environ['HOME'] + '/hscode_file',
        'outdated': False,
        'no_latest': False,
        'all': False,
        'help': False
    }
    # 第一个参数为hscode.py 直接从第二个开始进行解析
    for i in range(1, lenth):
        # 搜索条件参数
        if argv[i] == '-s' or argv[i] == '--search' and lenth > i+1:
            i += 1
            result['search'] = argv[i]
        # 文件根目录
        elif argv[i] == '--file-root' and lenth > i+1:
            i += 1
            result['file_root'] = argv[i]
        # 是否包含已过期数据
        elif argv[i] == '--outdated':
            result['outdated'] = True
        # 不生成/覆盖 latest 文件
        elif argv[i] == '--no-latest':
            result['no_latest'] = True
        # 爬取所有章节
        elif argv[i] == '--all' or argv[i] == '-a':
            result['all'] = True
        # 打印帮助信息
        elif argv[i] == '--help' or argv[i] == '-h':
            result['help'] = True
    return result


def url2html(url=''):
    """
      获取url地址的html内容，并以字符串返回
    """
    url_link = BASE_URL+'/'+url
    html = requests.get(url_link)
    html.encoding = 'utf-8'
    return html.text


def all_page_num(search):
    """
        search: 搜索条件
        查询指定搜索条件的最大页数
        返回int，如果没有则返回0
    """
    url = '/Search/999999?keywords=' + str(search)
    soup = BeautifulSoup(url2html(url), features='lxml')
    page_nav_div = soup.find(id='pagination')
    if page_nav_div is None:
        return 0
    page_span = page_nav_div.span
    if page_span is None:
        return 0
    return int(page_span.text)


def parse_code_head_tr(tr_, outdated=False):
    """
        通过每一行记录解析出商品编码并返回
    """
    tds = tr_.find_all('td')
    code_txt = tds[0].text
    code_txt = code_txt.replace(' ', '')
    code_txt = code_txt.replace('\n', '')
    code_txt = code_txt.replace('\r', '')
    code_txt = code_txt.replace('\t', '')
    code_txt = code_txt.replace('.', '')
    if '[过期]' in code_txt:
        if outdated:
            code = code_txt[0:-4]
            return int(code)
        return 0
    else:
        return code_txt


def query_page(search, page_index=1, outdated=False):
    """
        search: 搜索条件
        page_index: 页码
        outdated: 是否剔除已过期数据，默认True
        查询每一页的数据
        返回所有的商品编码集合
    """
    url = '/Search/' + str(page_index) + '?keywords=' + str(search)
    soup = BeautifulSoup(url2html(url), features='lxml')
    all_record_tr = soup.find_all('tr', class_='result-grid')
    if all_record_tr is None:
        return []
    result = []
    for tr_ in all_record_tr:
        code = parse_code_head_tr(tr_, outdated)
        if code != 0:
            result.append(code)
    return result


def find_details(code):
    """
        查询海关编码明细
    """
    url = '/Code/' + str(code) + '.html'
    html = url2html(url)
    soup = BeautifulSoup(html, 'lxml')
    # 资料div
    wrap_div = soup.find(id='wrap')
    if wrap_div is None:
        none_base = BaseInfo(code)
        return HsRecord(none_base, None, None, None, None, None)
    content = soup.find(id='wrap').contents[5].contents[1]
    details = content.find_all('div', class_='cbox')
    # 基本信息
    base_info_tab_txts = details[0].table.tbody.find_all('td', class_='td-txt')
    base_info = BaseInfo(code)
    base_info.name = base_info_tab_txts[1].text
    base_info.outdated = base_info_tab_txts[2].text == '过期'
    base_info.update_time = base_info_tab_txts[3].text
    # print(base_info)

    # 税率信息
    tax_info_tab = details[1].table.tbody
    # 税率种类
    tax_tr = tax_info_tab.find_all('tr')
    # 使用dict先存储避免网页税率顺序变化
    tax_result = {}
    for entity in tax_tr:
        tds = entity.find_all('td')
        # 税率名称
        name = tds[0].text
        # 税率值
        val = tds[1].text
        # 格式化税率值
        if val == '-' or val == '/':
            val = ''
        tax_result.update({name: val})
    # 税率属性值
    unit = tax_result.get('计量单位')
    export = tax_result.get('出口税率')
    ex_rebate = tax_result.get('出口退税税率')
    ex_provisional = tax_result.get('出口暂定税率')
    vat = tax_result.get('增值税率')
    preferential = tax_result.get('进口优惠税率')
    im_provisional = tax_result.get('进口暂定税率')
    import_ = tax_result.get('进口普通税率')
    consumption = tax_result.get('消费税率')
    tax_info = TaxInfo(unit, export, ex_rebate, ex_provisional,
                       vat, preferential, im_provisional, import_, consumption)
    # print(tax_info)

    # 申报要素
    declaration_txts = details[2].table.tbody.find_all('td', class_='td-txt')
    declarations = []
    for declaration in declaration_txts:
        txt = declaration.text
        txt = txt.replace('[?]', '')
        txt = txt.replace(' ', '')
        declarations.append(txt)
    # print(declarations)

    # 监管条件
    supervision_txts = details[3].table.tbody.find_all('td', class_='td-label')
    supervisions = []
    for supervision in supervision_txts:
        txt = supervision.text
        if txt != '无' and txt != '':
            supervisions.append(txt)
    # print(supervisions)

    # 检验检疫类别
    quarantines_txts = details[4].table.tbody.find_all('td', class_='td-label')
    quarantines = []
    for quarantine in quarantines_txts:
        txt = quarantine.text
        if txt != '无' and txt != '':
            quarantines.append(txt)
    # print(quarantines)

    # ciq编码
    ciq_code_txts = details[6].table.tbody.find_all('td', class_='td-label')
    ciq_codes = []
    for ciq_code in ciq_code_txts:
        txt = ciq_code.text
        if txt != '无'and txt != '':
            ciq_codes.append(txt)
    # print(ciq_codes)
    return HsRecord(base_info, tax_info, declarations, supervisions, quarantines, ciq_codes)


def get_search_of(search, include_outdated, file_root, no_latest):
    """
        爬取指定章节的所有code
    """
    # 最大页数
    page_num = all_page_num(search)
    all_code = []
    # 此处可以改用多线程
    for page_index in range(page_num):
        all_code.extend(query_page(search, page_index + 1, include_outdated))

    if not os.path.exists(file_root):
        os.mkdir(file_root)

    curr_date = time.strftime('%Y%m%d_%H:%M', time.localtime())

    outdated_str = "outdated_" if include_outdated else ''

    file_path = file_root + '/hscode_' + \
        outdated_str + search + '_' + curr_date + '.txt'

    file_latest = file_root + '/hscode_' + outdated_str + search + '_latest.txt'

    file1 = open(file_path, 'w')
    if not no_latest:
        file2 = open(file_latest, 'w')

    for code in all_code:
        # 解析海关编码
        hs_record = find_details(code)
        hs_record_str = str(hs_record)
        # 检验是否合法json
        print(hs_record_str)
        json.loads(hs_record_str)
        #　写入文件
        file1.write(hs_record_str)
        file1.write('\n')
        if not no_latest:
            file2.write(hs_record_str)
            file2.write('\n')
    file1.close()
    if not no_latest:
        file2.close()

    print('Items (with searching "' + search + '"' +
          (' including outdated'if include_outdated else '') +
          ')' +
          ' num: ' + str(len(all_code)))


def main():
    """
        main函数
    """

    args = parse_argv()

    if args.get('help'):
        print('参数列表：')
        print('  --help|-h                       查看帮助信息')
        print('  --search|-s [chapter]           爬取具体章节(商品编码前两位)的内容，默认01')
        print('  --all|-a                        爬取所有章节的内容。该开关开启时，--search 无效')
        print(
            '  --file-root [dir]               设置保存文件的根路径，默认值[HOME]/hascode_file')
        print(
            '                                  文件命名格式hscode_[chapter]_YYYYMMDD_HH:mm.txt，以及hscode_[chapter]_latest.txt')
        print('  --no-latest                     不生成(或覆盖原有的)latest文件')
        return
    # print(args)
    # 搜索条件
    search = args.get('search')
    include_outdated = args.get('outdated')
    file_root = args.get('file_root')
    # 是否爬取所有页面
    all_search = args.get('all')
    no_latest = args.get('no_latest')

    if all_search:
        # 01-09
        for i in range(9):
            chapter = '0' + str(i+1)
            get_search_of(chapter, include_outdated, file_root, no_latest)
        # 10-99
        for i in range(10, 100):
            get_search_of(str(i), include_outdated, file_root, no_latest)
    else:
        get_search_of(str(search), include_outdated, file_root, no_latest)


main()

# debug 单个页面
# json_str = str(find_details(8523521000))
# print(json_str)
# json.loads(json_str)
