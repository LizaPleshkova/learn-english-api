from django.contrib import admin
from test.models import Category, Test, Question, Answer, TestResult, AnswerUser


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 5
    max_num = 5


class TestInLine(admin.TabularInline):
    model = Test
    extra = 1
    max_num = 1
    fieldsets = [
        (None,
         {'fields': ['title']}
         ),
    ]


class QuestionInline(admin.TabularInline):
    model = Question
    inline = [AnswerInline]
    max_num = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [TestInLine]


class TestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['title', "category_id"]}
         ),
        ('Информация о дате',
         {'fields': ['date_published'],
          'classes': ['collapse']}
         ),
    ]
    inlines = [QuestionInline]

    list_display = ('title', 'date_published')

    list_filter = ['date_published']

    search_fields = ['title']


class TestResultAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'test', 'score', 'completed', 'date_finished', 'count_correct', 'count_incorrect')
    list_filter = ['completed']


class AnswerUserAdmin(admin.ModelAdmin):
    readonly_fields = ('test_result', 'question', 'answer')
    list_filter = ['test_result']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(AnswerUser, AnswerUserAdmin)
