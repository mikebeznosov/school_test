from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home_page, name='home'),

    # Страницы по предмету: /pages/algebra/, /pages/geometry/, /pages/physics/
    path('pages/<str:subject>/', views.home_page, name='pages_by_subject'),

    # Список всех тестов
    path('tests/', views.index, name='index'),

    # Прохождение теста
    path('test/<int:test_id>/', views.test, name='test'),

    # Результаты конкретного ученика
    path('results/<str:student_name>/', views.result_list, name='result_list'),

    # Просмотр всех результатов (для админа)
    path('results/', views.results_list_all, name='results_all'),

    # Детальный разбор теста
    path('result/<int:result_id>/', views.result_detail, name='result_detail'),

    # CMS-страницы по slug — всегда последним
    path('<slug:slug>/', views.page_view, name='page'),
]