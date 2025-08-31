from django.contrib import admin

from restaurant.models import Content, Table, Reservation


# Register your models here.
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('title', 'is_active')
    search_fields = ('title', 'text')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'hall', 'seats', 'status')
    list_filter = ('status', 'hall', 'seats')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'start_time', 'duration', 'end_time', 'table', 'status', 'guests', 'celebration')
    list_filter = ('user', 'date', 'start_time', 'duration','end_time', 'table', 'status', 'guests', 'celebration')
    search_fields = ('user',)
