# -*- coding: utf-8 -*-
"""
    The spider
"""
import json
import requests
from bs4 import BeautifulSoup
from hscode.row import Hscode, BaseInfo, TaxInfo

BASE_URL = 'https://www.hsbianma.com'


def url2html(url, proxy):
    """
      Get the page content of url
    """
    url_link = BASE_URL + url
    if proxy:
        url_link = proxy.replace('{url}', url_link)
    response = requests.get(url_link, timeout=1)
    if response.status_code == 404:
        return ''
    response.encoding = 'utf-8'
    content = response.text
    if not content:
        content = ''
    return str(content)


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
            return code_txt[0:-4]
        return None
    return code_txt


def query_hscodes_by_page(chapter, page_index=1, outdated=False, proxy=None):
    """
        search: 搜索条件
        page_index: 页码
        outdated: 是否剔除已过期数据，默认True
        查询每一页的数据
        返回所有的商品编码集合
    """
    url = '/Search/' + str(page_index) + '?keywords=' + str(chapter)
    content = url2html(url, proxy)
    if not content:
        # no response content or 404
        return []
    soup = BeautifulSoup(content, features='lxml')
    all_record_tr = soup.find_all('tr', class_='result-grid')
    if all_record_tr is None:
        return []
    result = []
    for tr_ in all_record_tr:
        code = parse_code_head_tr(tr_, outdated)
        if code:
            result.append(code)
    return result


def parse_base_info(code, details_div):
    """
        Parse base info
    """
    base_info_tab_txts = details_div[0].table.tbody.find_all('td', class_='td-txt')
    base_info = BaseInfo(code)
    base_info.name = base_info_tab_txts[1].text.replace(
        '\n', '').replace('\r', '').replace(' ', '')
    base_info.outdated = base_info_tab_txts[2].text == '过期'
    base_info.update_time = base_info_tab_txts[3].text
    return base_info


def parse_tax_info(_code, details_div):
    """
        税率信息
    """
    # 税率种类
    tax_tr = details_div[1].table.tbody.find_all('tr')
    # 使用dict先存储避免网页税率顺序变化
    tax_result = {}
    for entity in tax_tr:
        tds = entity.find_all('td')
        # 税率值
        val = tds[1].text
        # 格式化税率值
        if val in ('-', '/'):
            val = ''
        tax_result.update({tds[0].text: val})
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
    return TaxInfo(unit, export, ex_rebate, ex_provisional, vat, preferential, im_provisional, import_, consumption)


def parse_declaration(_code, details_div):
    """
        申报要素
    """
    declaration_txts = details_div[2].table.tbody.find_all('td', class_='td-txt')
    declarations = []
    for declaration in declaration_txts:
        txt = declaration.text
        txt = txt.replace('[?]', '')
        txt = txt.replace(' ', '')
        declarations.append(txt)
    return declarations


def parse_supervision(_code, details_div):
    """
        监管条件
    """
    supervision_txts = details_div[3].table.tbody.find_all('td', class_='td-label')
    supervisions = []
    for supervision in supervision_txts:
        txt = supervision.text
        if txt not in ('无', ''):
            supervisions.append(txt)
    return supervisions


def parse_quarantines(_code, details_div):
    """
        检验检疫类别
    """
    quarantines_txts = details_div[4].table.tbody.find_all('td', class_='td-label')
    quarantines = []
    for quarantine in quarantines_txts:
        txt = quarantine.text
        if txt not in ('无', ''):
            quarantines.append(txt)
    return quarantines


def parse_ciq_codes(_hscode, details_div):
    """
        ciq编码
    """
    ciq_codes = {}
    ciq_trs = details_div[6].table.tbody.find_all('tr')
    for ciq_tr in ciq_trs:
        tds = ciq_tr.find_all('td')
        if len(tds) == 2:
            ciq_code = tds[0].text
            ciq_name = tds[1].text.replace('\r', '').replace(
                '\n', '').replace(' ', '').replace('"', '').replace("'", '')
            ciq_codes[ciq_code] = ciq_name
    return ciq_codes


def parse_details(code, proxy=None):
    """
        查询海关编码明细
    """
    html = url2html('/Code/' + str(code) + '.html', proxy)
    if not html:
        return None
    soup = BeautifulSoup(html, 'lxml')
    # 资料div
    wrap_div = soup.find(id='wrap')
    if wrap_div is None:
        none_base = BaseInfo(code)
        return Hscode(none_base, None, None, None, None, None)
    content = soup.find(id='wrap').contents[5].contents[1]
    details = content.find_all('div', class_='cbox')
    base_info = parse_base_info(code, details)
    tax_info = parse_tax_info(code, details)
    declarations = parse_declaration(code, details)
    supervisions = parse_supervision(code, details)
    quarantines = parse_quarantines(code, details)
    ciq_codes = parse_ciq_codes(code, details)
    return Hscode(base_info, tax_info, declarations, supervisions, quarantines, ciq_codes)


def search_chapter(chapter, include_outdated=False, quiet=False, proxy=None):
    """
        Search the chapter
    """
    all_code = []
    page_num = 1
    while True:
        hscodes_per_page = query_hscodes_by_page(chapter, page_num, include_outdated, proxy)
        if len(hscodes_per_page) == 0:
            break
        if not quiet:
            print('Query page:chapter=' + str(chapter) + ', page=' + str(page_num))
        all_code.extend(hscodes_per_page)
        page_num = page_num + 1
    all_code_infos = []
    for code in all_code:
        # 解析海关编码
        hscode = parse_details(code, proxy)
        hscode_str = str(hscode)
        # 检验是否合法json
        if not quiet:
            print(hscode_str)
        json.loads(hscode_str)
        all_code_infos.append(hscode)
    if not quiet:
        print('Item (with searching "' + chapter + '"' + (' including outdated'if include_outdated else '') + ')' + ' num: ' + str(len(all_code)))
    return all_code_infos
