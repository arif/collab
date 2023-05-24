from django.contrib import admin

from documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', )
    search_fields = ('title', 'content', )

    def save_model(self, request, obj, form, change):
        if not change:
            if getattr(obj, 'author', None) is None:
                obj.author = request.user
        obj.save()
