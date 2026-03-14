from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),

    # поиск должен быть ВЫШЕ
    path('tests/search/', views.tests_search, name='tests_search'),

    # тесты по предмету
    path('tests/live-search/', views.tests_live_search, name='tests_live_search'),
    path('tests/<str:subject>/', views.tests_by_subject, name='tests_by_subject'),

    path('test/<int:test_id>/', views.test, name='test'),
    path('result/<int:result_id>/', views.result_detail, name='result_detail'),
    path('results/<str:student_name>/', views.result_list, name='result_list'),
    path('results/', views.results_list_all, name='results_list_all'),
    path('page/<slug:slug>/', views.page_view, name='page'),

]