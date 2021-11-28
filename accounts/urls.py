from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="accounts_login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/<slug:username>/', views.profile_user,
         name="accounts_profile_user"),
    path('profile/me', views.profile_me, name="accounts_profile_me")
]
