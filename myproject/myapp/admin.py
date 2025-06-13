from django.contrib import admin
from .models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',  'specification', 'qualification']

admin.site.register(Teacher, TeacherAdmin)
