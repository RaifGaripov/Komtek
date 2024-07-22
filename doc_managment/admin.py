from django.contrib import admin

from .models import RefBook, RefBookVersion, RefBookElement


class RefBookVersionInline(admin.TabularInline):
    model = RefBookVersion
    ordering = ["-start_date"]
    extra = 0


class RefBookElementInline(admin.TabularInline):
    model = RefBookElement
    extra = 0


class RefBookAdmin(admin.ModelAdmin):
    inlines = [RefBookVersionInline]
    list_display = ('id', 'code', 'name', 'get_current_version', 'get_current_version_start_date')

    @admin.display(description='Текущая версия')
    def get_current_version(self, obj):
        return obj.get_current_version()

    @admin.display(description='Дата начала действия версии')
    def get_current_version_start_date(self, obj):
        return obj.get_current_version_start_date()


class RefBookVersionAdmin(admin.ModelAdmin):
    inlines = [RefBookElementInline]
    list_display = ('id', 'refbook', 'version', 'start_date')


admin.site.register(RefBook, RefBookAdmin)
admin.site.register(RefBookVersion, RefBookVersionAdmin)
admin.site.register(RefBookElement)
