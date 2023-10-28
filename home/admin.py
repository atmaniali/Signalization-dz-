from django.contrib import admin
import csv
import datetime
from django.http import HttpResponse

from home.models import FAQ, Banner, BannerSecand, ContactMessage, Rating, Settings


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


export_to_csv.short_description = "Export to CSV"  # short description


class SettingsAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "status", "updated_at"]
    actions = [export_to_csv]
    readonly_fields = ("site_views",)
    # search_fields = ['title']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "note", "updated_at", "status"]
    list_filter = ["status"]
    readonly_fields = ("name", "subject", "email", "message", "ip")
    actions = [export_to_csv]
    search_fields = ["email", "name"]


class FAQMessageAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "ordernumber", "status"]
    list_filter = ["status"]
    actions = [export_to_csv]
    # search_fields = ['question']


class RatingAdmin(admin.ModelAdmin):
    list_display = ["subject", "comment", "status", "create_at"]
    list_filter = ["status", "rate"]
    readonly_fields = ("subject", "comment", "ip", "user", "rate", "id")
    actions = [export_to_csv]
    search_fields = ["user__email"]


class BannerAdmin(admin.ModelAdmin):
    list_display = [
        "main_title",
        "secand_title",
        "main_title_clases",
        "secand_title_clases",
    ]
    actions = [export_to_csv]


class BannerSecandAdmin(admin.ModelAdmin):
    list_display = [
        "main_title",
        "secand_title",
        "main_title_clases",
        "secand_title_clases",
    ]
    actions = [export_to_csv]
    # search_fields = ['title']


admin.site.register(Settings, SettingsAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQMessageAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerSecand, BannerSecandAdmin)
