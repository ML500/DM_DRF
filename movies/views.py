from django.db import models
from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.views import APIView
from .models import Movie, Actor
from .serializer import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorsListSerializer,
    ActorsDetailSerializer)
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    # def get(self, request):
    #     movies = Movie.objects.filter(draft=False).annotate(
    #         rating_user=models.Case(
    #             models.When(ratings__ip=get_client_ip(request), then=True),
    #                 default=False,
    #                 output_field=models.BooleanField()
    #             ),
    #     )
    # APIView
    # def get(self, request):
    #     movies = Movie.objects.filter(draft=False).annotate(
    #         rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
    #     ).annotate(
    #         middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
    #     )
    #     serializer = MovieListSerializer(movies, many=True)
    #     return Response(serializer.data)


# class MovieDetailView(APIView):
#     def get(self, request, pk):
#         movie = Movie.objects.get(id=pk, draft=False)
#         serializer = MovieDetailSerializer(movie)
#         return Response(serializer.data)

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


# class ReviewCreateView(APIView):
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer


# class AddStarRatingView(APIView):
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)

class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorsListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorsDetailSerializer
