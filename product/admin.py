from django.contrib import admin
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
import csv
import datetime
from django.http import HttpResponse

from product.models import (
    Adehesive_Appearence,
    Category,
    Color,
    Comment,
    Demension,
    Fastener,
    Images,
    Materiel,
    Product,
    Type,
    Typologie,
    Variants,
    Visuel,
    ProductVisual,
)


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


@admin_thumbnails.thumbnail("image")
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ("pk", "id")
    classes = ("collapse",)
    # search_fields = ['title','category__title']
    # actions = [export_to_csv]
    extra = 1


class ProductVariantsInline(admin.StackedInline):
    model = Variants
    readonly_fields = ("image_tag",)
    extra = 1
    classes = ("collapse",)
    show_change_link = True


class ProductVisualInline(admin.TabularInline):
    model = ProductVisual
    extra = 1
    classes = "collapse"
    show_change_link = True


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = (
        "tree_actions",
        "indented_title",
        "related_products_count",
        "related_products_cumulative_count",
        "image_tag",
    )
    list_display_links = ("indented_title",)
    prepopulated_fields = {"slug": ("title",)}
    actions = [export_to_csv]
    search_fields = ["title"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, "category", "products_cumulative_count", cumulative=True
        )

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, "category", "products_count", cumulative=False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = (
        "Related products (for this specific category)"
    )

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = "Related products (in tree)"


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "image_tag"]
    list_filter = ["product_views", "product_search", "category"]
    search_fields = ["title", "category__title"]
    actions = [export_to_csv]
    inlines = [ProductImageInline, ProductVariantsInline, ProductVisualInline]
    readonly_fields = ("image_tag", "product_views", "product_search")
    prepopulated_fields = {"slug": ("title",)}


@admin_thumbnails.thumbnail("image")
class ImagesAdmin(admin.ModelAdmin):
    list_display = ["title", "product", "image"]
    actions = [export_to_csv]
    search_fields = ["title", "product__title"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["subject", "comment", "created_at"]
    list_filter = (
        "status",
        "rate",
    )
    readonly_fields = ["subject", "comment", "product", "rate", "user"]


class DemensionAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    actions = [export_to_csv]
    search_fields = ["name"]


class MaterielAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    actions = [export_to_csv]
    search_fields = ["name"]


class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "color_tag"]
    actions = [export_to_csv]
    search_fields = ["name"]


class VisuelAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    actions = [export_to_csv]
    search_fields = ["name"]


class TypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    actions = [export_to_csv]
    search_fields = ["name"]


class FastenerAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    actions = [export_to_csv]
    search_fields = ["name"]


class TypologieAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    actions = [export_to_csv]
    search_fields = ["name"]


class Adehesive_AppearenceAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    actions = [export_to_csv]
    search_fields = ["name"]


class VariantsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product",
        "color",
        "demension",
        "materiel",
        "price",
        "quantity",
        "image_tag",
    ]
    actions = [export_to_csv]
    search_fields = ["title", "product__title"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Demension, DemensionAdmin)
admin.site.register(Materiel, MaterielAdmin)
admin.site.register(Visuel, VisuelAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Fastener, FastenerAdmin)
admin.site.register(Typologie, TypologieAdmin)
admin.site.register(Adehesive_Appearence, Adehesive_AppearenceAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(ProductVisual)
