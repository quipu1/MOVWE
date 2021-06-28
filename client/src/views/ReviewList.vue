<template>
<div>
  <div class="review-list-container" v-if="reviews.length && movie">
      <h1>{{ movie.title }} 영화 리뷰 목록</h1>
      <ReviewCard v-for="(review, idx) in reviews" :key="idx" :review="review" />
      <button class="btn" @click="goReviewForm">리뷰 생성</button>
  </div>
  <div v-else class="loading">
      <div class="circle"></div>
      <div class="circle"></div>
      <div class="circle"></div>
    </div>
</div>
</template>

<script>
import ReviewCard from '@/components/ReviewCard.vue'
export default {
    name: 'ReviewList',
    components: {
        ReviewCard,
    },
    data: function () {
        return {
            reviews: [],
            movie: null,
        }
    },
    methods: {
        goReviewForm: function () {
            this.$router.push({ name: 'ReviewFormRouter', params: { id: this.movie.id } })
        }
    },
    created: function () {
        this.$store.dispatch('modalOff')
        const movieId = this.$route.params.id
        this.$store.dispatch('getReviewList', movieId)
        .then(res => {
            if (!res.length) {
                alert('해당 영화의 리뷰가 존재하지 않습니다')
                this.$router.push({ name: 'Home' })
            }
            this.reviews = res;
        })
        .catch(err => {
            if(err.message === '401') {
                alert('로그인 세션이 만료되었습니다.')
                this.$store.dispatch('logOut')
                this.$router.push({ name: 'Login' })
            } else if(err.message === '404') {
                alert('존재하지 않는 영화입니다.')
                this.$router.push({ name : 'Home' })
            } else {
                alert('알 수 없는 오류입니다.')
            }
        })
        this.$store.dispatch('getMovieOne', movieId)
        .then(res => {
            this.movie = res
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

<style scoped>
.review-list-container {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100vw;
}
h1 {
    font-size: 2rem;
    font-weight: bold;
}
.btn {
    position: sticky;
    bottom: 10px;
    border: 2px solid #222;
}
</style>