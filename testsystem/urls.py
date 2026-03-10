from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/<int:test_id>/', views.test, name='test'),
    path('results/<str:student_name>/', views.result_list, name='result_list'),  # только свои
    path('results/', views.results_list_all, name='results_list'),                # все результаты
    path('', views.home_page, name='home'),  # главная страница
    path('admin/', admin.site.urls),  # админка
]