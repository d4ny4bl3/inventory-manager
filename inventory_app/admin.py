from django.contrib import admin
from .models import Location, Room, Rack, Product, Task


class RoomAdmin(admin.ModelAdmin):
    """Admin konfigurace pro model Room."""
    list_display = ("name", "description")


class RackAdmin(admin.ModelAdmin):
    """Admin konfigurace pro model Rack."""
    list_display = ("display_rack", "total_shelves")
    list_filter = ("room",)

    def display_rack(self, obj):
        """Zobrazení string reprezentace jednotlivých regálů."""
        return str(obj)
    display_rack.short_description = "Regál"


class ProductAdmin(admin.ModelAdmin):
    """Admin konfigurace pro model Product."""
    list_display = ("name", "get_locations", "product_id", "brand", "is_active")
    list_filter = ("is_active", "brand")
    search_fields = ("name", "product_id")
    prepopulated_fields = {"slug": ("name",)}

    def get_locations(self, obj):
        """Získá všechny locations pro daný produtk."""
        return ", ".join([str(location) for location in obj.location.all()])
    get_locations.short_description = 'Umístění'


class TaskAdmin(admin.ModelAdmin):
    """Admin konfigurace pro model Task."""
    list_display = ("task", "is_done")
    list_filter = ("is_done",)


admin.site.register(Location)
admin.site.register(Room, RoomAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Task, TaskAdmin)
