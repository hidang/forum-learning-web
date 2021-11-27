from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name="question_list"),
    path('create/', views.question_create, name="question_create"),
    path('<slug:tag_name>/', views.question_list, name="question_tag"),
    path('view/<slug:question_id>/', views.question_detail, name="question_detail"),
]
