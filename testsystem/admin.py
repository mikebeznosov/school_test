from django.contrib import admin
from .models import Test, Question, Answer, Result

class QuestionAdmin(admin.ModelAdmin):
    fields = ['test', 'text', 'image', 'allow_text_answer']
    # Это позволит писать формулы в админке с подсветкой синтаксиса

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)