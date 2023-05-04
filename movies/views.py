from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, Request
from movies.permissions import Employee_Permission
from movies.serializers import MovieSerializer, MovieOrderSerializer
from movies.models import Movie
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [Employee_Permission]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, 201)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [Employee_Permission]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)

        return Response(serializer.data, 200)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()

        return Response(status=204)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        movie_instance = get_object_or_404(Movie, id=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie=movie_instance)
        return Response(serializer.data, 201)
