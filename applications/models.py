from django.db import models

class SearchQueryModel(models.Model):
	# これを明示しないと参照エラーが発生する
	objects=models.Manager()
	md_query_name=models.CharField(max_length=50,null=True)
	md_or_title=models.TextField(null=True)
	md_ex_title=models.TextField(null=True)
	md_or_desc=models.TextField(null=True)
	md_ex_desc=models.TextField(null=True)
	md_price_min=models.CharField(max_length=50,null=True)
	md_price_max=models.CharField(max_length=50,null=True)
	md_alert_sw=models.CharField(max_length=50,null=True)
	def __str__(self):
		return 'id:'+str(self.id)+' name:'+str(self.md_query_name)