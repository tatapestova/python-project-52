from django.contrib import admin
from django.urls import include, path
from task_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('users/', include('task_manager.users.urls')),
]
