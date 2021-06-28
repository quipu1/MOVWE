from rest_framework import serializers
from .models import Movie, Review, Comment, Rank, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    user_picked = serializers.SerializerMethodField('user_valid', read_only=True)
    rank = serializers.SerializerMethodField('user_rank', read_only=True)

    def user_valid(self, movie):
        user = self.context.get('user')
        if movie.picked.filter(pk=user.pk).exists():
            return True
        else:
            return False

    def user_rank(self, movie):
        user = self.context.get('user')
        if movie.rank_set.filter(user=user).exists():
            return movie.rank_set.get(user=user).rank
        else:
            return 0
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'poster_path', 'genres', 'vote_average', 'vote_count', 'user_picked', 'trailer', 'rank')

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rank
        fields = '__all__'
        read_only_fields = ('user', 'movie',)

class ReviewSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    rank = serializers.SerializerMethodField('rank_query', read_only=True)
    username = serializers.SerializerMethodField('user_name', read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    def user_name(self, review):
        return review.user.username

    def rank_query(self, review):
        qs = Rank.objects.get(movie=review.movie, user=review.user)
        serializer = RankSerializer(instance=qs)
        return serializer.data['rank']

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie', 'like_users')

class CommentSerializer(serializers.ModelSerializer):
    user_flag = serializers.SerializerMethodField('user_valid', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    def user_valid(self, comment):
        user = self.context.get('user')
        if user == comment.user:
            return True
        else:
            return False

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review',)

class ReviewDetailSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    user_like = serializers.SerializerMethodField('userlike', read_only=True)
    rank = serializers.SerializerMethodField('rank_query', read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    user_flag = serializers.SerializerMethodField('user_valid', read_only=True)
    movie = serializers.CharField(source='movie.title', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    def userlike (self, review):
        user = self.context.get('user')
        if review.like_users.filter(pk=user.pk).exists():
            return True
        else:
            return False

    def rank_query(self, review):
        qs = Rank.objects.get(movie=review.movie, user=review.user)
        serializer = RankSerializer(instance=qs)
        return serializer.data['rank']

    def user_valid(self, review):
        user = self.context.get('user')
        if user == review.user:
            return True
        else:
            return False
    

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie', 'like_users')

