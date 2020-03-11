# 海关编码爬虫

### 一、介绍

海关编码爬虫脚本

https://hsbianma.com


### 二、使用说明

+ 确认已安装Python3环境、以及pip
+ 依赖库安装：
  + BeautifulSoup4
  + lxml

```shell
pip install BeautifulSoup4
pip install lxml
```
+ 运行脚本
```shell
python main.py [options]
```

参数列表:

+ --help：查看帮助信息
+ -s或--search \[chapter\]：爬取具体章节(商品编码前两位)的内容，默认01
+ -a或--all：爬取所有章节的内容。该开关开启时，-s 无效
+ --file-root \[dir\]: 设置保存文件的根路径，默认值\[HOME]/hascode_file。文件命名hscode_\[chapter]\_YYYYMMDD_HH:mm.txt，以及hscode_\[chapter]_latest.txt+
+ --no-latest：不生成(或覆盖原有的)latest文件


### 其他

帮助到了你就请我吃个阿尔卑斯吧