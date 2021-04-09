# -*- coding: utf-8 -*-
"""
    The argument of hscode
"""
import os
DEFAULT_CHAPTER = '01'
DEFAULT_FILE_ROOT = os.path.join(os.environ['HOME'], 'hscode_file')


class Argument:
    """
        The argument set
    """

    def __init__(self):
        self.all_chapters = False
        self.chapter = DEFAULT_CHAPTER
        self.file_root = DEFAULT_FILE_ROOT
        self.outdated = False
        self.no_latest = False
        self.print_help = False
        self.quiet_mode = False
        self.url_proxy = None


def print_help():
    """
        Print the help info
    """
    print('参数列表：')
    print('  --help|-h                     查看帮助信息')
    print('  --search|-s [chapter]         爬取具体章节(商品编码前两位)的内容，默认01')
    print('  --all|-a                      爬取所有章节的内容。该开关开启时，--search 无效')
    print('  --file-root [dir]             保存文件的根路径')
    print('                                默认值[HOME]/hascode_file')
    print('                                文件名格式: ')
    print('                                 hscode_[chapter]_YYYYMMDD_HH:mm.txt')
    print('                                 hscode_[chapter]_latest.txt')
    print('  --no-latest                   不生成(或覆盖原有的)latest文件')
    print('  --outdated                    包含[过期]数据')
    print('  --proxy|-p [proxy-url]        请求代理')
    print('                                 --proxy https://www.baidu.com?s={url}')
    print('                                {url} 是原始请求 url')


def parse_argv(sys_argv):
    """
      解析系统参数
      python hscode.py -s 85
    """
    length = len(sys_argv)
    result = Argument()
    #　是否已经读取 py 参数
    read_py_file = False
    for i in range(0, length):
        arg = sys_argv[i]
        if not read_py_file and arg.endswith('.py'):
            read_py_file = True
            continue
        # 搜索条件参数
        if arg in ['-s', '--search'] and length > i + 1 and not result.all_chapters:
            i += 1
            result.chapter = sys_argv[i]
        # 文件根目录
        elif arg == '--file-root' and length > i + 1:
            i += 1
            result.file_root = sys_argv[i]
        # 是否包含已过期数据
        elif arg == '--outdated':
            result.outdated = True
        # 不生成/覆盖 latest 文件
        elif arg == '--no-latest':
            result.no_latest = True
        # 爬取所有章节
        elif arg in ['--all', '-a']:
            result.all_chapters = True
            result.chapter = None
        # 打印帮助信息
        elif arg in ['--help', '-h']:
            result.print_help = True
        # 静默模式
        elif arg in ['--quiet', '-q']:
            result.quiet_mode = True
        # 代理
        elif (arg in ['--proxy', '-p']) and length > i + 1:
            i += 1
            url_proxy = sys_argv[i]
            if '{url}' in url_proxy:
                result.url_proxy = url_proxy
    return result
