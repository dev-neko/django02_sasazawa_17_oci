from django.contrib import admin
from .models import SearchQueryModel,UserDataModel

admin.site.register(SearchQueryModel)
admin.site.register(UserDataModel)