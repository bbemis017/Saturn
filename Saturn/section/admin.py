from django.contrib import admin
from section.models import (
    Section, 
    Summary,
    Post,
    Photo
)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique_name', )


class PostAdmin(admin.ModelAdmin):
    exclude = ('author', )
    list_display = ('id', 'title', 'status', 'created_at')
    list_filter = ('status', )
    ordering = ('-created_at', )
    search_fields = ('title', )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class SummaryAdmin(admin.ModelAdmin):
    exclude = ('author', )
    list_display = ('id', 'created_at')
    ordering = ('-created_at', )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class PhotoAdmin(admin.ModelAdmin):
    exclude = ('author', )
    list_display = ('id', 'title', 'status', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Section, SectionAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
