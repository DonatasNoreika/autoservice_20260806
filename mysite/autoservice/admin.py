from django.contrib import admin
from .models import (Service,
                     Car,
                     Order,
                     OrderLine,
                     OrderComment,
                     Profile)


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    readonly_fields = ['line_sum', 'service_price']
    fields = ['service', 'quantity', 'service_price', 'line_sum']


class OrderCommentInLine(admin.TabularInline):
    model = OrderComment
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'client', 'date', 'deadline', 'total', 'status', 'is_overdue']
    inlines = [OrderLineInLine, OrderCommentInLine]
    readonly_fields = ['date', 'total']

    fieldsets = [
        ('General', {'fields': ('car', 'client', 'date', 'deadline', 'total', 'status')}),
    ]


class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'license_plate', 'vin_code', 'client_name']
    list_filter = ['client_name', 'make', 'model']
    search_fields = ['license_plate', 'vin_code']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class OrderCommentAdmin(admin.ModelAdmin):
    list_display = ['order', 'author', 'date', 'content']

# Register your models here.
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(OrderComment, OrderCommentAdmin)
admin.site.register(Profile)
