from django.urls import path
from . import views

urlpatterns = [
    # Главная страница сайта (CMS)
    path('', views.home_page, name='home'),

    # Список тестов
    path('tests/', views.index, name='test_index'),

    # Прохождение теста
    path('test/<int:test_id>/', views.test, name='test'),

    # Результаты конкретного пользователя
    path('results/<str:student_name>/', views.result_list, name='result_list'),

    # Просмотр всех результатов (для админа)
    path('results/', views.results_list_all, name='results_all'),

    # CMS-страницы по slug — должно быть последним
    path('<slug:slug>/', views.page_view, name='page'),
]