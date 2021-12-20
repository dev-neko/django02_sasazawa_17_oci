from django.db import models

class BorderDataModel(models.Model):
	objects=models.Manager()
	md_name=models.CharField(max_length=50,null=True)
	md_r_day=models.CharField(max_length=50,null=True)
	md_r_time=models.CharField(max_length=50,null=True)
	md_r_shisetsu=models.CharField(max_length=50,null=True)
	md_r_shitsujou=models.CharField(max_length=50,null=True)
	md_r_corder=models.CharField(max_length=50,null=True)
	def __str__(self):
		return 'id:'+str(self.id)+' name:'+str(self.md_name)