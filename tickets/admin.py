from django.contrib import admin

from .models import Ticket, Category, FollowUp


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type']
    list_display_links = ['title']
    list_editable = ['type']
    list_filter = ['category', 'type']
    search_fields = ['title', 'category', 'associate']


admin.site.register(Category)
admin.site.register(FollowUp)
admin.site.register(Ticket, TicketAdmin)
