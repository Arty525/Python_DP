from django.contrib import admin

from restaurant.models import Content, Table, Reservation, Contacts


# Register your models here.
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content_type')
    list_filter = ('title', 'is_active', 'content_type')
    search_fields = ('title', 'text')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'hall', 'seats', 'status')
    list_filter = ('status', 'hall', 'seats')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'date', 'start_time', 'duration', 'end_time', 'table', 'status', 'guests', 'celebration')
    list_filter = ('user', 'first_name', 'last_name', 'date', 'start_time', 'duration','end_time', 'table', 'status', 'guests', 'celebration')
    search_fields = ('user',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_phone_number', 'phone_number', 'email', 'city', 'address', 'subway')
    list_filter = ('mobile_phone_number', 'phone_number', 'email', 'city', 'address', 'subway')