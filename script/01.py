import time
import requests
from bs4 import BeautifulSoup

item_cd='FPC-17A-002'
item_color='181'

src_url='https://www.jins.com/jp/item_itemproperty_zaiko_sub.html?item_cd='+item_cd
bs4obj=BeautifulSoup(requests.get(src_url).text,'html.parser')

th_name=[]
for i in bs4obj.select_one('table').select('th'):
	th_name.append(i.text)
print(th_name)

