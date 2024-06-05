from django.urls import path, include

from users import views

urlpatterns = [
    path('signin', views.SignInView.as_view(), name='login'),
    path('user/add', views.UserCreateView.as_view()),
    path('user/update', views.UserUpdateView.as_view()),
    path('user', views.UserListView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    path('role/add', views.RoleCreateView.as_view()),
    path('role/update', views.RoleUpdateView.as_view()),
    path('role', views.RoleListView.as_view()),
    path('role/<int:pk>/', views.RoleDetailView.as_view()),
]
