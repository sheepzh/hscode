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
        --quiet或-q：静默模式，不打印海关编码信息
        --proxy或-p [proxy-url]: 使用请求代理
    @author zhy
    @version 1.2
"""
import sys
from hscode import argument
from hscode.spider import search_chapter
from hscode.writter import write


def search_and_save(chapter, args):
    """
        Search and save
    """
    include_outdated = args.outdated
    quiet = args.quiet_mode
    proxy = args.url_proxy
    hscodes = search_chapter(chapter, include_outdated, quiet, proxy)
    write(args.file_root, chapter, hscodes, not args.no_latest)


def main():
    """
        Entrance
    """
    args = argument.parse_argv(sys.argv)

    if args.print_help:
        argument.print_help()
        return
    # 搜索条件
    chapter = args.chapter
    # 是否爬取所有页面
    all_search = args.all_chapters

    if all_search:
        # 01-09
        for i in range(1, 10):
            chapter = '0' + str(i)
            search_and_save(chapter, args)
        # 10-99
        for i in range(10, 100):
            search_and_save(str(i), args)
    else:
        search_and_save(str(chapter), args)
