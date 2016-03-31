from django.contrib import admin
from section.models import (
    Section, 
    Summary,
    Post,
    Photo
)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


class PostAdmin(admin.ModelAdmin):
    exclude = ('user', )
    list_display = ('id', 'status', 'created_at')
    list_filter = ('status', )
    ordering = ('-created_at', )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class SummaryAdmin(admin.ModelAdmin):
    exclude = ('user', )
    list_display = ('id', 'created_at')
    ordering = ('-created_at', )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class PhotoAdmin(admin.ModelAdmin):
    exclude = ('user', )
    list_display = ('id', 'status', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Section, SectionAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
