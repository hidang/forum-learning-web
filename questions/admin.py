from django.contrib import admin
from .models import Comment, Question


class CommentInline(admin.TabularInline):
    model = Comment


class QuestionAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
