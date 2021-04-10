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

from cmd import main

main()
