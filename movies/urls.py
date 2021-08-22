from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('movie/', views.MovieListView.as_view()),
    path('movie/<int:pk>/', views.MovieDetailView.as_view()),
]
