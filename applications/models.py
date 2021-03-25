from django.db import models

class SearchQueryModel(models.Model):
	# これを明示しないと参照エラーが発生する
	objects=models.Manager()
	md_query_name=models.CharField(max_length=50,null=True)
	md_radio_url=models.CharField(max_length=50,null=True)
	md_src_url=models.TextField(null=True)
	md_seller_url=models.TextField(null=True)
	md_radio_e_wday_e_time=models.CharField(max_length=50,null=True)
	md_e_wday=models.CharField(max_length=50,null=True)
	md_e_time=models.CharField(max_length=50,null=True)
	# md_analysis_pages=models.CharField(max_length=50,null=True)
	md_analysis_pages_radio=models.CharField(max_length=50,null=True)
	md_analysis_pages_str=models.CharField(max_length=50,null=True)
	md_analysis_pages_end=models.CharField(max_length=50,null=True)
	md_radio_ana_end_spec=models.CharField(max_length=50,null=True)
	md_ana_end_spec=models.CharField(max_length=50,null=True)
	md_auto_ext=models.CharField(max_length=50,null=True)
	md_rate_radio=models.CharField(max_length=50,null=True)
	md_rate=models.CharField(max_length=50,null=True)
	md_exclude_id_radio=models.CharField(max_length=50,null=True)
	md_exclude_id=models.TextField(null=True)
	md_exclude_titledesc_radio=models.CharField(max_length=50,null=True)
	md_exclude_titledesc=models.TextField(null=True)
	def __str__(self):
		return 'id:'+str(self.id)+' name:'+str(self.md_query_name)