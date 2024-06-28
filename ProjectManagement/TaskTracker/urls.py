from django.urls import path
from .views import *

app_name = 'projects'

urlpatterns = [
    path('create/', project_create, name='project_create'),
    path('details/', project_detail, name='project_detail'),
    path('update/<int:pk>', project_update, name='project_update'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),
    path('project/<int:project_id>/task/create/', create_task, name='create_task'),
    path('tasks/<int:id>/', task_list, name='task_list'),
    path('task/<int:pk>/', task_detail, name='task_detail'),
    path('task/<int:pk>/update/', update_task, name='update_task'),
    path('task/<int:pk>/delete/', delete_task, name='delete_task'),
]
