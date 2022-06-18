"""
https://itc.tokyo/django/how-to-create-custom-template-filter/

関数を追加するときは
@register.filter
も付与すればINSTALLED_APPSに追加する必要はない
"""

from django import template
from datetime import datetime as dt
import datetime

register=template.Library()

@register.filter
def hhmmss_conv(value):
	aaa=dt.strptime(value,'%H:%M:%S')
	# print(str(aaa.hour)+'h'+str(aaa.minute)+'m'+str(aaa.second)+'s')
	return str(aaa.hour)+'h'+str(aaa.minute)+'m'+str(aaa.second)+'s'

@register.filter
def sss(value):
	#ここに処理を入れる
	return value+'aaa'

if __name__=='__main__':
	hhmmss_conv('2:02:02')