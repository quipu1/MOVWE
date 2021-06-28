from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movie/<int:movie_pk>/', views.movie_one),
    path('movies/pick/', views.movie_pick_list),
    path('genres/', views.movie_genres),
    path('movie/<int:movie_pk>/review/', views.movie_review),
    path('movie/<int:movie_pk>/rank/', views.movie_rank),
    path('movie/<int:movie_pk>/pick/', views.movie_pick),
    path('review/<int:review_pk>/', views.review_detail),
    path('review/<int:review_pk>/comment/', views.review_comment),
    path('comment/<int:comment_pk>/', views.comment_detail),
    path('review/<int:review_pk>/like/', views.review_like),
    path('movies/recommend/', views.movie_recommend),
    path('search/preview/', views.search_preview),
    path('search/', views.search_detail),
]