<template>
  <div>
        <h1>내가 찜한 영화 목록</h1>
        <div v-if="movies.length && load">
            <div class="moviecard-container">
                <MovieCard v-for="(movie, idx) in movies" :key="idx" :movie="movie" :index="idx" @pick="pick"/>
            </div>
            <Modal v-if="modalMovieId" />
        </div>
        <div v-else-if="load" style="text-align: center; margin: 1rem 0;">
            정보가 존재하지 않습니다.
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
    name: 'MoviePick',
    components: {
        MovieCard,
        Modal,
    },
    data: function () {
        return {
            movies: [],
            load: false,
        }
    },
    methods: {
        pick: function (index, pick) {
            this.movies[index].user_picked = pick
        }
    },
    computed: {
        modalMovieId: function () {
            return this.$store.state.modalMovieId
        },
    },
    created: function () {
        this.$store.dispatch('modalOff')
        this.$store.dispatch('getMoviePick')
        .then(res => {
            this.movies = res
            this.load = true
        })
        .catch(err => {
            if (err.message === '204') {
                alert('찜한 영화가 존재하지 않습니다.')
                this.$router.push({ name: 'Home' })
            } else if (err.message === '401') {
                alert('로그인 세션이 만료되었습니다.')
                this.$store.dispatch('logOut')
                this.$router.push({ name: 'Login' })
            } else {
                alert('알 수 없는 오류')
                this.$router.push({ name: 'Home' })
            }
        })
    }
}
</script>

<style>
h1 {
  font-size: 3rem;
  text-align: center;
  margin-bottom: .5em;
}
.moviecard-container {
  width: 100vw;
  display: flex;
  flex-wrap: wrap;
  gap: 4vw 0;
}
</style>