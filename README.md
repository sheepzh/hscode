# 海关编码查询

[![codecov](https://codecov.io/gh/sheepzh/hscode/branch/master/graph/badge.svg?token=5DX131J0LI)](https://codecov.io/gh/sheepzh/hscode)
[![](https://img.shields.io/github/license/sheepzh/hscode)](https://github.com/sheepzh/hscode/blob/main/LICENSE)
[![](https://img.shields.io/github/v/release/sheepzh/hscode)](https://github.com/sheepzh/hscode/releases)


https://hsbianma.com

海关编码查询。**不打算兼容Python2**。


## 使用

### 代码内调用

1. 安装
```shell
  pip3 install hscode 
```
2. 引入
```python
from hscode import get_code_info
```
3. 查询单条海关编码信息

```python
code = get_code_info('123')
print(code)
```
不存在时返回 None
```python
code = get_code_info('2302500000')
print(code)
```
查询 [2302500000](https://hsbianma.com/Code/2302500000.html) 成功时返回的海关编码信息。
```json
# 以下为格式化后的显示
{
    "code": "2302500000",
    "name": "豆类植物糠、麸及其他残渣",
    "outdated": false,
    "update_time": "2021/1/7",
    "tax_info": {   
        "unit": "千克",
        "export": "0%",
        "ex_rebate": "0%",
        "ex_provisional": "",
        "vat": "9%",
        "preferential": "5%",
        "im_provisional": "",
        "import": "30%",
        "consumption": ""
    },
    "declarations": [
        "品名",
        "品牌类型",
        "出口享惠情况",
        "种类[玉米的、小麦的等]",
        "GTIN",
        "CAS",
        "其他"
    ],
    "supervisions": ["A", "B"],
    "quarantines": ["P", "Q"],
    "ciq_codes": {
        "2302500000999": "豆类植物糠、麸及其他残渣"
    }
}
```

### 爬虫

使用爬虫脚本可以批量爬取海关编码信息

1. 克隆仓库并安装依赖
```shell
git clone https://github.com/sheepzh/hscode.git
cd hscode

pip3 install BeautifulSoup4
pip3 install lxml
pip3 install requests
```

2. 查看帮助信息

```shell
python3 main.py --help
```

```txt
参数列表：
  --help|-h                     查看帮助信息
  --search|-s [chapter]         爬取具体章节(商品编码前两位)的内容，默认01
  --all|-a                      爬取所有章节的内容。该开关开启时，--search 无效
  --file-root [dir]             保存文件的根路径
                                默认值[HOME]/hascode_file
                                文件名格式: 
                                 hscode_[chapter]_YYYYMMDD_HH:mm.txt
                                 hscode_[chapter]_latest.txt
  --no-latest                   不生成(或覆盖原有的)latest文件
  --quiet|-q                    静默模式，不打印日志信息
  --outdated                    包含[过期]数据
  --proxy|-p [proxy-url]        请求代理
                                 --proxy https://www.baidu.com?s={url}
                                {url} 是原始请求 url
```

3. 示例：爬取 [第 97 章](https://hsbianma.com/search?keywords=97) 的海关编码

```shell
python3 main.py -s 97 --outdated
```

```
Query page:chapter=97, page=1
.........
Query page:chapter=97, page=[最大页数]
{ "code": "9701101000", "name": "手绘油画、粉画及其他画的原件(但手工绘制及手工描饰的制品或品目4906的图纸除外)", "outdated": true, "update_time": "2018/12/30", "tax_info": { "unit": "幅", "export": "0.0%", "ex_rebate": "0.0%", "ex_provisional": "", "vat": "17.0%", "preferential": "12.0%", "im_provisional": "6.0%", "import": "50.0%", "consumption": "0.0%" } }
{ "code": "9701101100", "name": "唐卡原件", "outdated": false, "update_time": "2021/1/8", "tax_info": { "unit": "幅/千克", "export": "0%", "ex_rebate": "0%", "ex_provisional": "", "vat": "13%", "preferential": "6%", "im_provisional": "", "import": "50%", "consumption": "" }, "declarations": ["品名", "品牌类型", "出口享惠情况", "是否野生动物产品", "尺寸大小", "GTIN", "CAS", "其他"], "ciq_codes": {"9701101100999": "唐卡原件(但带有手工绘制及手工描饰的制品或品目4906的图纸除外)"} }
......
......
{ "code": "9701101900", "name": "其他手绘油画、粉画及其他画的原件", "outdated": false, "update_time": "2021/1/8", "tax_info": { "unit": "幅/千克", "export": "0%", "ex_rebate": "0%", "ex_provisional": "", "vat": "13%", "preferential": "1%", "im_provisional": "", "import": "50%", "consumption": "" }, "declarations": ["品名", "品牌类型", "出口享惠情况", "是否野生动物产品", "尺寸大小", "作者", "作品名称", "GTIN", "CAS", "其他"], "ciq_codes": {"9701101900999": "其他手绘油画、粉画及其他画的原件(但带有手工绘制及手工描饰的制品或品目4906的图纸除外)"} }
{ "code": "9706000090", "name": "其他超过一百年的古物", "outdated": false, "update_time": "2021/1/8", "tax_info": { "unit": "千克", "export": "0%", "ex_rebate": "0%", "ex_provisional": "", "vat": "13%", "preferential": "0%", "im_provisional": "", "import": "0%", "consumption": "" }, "declarations": ["品名", "品牌类型", "出口享惠情况", "年代", "是否野生动物产品", "GTIN", "CAS", "其他"], "ciq_codes": {"9706000090999": "其他超过一百年的古物"} }
Item (with searching "97" including outdated) num: [爬取结果的总行数]
```
爬取的内容将保存在本地文件中

```shell
cat ~/hscode_file/latest/hscode_97.txt
```

每行用 json 的格式存储一条海关编码。内容与上述日志打印的内容相同。
### TODO

+ <del>发布到 PyPi</del>
+ 将爬虫命令加入到 PyPi 包
