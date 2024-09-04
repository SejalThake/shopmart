from django.urls import path
from customer import views
urlpatterns = [
    path('', views.home),
    path('register/', views.user_register),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('add-to-cart/<product_id>',views.add_to_cart),
    path('cart/',views.view_cart),
    path('cart/delete/<cart_id>',views.delete_cart_item),
    path('cart/<flag>/<cart_id>',views.update_cart),
    path('category/<categoryId>',views.filterByCategory),
    path('sort-by/<flag>',views.sortByprice),
    path('search/',views.searchByName),
    path('price-range/',views.filterByPriceRange),
    path('profile/',views.updateprofile),
    path('order-summary/',views.order_summary),
]
