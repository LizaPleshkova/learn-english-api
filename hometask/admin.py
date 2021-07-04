from django.contrib import admin
from hometask.models import Hometask, CompletedHometask


class HometaskAdmin(admin.ModelAdmin):
    search_fields = ['task']


class CompletedHometaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['hometask', 'file_txt', 'mark', 'comment_admin']}
         ),
        ('Информация о дате',
         {'fields': ['date_finished'],
          'classes': ['collapse']}
         ),
    ]
    list_filter = ['date_finished']


admin.site.register(Hometask, HometaskAdmin)
admin.site.register(CompletedHometask, CompletedHometaskAdmin)
