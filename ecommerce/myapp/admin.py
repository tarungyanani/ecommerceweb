from django.contrib import admin
from .models import CustomUser, Product
from django.contrib.auth.admin import UserAdmin

# Custom user admin
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (None, {'fields': ('profile_image',)}),
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (None, {'fields': ('name', 'email', 'mobile', 'profile_image')}),
    )

    list_display = ('username', 'email', 'name', 'mobile', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'name', 'mobile')
    ordering = ('username',)

# Product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('price',)
    ordering = ('created_at',)

    def image_tag(self, obj):
        return '<img src="/{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image_url)
    
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
