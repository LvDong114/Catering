"""
URL configuration for Catering project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

from app_admin import views
from app_admin.views import AddOrdersView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('admin/',views.admin_board,name='admin'),
    path('admin/dish_management/',views.dish_management,name='dish-management'),
    path('admin/edit_dish/<int:dish_id>/', views.edit_dish, name='edit-dish'),
    path('admin/delete_dish/<int:dish_id>/', views.delete_dish, name='delete-dish'),
    path('admin/add_dish/', views.add_dish, name='add-dish'),

    path('admin/category_management/',views.category_management,name='category-management'),
    path('admin/edit_category/<int:category_id>/', views.edit_category, name='edit-category'),
    path('admin/delete_category/<int:category_id>/', views.delete_category, name='delete-category'),
    path('admin/add_category/', views.add_category, name='add-category'),

    path('admin/announcement_management/', views.announcement_management, name='announcement-management'),
    path('admin/add_announcement/', views.add_announcement, name='add-announcement'),
    path('admin/edit_announcement/<int:announcement_id>/', views.edit_announcement, name='edit-announcement'),
    path('admin/delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete-announcement'),

    path('admin/user_management/', views.user_management, name='user-management'),
    path('admin/delete_user/<int:user_id>/', views.delete_user, name='delete-user'),

    path('admin/order_management/', views.order_management, name='order-management'),
    path('admin/delete_order/<int:order_id>/', views.delete_order, name='delete-order'),
    path('admin/order_detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('admin/update_order_status/<int:order_id>/', views.update_order_status, name='update-order-status'),

    path('api/orders/', views.get_orders, name='get_orders'),
    path('api/get_orderItems/', views.get_orderItems_by_order_id, name='get_orderItems'),
    path('api/add_orders/', AddOrdersView.as_view(), name='add_orders'),
    path('api/login/', views.mini_program_login, name='mini_program_login'),
    path('api/categories/',views.get_categories,name='get_categories'),
    path('api/dishes/', views.get_dishes_by_category, name='get_dishes_by_category'),
    path('api/get_announcements/', views.get_announcements, name='get_announcements'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
