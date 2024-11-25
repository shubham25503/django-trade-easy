from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('stockmarket/', views.stockmarket, name='stockmarket'),
    path('marketnews/', views.marketnews, name='marketnews'),
    path('cryptocurrency/', views.cryptocurrency, name='cryptocurrency'),
    path('mailinbox/', views.mailinbox, name='mailinbox'),
    path('authlogin/', views.authlogin, name='authlogin'),
    path('authregister/', views.authregister, name='authregister'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('buycrypto/', views.buycrypto, name='buycrypto'),
    path('sellcrypto/', views.sell_crypto, name='sellcrypto'),
    path('logout/', views.logout, name='logout'),
    #path('delete/<item_id>', views.delete, name='delete'),
    #path('crossoff/<item_id>', views.cross_off, name='cross_off'),
    #path('uncross/<item_id>', views.uncross, name='uncross'),
    #path('edit/<item_id>', views.edit, name='edit'),
]
