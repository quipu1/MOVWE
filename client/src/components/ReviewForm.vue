<template>
  <div class="review-form-container">
    <div v-if="review !== null">
      <h1>{{ movie.title }} 리뷰 수정 </h1>
      <form @submit.prevent="submitReview" class="review-form">
        <label for="title">리뷰 제목</label>
        <input id="title" type="text" name="title" v-model="title" placeholder="리뷰 제목을 작성하세요. 100자 이내">
        <label for="content">리뷰 내용</label>
        <textarea id="content" name="content" placeholder="리뷰 내용을 작성하세요." v-model="content"></textarea>
        <div class="review-button-container">
          <button type="submit" class="submit-btn review-btn">수정 완료</button>
          <button class="review-btn back-btn" @click="backPage">목록으로</button>
        </div>
      </form>
    </div>
    <div v-else>
      <h1>{{ movie.title }} 리뷰 생성</h1>
      <form @submit.prevent="submitReview" class="review-form">
        <input type="text" name="title" placeholder="리뷰 제목을 작성하세요. 100자 이내">
        <textarea name="content" placeholder="리뷰 내용을 작성하세요."></textarea>
        <div class="review-button-container">
          <button type="submit" class="submit-btn review-btn">작성 완료</button>
          <button class="review-btn back-btn" @click="backPage">목록으로</button>
        </div>
      </form>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'ReviewForm',
  props: {
    movie: Object,
    review: {
      type: Object,
      default: null
    }
  },
  data: function () {
    return {
      content: '',
      title: '',
    }
  },
  methods: {
    backPage: function () {
      this.$router.push({ name: 'ReviewList', params: { id: this.movie.id } })
    },
    submitReview: function (e) {
      if (this.review) {
        const params = {
          reviewId: this.review.id,
          form: e.target
        }
        this.$store.dispatch('reviewModify', params)
        .then(() => {
          this.$router.push({ name : 'Review', params: { id: this.review.id } })
        })
        .catch(err => {
          if (err.message === '403') {
            alert('권한이 없습니다.')
            this.$router.push({ name: 'Home' })
          } else {
            alert('잘못된 형식입니다.')
          }
        })
      } else {
        const params = {
            movieId: this.movie.id,
            form: e.target,
        }
        this.$store.dispatch('review_create', params)
        .then(res => {
          this.$router.push( { name: 'Review', params: { id: res.id } } )
        })
        .catch(err => {
            if (err.message === '401') {
                alert('로그인 세션이 만료되었습니다.')
                this.$store.dispatch('logOut')
                this.$router.push({ name: 'Login' })
            } else {
                alert(err.message)
            }
        })
      }
    }
  },
  created: function () {
    if(this.review) {
      this.content = this.review.content;
      this.title = this.review.title;
    }
  }
}
</script>

<style scoped>
  .review-form-container {
    width: 100%;
  }
  h1 {
    text-align: center;
    font-size: 2rem;
    font-weight: bold;
    margin: 1em 0;
  }
  .review-form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
  }
  .review-form > label {
    margin-bottom: .3rem;
  }
  .review-form > input,
  .review-form > textarea {
    width: 100%;
    border-radius: 5px;
    margin-bottom: .8rem;
    font-size: 1.2rem;
  }
  .review-form > *:focus {
    outline: none;
  }
  .review-form > input {
    height: 2rem;
  }
  .review-form > textarea {
    height: 20rem;
  }
  .review-button-container {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  .review-btn {
    font-weight: bold;
    color: white;
    border: none;
    border-radius: 5px;
    padding: .5em;
    margin: 0 .3em;
  }
  .submit-btn {
    background: #6f42c1;
  }
  .back-btn {
    background: #adb5bd;
  }
</style>