from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.welcome,name= 'welcome_page'),
    path('history/',views.our_bank,name= 'our_bank'),
    path('register/', views.register_user, name='register_user'),
    path('login/', auth_views.LoginView.as_view(template_name='login_user.html'), name='login_user'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout_user.html'), name='logout_user'),
    path('create/',views.create_account, name = 'create_account' ),
    path('profile/',views.profile_page, name= 'user_profile'),
    path('profile/<str:acc_number>/', views.account, name='account'),
    path('profile/<str:acc_number>/transfer', views.send_moneys, name='transfer2'),
    path('my_transactions/',views.my_transactions, name= 'my_transactions'),
    path('send_money/', views.send_balance_form, name='transfer3'),
    path('send_moneys/', views.send_balance, name='transfer'),
]