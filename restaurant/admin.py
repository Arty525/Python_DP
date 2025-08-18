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
    list_display = ('id', 'number', 'seats', 'status')
    list_filter = ('status', 'seats')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'time', 'table', 'status', 'guests', 'celebration')
    list_filter = ('user', 'date', 'time', 'table', 'status', 'guests', 'celebration')
    search_fields = ('user',)
