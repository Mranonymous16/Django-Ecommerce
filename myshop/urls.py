from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import MyLoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart'),
    # path('cart/update/<int:item_id>/', views.update_quantity, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.order_history, name='order_history'),
    path('add-product/', views.add_product, name='add_product'),

    path('accounts/login/', MyLoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', views.user_register, name='register'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)