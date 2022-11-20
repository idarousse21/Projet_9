from django.contrib import admin
from review.models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review)
admin.site.register(UserFollows)
# Register your models here.
