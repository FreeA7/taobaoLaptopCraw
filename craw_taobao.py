import requests
from bs4 import BeautifulSoup
from json import loads

f = open('output.txt', 'w')
f.write('id\t产品名称\t排名\t全网参考价格\timportantKey\t在售商家数量\t')
f.write('热销\t新品\t降价\tmonth_sales\ttag1\ttag2\ttag3\t点评数\t类目排名\t屏幕尺寸\t')
f.write('硬盘容量\t核心数量\t内存容量\t上市时间\t处理器型号\t分辨率\t摄像头类型\t电池容量\t')
f.write('接口类型\t操作系统\t品牌\t型号\t4G网络\tCPU主频\t产品类型\t尺寸\t电池类型\t重量\t')
f.write('续航时间\t存储类型\t触摸屏类型\t附加功能\t是否支持蓝牙\t前置摄像头像素\t后置摄像头像素\n')
f.flush()

url = 'https://s.taobao.com/list?q=%E5%B9%B3%E6%9D%BF%E7%94%B5%E8%84%91&s='
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
s = requests.Session()
product_list = []

for i in range(17): # 17
    res = s.get(url + str(i * 48))
    begin = res.text.find('\"spus\":')
    end = res.text.find('}},\"spucombo\"')
    text1 = res.text[begin:end + 4]
    # print(text1)
    count = 0
    while text1.find('{\"cat') != -1 or text1.find(']}},\"') != -1:
        if text1.find('{\"cat') == -1 and text1.find(']}},\"') != -1:
            product_list.append(loads('{' + text1[:-5]))
            text1 = ''
            count += 1
        else:
            spilt_flag = text1.find('{\"cat')
            if count == 0:
                pass
            else:
                if text1[:spilt_flag][-1] == ',':
                    product_list.append(loads('{' + text1[:spilt_flag][:-1]))
                else:
                    product_list.append(loads('{' + text1[:spilt_flag]))
            text1 = text1[spilt_flag + 1:]
            count += 1

    print('遍历' + str(i+1) + '页完成')

count = 0
for i in product_list:
	count += 1
	res = s.get('https:' + i['seller']['url'])
	if res.url == 'https://s.taobao.com/list?app=mainSrp&q=%E5%B9%B3%E6%9D%BF%E7%94%B5%E8%84%91&cd=false':
		print(str(count) + '\t' + i['title'] + ' no info')
		continue

	f.write(i['cat'] + '\t' + i['title'] + '\t' + str(count) + '\t' + i['price'] + '\t' + i['importantKey'] + '\t' + i['seller']['num'])
	if 'tag' in i.keys():
		if i['tag'] == 'isnew':
			f.write('\t0\t1\t0\t')
		elif i['tag'] == 'ishot':
			f.write('\t1\t0\t0\t')
		else:
			f.write('\t0\t0\t1\t')
	else:
		f.write('\t0\t0\t0\t')
	f.write(i['month_sales'])
	if len(i['tag_info']) == 0:
		f.write('\tnull\tnull\tnull')
	elif len(i['tag_info']) == 1:
		f.write('\t' + i['tag_info'][0]['tag'] + '\tnull\tnull')
	elif len(i['tag_info']) == 2:
		f.write('\t' + i['tag_info'][0]['tag'] + '\t' + i['tag_info'][1]['tag'] + '\tnull')
	else:
		f.write('\t' + i['tag_info'][0]['tag'] + '\t' + i['tag_info'][1]['tag'] + '\t' + i['tag_info'][2]['tag'])
	f.write('\t' + str(i['cmt_count']))
	f.flush()

	
	target_text = res.text[res.text.find('g_page_config = {'):res.text.find('\"catpath\":[')]
	data = loads(target_text[16:-1] + '}}}}')
	# print (data)
	try:
		f.write('\t' + str(data['mods']['spuhead']['data']['catRank']))
	except:
		f.write('\tnull')
	
	for k in range(len(data['mods']['spuhead']['data']['params'])):
		if data['mods']['spuhead']['data']['params'][k]['value'] == ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,':
			print (21312321321312)
		f.write('\t' + data['mods']['spuhead']['data']['params'][k]['value'])
	f.write('\n')
	f.flush()
	print(str(count) + '\t' + i['title'])

