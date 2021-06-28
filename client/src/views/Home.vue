<template>
  <div class="home">
    <div v-if="loadPopularMovieList && loadGenreList">
      <HomeMain />
      <MovieList :movies="popularMovies" />
      <MovieList v-for="(genreObj, idx) in genreMovies" :key="idx" :movies="genreObj.data" :genre="genreObj.name" />
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
import HomeMain from '@/components/HomeMain.vue'
import MovieList from '@/components/MovieList.vue'
import Modal from '@/components/Modal.vue'
import _ from 'lodash'

export default {
  name: 'Home',
  components: {
    MovieList,
    Modal,
    HomeMain,
  },
  data: function () {
    return {
      listCount: 0,
      loadPopularMovieList: false,
      loadGenreList: false,
    }
  },
  computed: {
    popularMovies: function () {
      return this.$store.getters.popularMovieList.slice(0, 20)
    },  
    genreMoviesArray: function () {
      return this.$store.getters.genreMoviesArray
    },
    modalMovieId: function () {
      return this.$store.state.modalMovieId
    },
    genreMovies: function () {
      return this.genreMoviesArray.map(item => {
        return {
          name: item.name,
          data: this.randomList(item.data)
        }
      })
    }
  },
  methods: {
    resizeHandler: function () {
      document.querySelectorAll('.card-list').forEach((item) => {
        item.style.marginLeft = `-${0}vw`;
      })
    },
    randomList: function (movieList) {
      return movieList.length > 20 ? _.sampleSize(movieList, 20) : _.sampleSize(movieList, movieList.length)
    },
  },
  created: function () {
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
  },
  mounted: function () {
    window.addEventListener('resize', this.resizeHandler)
  },
  destroyed: function () {
    window.removeEventListener('resize', this.resizeHandler)
  }
}
</script>

<style scoped>
.home {
  margin-bottom: 2rem;
  overflow-x: hidden;
}

</style>
