from django.contrib import admin
import csv
import datetime
from django.http import HttpResponse

from order.models import LikedList, Order, OrderProduct, ShopCart


# Register your models here.
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment;" "filename={}.csv".format(
        opts.verbose_name
    )
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)

    return response


class ShopCartAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "user",
        "quantity",
        "price",
        "varprice",
        "amount",
        "variant",
        "variant_id",
    ]
    list_filter = ["user"]
    actions = [export_to_csv]
    search_fields = ["product__title"]


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ("user", "product", "quantity", "price", "amount")
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "city", "total", "status"]
    list_filter = ["status", "user"]
    readonly_fields = (
        "user",
        "address",
        "city",
        "phone",
        "first_name",
        "ip",
        "last_name",
        "phone",
        "city",
        "total",
    )
    can_delete = False
    inlines = [OrderProductline]
    actions = [export_to_csv]
    search_fields = ["user__email"]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
        "price",
        "quantity",
        "amount",
        "variant",
        "variant_id",
    ]
    list_filter = ["user"]
    actions = [export_to_csv]
    search_fields = ["product__title", "user__email"]


class LikedListAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]
    actions = [export_to_csv]
    search_fields = ["product__title", "user__email"]


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(LikedList, LikedListAdmin)
