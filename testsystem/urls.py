from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/<int:test_id>/', views.take_test, name='take_test'),
    path('results/<str:student_name>/', views.result_list, name='result_list'),  # только свои
    path('results/', views.results_list_all, name='results_list'),                # все результаты
]