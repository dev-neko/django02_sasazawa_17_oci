import datetime
import time
from applications.models import SearchQueryModel
from django.core.management.base import BaseCommand, CommandError

# https://qiita.com/jansnap/items/d50f59dabc5da7c1d0dd
class Command(BaseCommand):
	help = 'crawler for test.'
	def handle(self, *args, **options):
		# t = SearchQueryModel.objects.all()
		# self.stdout.write(self.style.SUCCESS("all Topic=%s" % t))

		SearchQueryModel.objects.create(id=1,md_query_name=datetime.datetime.now())

		while True:
			tmp_db=SearchQueryModel.objects.get(id=1)
			dt_now=datetime.datetime.now()
			tmp_db.md_query_name=dt_now
			# self.stdout.write(dt_now)
			self.stdout.write(self.style.SUCCESS(dt_now))
			tmp_db.save()
			time.sleep(1)