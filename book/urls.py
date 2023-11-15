from django.urls import path
from . import views

urlpatterns = [
    path('type/<slug:slug>/', views.type, name='type'),
    path('genre/<slug:slug>/', views.genre, name='genre'),
    path('<slug:slug>/', views.hot_cate, name='hot-cate'),
    path('book/<slug:slug>/', views.book_detail, name="book-detail"),
    path('read/<slug:slug>/<str:chap>/', views.read_book, name="read-book"),
    path('read/<slug:slug>/', views.read_book, name="read-book-first"),
    
    path('filter', views.filter, name='filter'),
    path('random', views.random, name='random'),
    path('az-list', views.az_list, name='az-list'),
    path('az-list/<str:alpha>/', views.az_list, name='az-list'),
    path('ajax/book/search/suggest', views.suggest, name="suggest"),
    path('ajax/vote/submit', views.vote, name="vote"),
    path('ajax/book/count-view/<int:pk>', views.count_view, name="count-view"),
    path('search', views.search, name="search"),
]
