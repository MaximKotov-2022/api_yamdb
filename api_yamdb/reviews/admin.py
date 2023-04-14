from django.contrib import admin

from reviews.models import  Title, Category, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category',)
    list_display_links = ('name')
    list_editable = ('category',)
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
