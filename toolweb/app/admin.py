from django.contrib import admin
from .models import AppModel, HtmlContent, ViewContent


# Register your models here.

@admin.register(AppModel)
class AppAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "read_num"]

    def __str__(self):
        return self.name


@admin.register(ViewContent)
class ViewContentAdmin(admin.ModelAdmin):
    list_display = ["id"]

    def __str__(self):
        return self.id


@admin.register(HtmlContent)
class HtmlContentAdmin(admin.ModelAdmin):
    list_display = ["id"]

    def __str__(self):
        return self.id
