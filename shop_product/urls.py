from django.urls import path
from . import views

app_name = "shop_product"


urlpatterns = [
    path('', views.ProductView.as_view(), name='home_page'),
   
    path('chekout/', views.ChekoutView.as_view(), name='chekout'),

    path('caregory/', views.categories_all, name='categories_all'),

    path('category/<int:pk>/', views.category_by_id, name='category_by_id'),

    path('brand/<int:pk>/', views.brand_by_id, name='brand'),

    path('product_detail/<slug:slug>/', views.ProductDetailView.as_view(), name='pro_detail'),

    path('my_cart/', views.MyCartView.as_view(), name='mycart'),

    path('add-to-cart/<int:pro_id>/', views.AddToCartView.as_view(), name='add_to_cart'),

    path('manager-cart/<int:cp_id>/', views.ManagerCartView.as_view(), name='manager'),

    path('all_delete/', views.AllDeleteView.as_view(), name='alldelete'),

    path('delete/<int:id>/', views.delete_product, name='delete_product'),

    path('product_edit/<int:pk>/', views.ProductEdit.as_view(), name='product_edit'),

    path('search/', views.search, name='search'),

    path('order_detail/<int:pk>/', views.UserOrderDetaile.as_view(), name='order_detail'),

    path('order/', views.orderview, name='myorder'),
]