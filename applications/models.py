from django.db import models

class UserDataModel(models.Model):
	objects=models.Manager()
	md_name=models.CharField(max_length=50,null=True)
	md_line_token=models.CharField(max_length=100,null=True)
	md_to_email=models.CharField(max_length=100,null=True)
	md_ac_id=models.CharField(max_length=100,null=True)
	md_ac_pass=models.CharField(max_length=100,null=True)
	def __str__(self):
		return 'id:'+str(self.id)+' name:'+str(self.md_name)

class BorderDataModel(models.Model):
	objects=models.Manager()
	md_name=models.CharField(max_length=50,null=True)
	md_cancel_border=models.TextField(null=True)
	md_reserve_border=models.TextField(null=True)
	def __str__(self):
		return 'id:'+str(self.id)+' name:'+str(self.md_name)