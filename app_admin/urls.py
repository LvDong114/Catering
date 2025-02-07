from django.urls import path
from .views import AddOrdersView

urlpatterns = [
    path('add_orders/', AddOrdersView.as_view(), name='add_orders'),
    # 其他路由...
] 