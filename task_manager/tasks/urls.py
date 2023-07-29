from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.TasksListView.as_view(),
         name='tasks_list'),
    path('create/', views.TaskCreationView.as_view(),
         name='task_create'),
    path('<int:pk>/', views.TaskDetailView.as_view(),
         name='task_detail'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(),
         name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(),
         name='task_delete'),
]