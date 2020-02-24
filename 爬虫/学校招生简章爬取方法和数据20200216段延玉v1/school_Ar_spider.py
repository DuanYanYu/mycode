"""
爬取各大学校的招生简章，主要是2019年的招生简章
"""
import requests
import re
from lxml import etree
import xlwt

# 创建一个Excel文件
xls = xlwt.Workbook()
sheet = xls.add_sheet('招生简章')
sheet.write(0, 0, '学校')
sheet.write(0, 1, '招生简章')

# 定义Excel表的行号
line = 1
# 定义网页号（一共有28页）
page = 0

for i in range(0, 28):

    url = "https://gaokao.chsi.com.cn/zsgs/zhangcheng/listVerifedZszc--method-index,lb-1,start-%s.dhtml" %page
    response = requests.get(url)
    html = response.text
    # 查找学校章程的网址和学校名称
    schools = re.findall(r'<td class="yes">.*? <a href="(.*?)" target="_blank".*?>(.*?)</a>&nbsp;.*?</td>', html, re.S)

    #schoolArs保存学校招生简章的url, school保存学校名称
    for schoolArs, school in schools:
        school = school.replace('\r\n', '')
        school = school.replace(' ', '')
        schoolArs_url = "https://gaokao.chsi.com.cn%s" %schoolArs

        #爬取最新的招生简章
        response2 = requests.get(schoolArs_url)
        html2 = response2.text
        html2Elm = etree.HTML(html2)
        # 异常处理，处理学校没有招生简章的情况
        try:
            # xpath选取2019招生章程的地址
            ARurl = html2Elm.xpath("//div[@class='width1000 gery']/div[2]//tr[1]/td[1]/a/@href")[0]
            ARurl = "https://gaokao.chsi.com.cn%s" %ARurl
        except IndexError:
            print(school+"没有招生简章")
            ARurl = ""
        # 往Excel写入数据
        sheet.write(line, 0, school)
        sheet.write(line, 1, ARurl)
        line += 1
        print("----------%s-------------" %page)
        print(school, ARurl)
    # 每一页的url最后的部分都是1的100整数倍
    page += 100

xls.save('招生简章.xls')
