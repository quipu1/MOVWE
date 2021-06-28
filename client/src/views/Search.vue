<template>
  <div>
    <div v-if="movies_movies.length || genres_movies.length">
        <h2>"{{ query }}" 영화 검색 결과</h2>
        <div v-if="movies_movies.length">
            <div class="moviecard-container" data-name="movies">
                <MovieCard v-for="(movie, idx) in movies_movies" :key="idx" :movie="movie" @pick="pick"/>
            </div>
        </div>
        <div v-else style="text-align: center;">"{{ query }}"로 검색된 영화 타이틀이 존재하지 않습니다.</div>
        <h2>"{{ query }}" 장르 검색 결과</h2>
        <div v-if="genres_movies.length">
            <div class="moviecard-container" data-name="genres">
                <MovieCard v-for="(movie, idx) in genres_movies" :key="idx" :movie="movie" @pick="pick"/>
            </div>
        </div>
        <div v-else style="text-align: center;">"{{ query }}"로 검색된 장르가 존재하지 않습니다.</div>
        <Modal v-if="modalMovieId" />
    </div>
    <div v-else class="loading">
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
    </div>
  </div>
</template>

<script>
import MovieCard from '@/components/MovieCard.vue'
import Modal from '@/components/Modal.vue'

export default {
    name: 'Search',
    components: {
        MovieCard,
        Modal,
    },
    data: function () {
        return {
            movies_movies: [],
            genres_movies: [],
            load: false,
        }
    },
    watch: {
        query: function () {
            this.movies_movies = []
            this.genres_movies = []
            this.getMovies()
        }
    },
    methods: {
        pick: function (index, pick, target) {
            let current = target
            while(!current.matches('.card-root')) {
                current = current.parentNode
            }
            const dataName = current.parentNode.dataset.name
            if (dataName === 'movies') {
                this.movies_movies[index].user_picked = pick
            }
            console.log(current.parentNode, index, pick)
        },
        getMovies: function() {
            this.$store.dispatch('modalOff')
            console.log(this.$route.query.q)
            this.$store.dispatch('searchDetail', this.$route.query.q)
            .then(res => {
                this.movies_movies = res.movies
                this.genres_movies = res.genres
            })
        },
    },
    computed: {
        modalMovieId: function () {
            return this.$store.state.modalMovieId
        },
        query: function () {
            return this.$route.query.q
        }
    },
    created: function () {
        this.getMovies()
    }
}
</script>

<style>
h2 {
  font-size: 2.5rem;
  text-align: center;
  margin: 1em 0;
}
.moviecard-container {
  width: 100vw;
  display: flex;
  flex-wrap: wrap;
  gap: 4vw 0;
}
</style>