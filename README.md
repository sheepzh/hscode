# 海关编码查询

[![codecov](https://codecov.io/gh/sheepzh/hscode/branch/master/graph/badge.svg?token=5DX131J0LI)](https://codecov.io/gh/sheepzh/hscode)
[![](https://img.shields.io/github/license/sheepzh/hscode)](https://github.com/sheepzh/hscode/blob/main/LICENSE)
[![](https://img.shields.io/github/v/release/sheepzh/hscode)](https://github.com/sheepzh/hscode/releases)

海关编码查询。有其他需求，建议或者意见，请提 ISSUE。

https://hsbianma.com


### 二、爬虫脚本使用说明

+ 确认已安装Python3环境、以及pip3。暂不打算支持 Python2
+ 依赖库安装：
  + BeautifulSoup4
  + lxml
  + requests

```shell
pip3 install BeautifulSoup4
pip3 install lxml
pip3 install requests
```
+ 运行脚本
```shell
python3 main.py [options]
```
参数列表:

+ --help：查看帮助信息
+ -s或--search \[chapter\]：爬取具体章节(商品编码前两位)的内容，默认01
+ -a或--all：爬取所有章节的内容。该开关开启时，-s 无效
+ --file-root \[dir\]: 设置保存文件的根路径，默认值\[HOME]/hascode_file。文件命名hscode_\[chapter]\_YYYYMMDD_HH:mm.txt，以及hscode_\[chapter]_latest.txt
+ --no-latest：不生成(或覆盖原有的)latest文件
+ --outdated: 爬取过期数据
+ --quiet或-q: 不打印海关编码信息
+ --proxy或-p [proxy-url]：设置请求代理

### 数据格式

+ 每行保存一条编码数据
+ 数据格式示例如下

```json
{   
    "code":"0106209010", 
    "name":"其他濒危爬行动物",
    "outdated":false,
    "update_time":"2020/1/1 0:00:00",
    "tax_info":{
        "unit":"千克/只",
        "export":"0%",
        "ex_rebate":"0%",
        "ex_provisional":"",
        "vat":"9%",
        "preferential":"10%",
        "im_provisional":"",
        "import":"50%",
        "consumption":""
    },
    "declarations":[
        "品牌类型",
        "出口享惠情况",
        "GTIN",
        "CAS"
    ],
    "supervisions":[
        "F",
        "E",
        "A",
        "B"
    ],
    "quarantines":[
        "P",
        "Q"
    ],
    "ciq_codes":{
        "0106209010999": "其他濒危爬行动物(包括人工驯养、繁殖的）"
    }
}
```

### TODO

+ 发布到 PyPi
