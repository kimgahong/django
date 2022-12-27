from django.urls import path

from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('ranking', views.ranking, name='ranking'),
    path('sudoku/ranking/register', views.register_ranking, name='register_ranking'),
    path('sudoku/ranking', views.get_ranking_list, name='get_ranking_list'),
    path('sudoku/check', views.check_sudoku, name='check_sudoku'),
    path('sudoku/make', views.make_sudoku, name='make_sudoku'),
]