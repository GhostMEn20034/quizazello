from django.contrib import admin

from .models import Quiz


class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer',)
    search_fields = ('question',)


admin.site.register(Quiz, QuizAdmin)
