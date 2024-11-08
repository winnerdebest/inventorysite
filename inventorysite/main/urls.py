from django.urls import path 
from . import views 

urlpatterns = [
    # Login and Log out URLS
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Inventory Manager URLs
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('inventory_dashboard/', views.inventory_dashboard, name='inventory_dashboard'),
    path('register/', views.register, name='register'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_stock_movement/', views.add_stock_movement, name='add_stock_movement'),
    path('success/', views.success, name='success'),
    path('product/<int:product_id>/purchases/', views.product_purchases, name='product_purchases' ),
    # End of Inventory Managers Page

    # Supervisors Page
    path('supervisor_dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('request_purchase/<int:product_id>/', views.request_purchase, name='request_purchase'),
]
    

