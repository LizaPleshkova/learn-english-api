from django.contrib import admin
from survey.models import PollQuestion, PollChoice


class PollChoiceInline(admin.TabularInline):
    model = PollChoice
    max_num = 1

    readonly_fields = ('votes',)


class PollQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['question_text']}
         ),
        ('Информация о дате',
         {'fields': ['pub_date'],
          'classes': ['collapse']}
         ),
    ]

    inlines = [PollChoiceInline]

    list_filter = ['pub_date']

    search_fields = ['question_text']


admin.site.register(PollQuestion, PollQuestionAdmin)
