from django.contrib import admin
from review.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review)
# Register your models here.
