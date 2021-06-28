<template>
  <div>
    
    <h1>{{ genre }} 영화 목록</h1>
    <div v-if="movies.length">
      <div class="moviecard-container">
        <MovieCard v-for="(movie, idx) in movies" :key="idx" :movie="movie"/>
      </div>
      <Modal v-if="modalMovieId" />
    </div>
    <div v-else style="text-align: center; margin: 1rem 0;">
      정보가 존재하지 않습니다.
    </div>
  </div>
</template>

<script>
import MovieCard from '@/components/MovieCard.vue'
import Modal from '@/components/Modal.vue'

export default {
  name: 'Genre',
  components: {
    MovieCard,
    Modal,
  },
  data: function () {
    return {
      genre: this.$route.params.name,
    }
  },
  computed: {
    movies: function () {
      const movies = []
      this.$store.state.movieList.forEach(movie => {
        for (let i=0; i < movie.genres.length; i++) {
          if (movie.genres[i].name === this.genre) {
            movies.push(movie);
            break;
          }
        }
      })
      return movies
    },
    modalMovieId: function () {
      return this.$store.state.modalMovieId
    },
  },
  created: function () {
    window.scrollTo(0, 0);
    if (this.$store.state.movieList.length === 0) {
        this.$store.dispatch('getMovieList')
      .then(() => {
        this.loadPopularMovieList = true
      })
      .catch(err => {
        if(err.message === '401') {
          alert('로그인 세션이 만료되었습니다.')
          this.$store.dispatch('logOut')
          this.$router.push({ name: 'Login' })
        }
      })
      this.$store.dispatch('getGenreList')
      .then(() => {
        this.loadGenreList = true
      })
      .catch(err => {
        if(err.message === '401') {
          alert('로그인 세션이 만료되었습니다.')
          this.$store.dispatch('logOut')
          this.$router.push({ name: 'Login' })
        }
      })
    }
  }
}
</script>

<style scoped>
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