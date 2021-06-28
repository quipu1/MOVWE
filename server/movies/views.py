from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Movie, Review, Comment, Rank, Genre
from .serializers import MovieListSerializer, ReviewSerializer, CommentSerializer, ReviewDetailSerializer, GenreSerializer
from django.db.models import Q


@api_view(['GET'])
# 토큰 기반 인증 중에서 JWT를 활용해서 검증
# 인증 여부와 관계없이 JWT 토큰이 유효한지(정상인지) 파악
@authentication_classes([JSONWebTokenAuthentication])
# 인증이 되는지 확인(로그인 했는지?)
# 인증 데이터가 제공되지 않았습니다. 같은 메세지를 보내줌
@permission_classes([IsAuthenticated])
def movie_list(request):
    movies = get_list_or_404(Movie.objects.order_by('-popularity'))
    serializer = MovieListSerializer(movies, many=True, context={'user': request.user})
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_one(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieListSerializer(movie, context={ 'user' : request.user})
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_pick_list(request):
    user = request.user
    if user.pick.all().exists():
        movies = user.pick.all()
        serializer = MovieListSerializer(movies, many=True, context= {'user' : request.user})
        return Response(serializer.data)
    else:
        return Response({'message': '존재하지 않습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_genres(request):
    genres = get_list_or_404(Genre)
    serializer = GenreSerializer(genres, many=True, context={'user': request.user})
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_review(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 작성된 리뷰들 모두 보여주기
    if request.method == 'GET':
        reviews = movie.review_set.order_by('-pk')
        serializer = ReviewSerializer(reviews, many=True, context={'user': request.user})
        return Response(serializer.data)
    # 새로운 리뷰 작성
    elif request.method == 'POST':
        if not movie.rank_set.all().filter(user=user).exists():
            data = {
                'message': '평점을 먼저 매겨야 합니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(user=user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': '올바르지 않은 형식입니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST', 'GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_rank(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    print('-------here-------', request.data)
    number = request.data['rank']
    # 범위 검사
    if not (1 <= int(number) <= 10):
        data = {
            'message': '유효하지 않은 숫자 범위 입니다.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    origin_vote_count = movie.vote_count
    origin_vote_average = movie.vote_average


    # 수정
    # 이 영화의 랭크를 이 유저가 매겼는지?
    if movie.rank_set.filter(user=user).exists():
            
        rank = movie.rank_set.get(user=user)
        # print('-------here-------', request.data['rank'])
        number = request.data['rank']
        origin_rank = rank.rank
        movie.vote_average = (origin_vote_average*origin_vote_count - origin_rank + int(number)) / origin_vote_count
        movie.save()
        rank.rank = number
        rank.save()

        data = {
            'rank': number
        }
        return Response(data)

    else:
        number = request.data['rank']
        
        rank = Rank(user=user, movie=movie, rank=number)
        rank.save()
        movie.vote_count = origin_vote_count + 1
        movie.vote_average = ((origin_vote_average * origin_vote_count) + int(number)) / (origin_vote_count + 1)
        movie.save()
        data = {
            'rank': number
        }
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST', 'GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_pick(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if request.method == 'POST':
        if movie.picked.filter(pk=user.pk).exists():
            movie.picked.remove(user)
            pick = False
        else:
            movie.picked.add(user)
            pick = True
        data = {
            'pick': pick
        }
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        movies = user.pick.all()
        serializer = MovieListSerializer(movies, many=True, context={'user': request.user})
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)
    
    if request.method == 'GET':
        serializer = ReviewDetailSerializer(review, context={'user': request.user})
        return Response(serializer.data)

    if user != review.user:
        data = {
            'message': '권한이 없습니다.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)
        
    if request.method == 'PUT':
        serializer = ReviewDetailSerializer(instance=review, data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:  
            data = {
                'message': '올바르지 않은 형식입니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        review.delete()
        data = {
            'delete': '리뷰가 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST',])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_comment(request, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(user=user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': '올바르지 않은 형식입니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_pk)
    if user != comment.user:
        data = {
            'message': '권한이 없습니다.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:  
            data = {
                'message': '올바르지 않은 형식입니다.'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        comment.delete()
        data = {
            'delete': '리뷰가 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user

    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        liked = False
    else:
        review.like_users.add(user)
        liked = True
    data = {
        'liked': liked
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_recommend(request):

    user = request.user
    if Rank.objects.filter(user=user).exists():
        genres = Genre.objects.all()
        genre_dic = {}
        for genre in genres:
            genre_dic[genre.pk] = 0

        seen_movies = []

        ranked_movies = user.rank_set.all()
        for ranked_movie in ranked_movies:
            score = (ranked_movie.rank - 5) / 2
            movie = Movie.objects.get(pk=ranked_movie.movie.pk)
            seen_movies.append(ranked_movie.movie.pk)

            for genre in movie.genres.all():
                genre_dic[genre.pk] += score

        result_movies = []
        for movie in Movie.objects.all():
            if movie.pk in seen_movies:
                continue
            score = movie.vote_average

            for genre in movie.genres.all():
                score += genre_dic[genre.pk]
            
            result_movies.append([movie.pk, score])
        
        result_movies.sort(reverse=True, key=lambda x: x[1])
        upper15 = result_movies[:15]
        
        upper2obj = []
        for id, score in upper15:
            movie = Movie.objects.get(pk=id)
            upper2obj.append(movie)

        serializer = MovieListSerializer(upper2obj, many=True, context={'user': request.user})

        return Response(serializer.data)
    else:
        data = {
            'message': 'rank 하나라도 달고와'
        }
        return Response(data, status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def search_preview(request):
    query = request.GET.get('q')
    movie_count = Movie.objects.filter(title__icontains=query).count()
    genre_count = Genre.objects.filter(name__icontains=query).count()
    
    result = {
        'movie_count': movie_count,
        'genre_count': genre_count
    }
    return Response(result)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def search_detail(request):
    query = request.GET.get('q')
    movies = Movie.objects.filter(title__icontains=query)
    genres = Genre.objects.filter(name__icontains=query)

    genre_movie_list = []
    for genre in genres:
        genre_movies = genre.movie_set.all()
        
        for genre_movie in genre_movies:
            if genre_movie.id in genre_movie_list:
                continue
            genre_movie_list.append(genre_movie.id)
    
    genre_data = []
    for movie_id in genre_movie_list:
        movie = Movie.objects.get(pk=movie_id)
        genre_serializer = MovieListSerializer(movie, context={'user': request.user})
        genre_data.append(genre_serializer.data)

    movie_serializer = MovieListSerializer(movies, many=True, context={'user': request.user})
    
    result = {
        'movies': movie_serializer.data,
        'genres': genre_data
    }
    return Response(result)