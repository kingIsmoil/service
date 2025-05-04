from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('create/', views.problem_create, name='problem_create'),
    path('problem/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('problem/<int:pk>/apply/', views.application_create, name='application_create'),
    path('problem/<int:pk>/accept/<int:app_id>/', views.application_accept, name='application_accept'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='problem_list'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('problem/<int:pk>/edit/', views.problem_edit, name='problem_edit'),
    path('problem/<int:pk>/delete/', views.problem_delete, name='problem_delete'),
    path('application/<int:pk>/edit/', views.application_edit, name='application_edit'),
    path('application/<int:pk>/delete/', views.application_delete, name='application_delete'),
]