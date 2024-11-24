from django.contrib import admin
from .models import Category, Product, Vendor, Purchase, StockMovement, DieselTracker



admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(Purchase)
admin.site.register(StockMovement)
admin.site.register(DieselTracker)
