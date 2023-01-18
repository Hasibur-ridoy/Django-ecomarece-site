from django.urls import path
from . import views 

from django.contrib.auth import views as auth_views

urlpatterns = [
 	
 	path('', views.home, name='home'),
 	path('login/', views.login_page, name='login'),
 	path('logout/', views.logout_page, name='logout'),
 	path('user/', views.user_page, name='user'),
 	path('settings/', views.settings, name='settings'),
 	path('register/', views.register_page, name='register'),
 	path('products/', views.products, name='products'),
 	path('customers/<str:pk>/', views.customers, name='customers'),
 	path('create_order/<str:pk>/', views.create_order, name='create_order'),
 	path('update_order/<str:pk>/', views.update_order, name='update_order'),
 	path('delete_order/<str:pk>/', views.delete, name='delete'),



 	path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),

 	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
 		name="password_reset_done"),

 	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), 
 		name="password_reset_confirm"),

 	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
 		name="password_reset_complete"),



]