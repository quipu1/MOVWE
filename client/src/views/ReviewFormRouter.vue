<template>
  <div>
    <div v-if="movie && review !== undefined">
      <ReviewForm :movie="movie" :review="review" />
    </div>
  </div>
</template>

<script>
import ReviewForm from '@/components/ReviewForm.vue'
export default {
  name: 'ReviewFormRouter',
  components: {
    ReviewForm,
  },
  data: function () {
    return {
      movie: null,
      review: undefined,
    }
  },
  created: function () {
    const movieId = this.$route.params.id
    this.$store.dispatch('getMovieOne', movieId)
    .then(res => {
      this.movie = res
      if (this.$route.query.reviewid) {
        console.log(this.movie)
        const reviewId = this.$route.query.reviewid
        this.$store.dispatch('getReviewDetail', reviewId)
        .then(res => {
            if (!res.user_flag) {
              alert('권한이 없습니다.')
              this.$router.push({ name: 'Home' })
            }
            if (res.movie_id !== this.movie.id) {
              alert('잘못된 접근입니다.')
              this.$router.push({ name: 'Home' })
            }
            this.review = res
        })
      .catch(err => {
          if (err.message === '401') {
              alert('로그인 세션이 만료되었습니다.')
              this.$store.dispatch('logOut')
              this.$router.push({ name: 'Login' })
          } else {
              alert('존재하지 않는 게시물 입니다.')
              this.$router.push({ name: 'Home' })
          }
      })
    }
    else this.review = null;
    })
    .catch(err => {
      if (err.message === '404') {
        alert('존재하지 않는 영화 입니다.')
        this.$router.push({ name: 'Home' })
      } else {
        alert(err.message)
      }
    })
  }
}
</script>

<style>
</style>