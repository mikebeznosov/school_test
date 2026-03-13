from django.urls import path
from . import views

urlpatterns = [
    # Главная страница / CMS
    path('', views.home_page, name='home'),

    # Страница с тестами по предмету
    path('tests/<str:subject>/', views.tests_by_subject, name='tests_by_subject'),

    # Поиск тестов
    path('tests/search/', views.tests_search, name='tests_search'),

    # Прохождение теста
    path('test/<int:test_id>/', views.test, name='test'),

    # Результат конкретного теста
    path('result/<int:result_id>/', views.result_detail, name='result_detail'),

    # Список результатов ученика
    path('results/<str:student_name>/', views.result_list, name='result_list'),

    # Все результаты
    path('results/', views.results_list_all, name='results_list_all'),

    # CMS страницы
    path('page/<slug:slug>/', views.page_view, name='page'),
]