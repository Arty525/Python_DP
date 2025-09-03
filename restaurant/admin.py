from django.contrib import admin

from restaurant.models import Content, Table, Reservation, Contacts, Team, Service, Feedback, Chief, SousChef


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


@admin.register(Chief)
class ChiefAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(SousChef)
class SousChefAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')



@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ('description',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'is_active')
    list_filter = ('title', 'description', 'price', 'is_active')
    search_fields = ('title', 'description')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'datetime', 'status')
    list_filter = ('first_name', 'last_name', 'email', 'phone', 'status')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'text')