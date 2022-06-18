from django.db import models

class DBModel(models.Model):
	objects=models.Manager()
	md_name=models.CharField(max_length=50,null=True)
	md_video_title=models.CharField(max_length=150,null=True)
	md_ts_chat=models.TextField(null=True)
	md_dl_state=models.CharField(max_length=50,null=True)
	# md_video_length=models.CharField(max_length=50,null=True)
	# md_video_recorded_at_jst=models.CharField(max_length=50,null=True)
	def __str__(self):
		return 'id:'+str(self.id)+' name:'+str(self.md_name)