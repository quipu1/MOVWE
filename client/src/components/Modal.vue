<template>
  <div class="background" @click="modalClicked">
    <div class="article">
      <div class="article-content" v-if="movie && reviewLoad">
        <div class="video-container">
          <iframe :src="videoSrc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"></iframe>
        </div>
        <div class="movie-info">
            <h3>{{ movie.title }}</h3>
            <p>{{ movie.overview }}</p>
        </div>
        <hr>
        <div class="star-rating-container">
            <h3>별점을 선택해주세요.</h3>
            <StarRating :increment="0.5" :border-width="3" :show-rating="false" :star-size="30" :rating="rating" @rating-selected="setRating"/>
        </div>
        <hr>
        <div class="review-header">
            <h4>리뷰 목록</h4>
            <button class="btn form-open" @click="openForm">리뷰 작성</button>
        </div>
        <div class="form-container">
            <form class="review-form" @submit.prevent="reviewSubmit">
                <input type="text" name="title" placeholder="리뷰 제목을 작성하세요. 100자 이내">
                <textarea name="content" id="content" cols="30" placeholder="리뷰 내용을 작성하세요."></textarea>
                <button type="submit" class="btn">작성 완료</button>
            </form>
            <div class="close-container">
                <div class="pin"></div>
                <button class="btn" @click="closeForm"><i class="fas fa-chevron-up"></i></button>
            </div>
        </div>
        <div v-if="reviews.length" class="review-list-container">
            <ReviewCard v-for="(review, idx) in reviews" :key="idx" :review="review" />
            <button class="btn" @click="goReviewList">리뷰 전체 보기</button>
        </div>
        <h4 v-else>아직 작성된 리뷰가 없습니다.</h4>
        
      </div>
      <div class="loading" v-else>
          <div class="circle"></div>
          <div class="circle"></div>
          <div class="circle"></div>
      </div>
    </div>
  </div>
</template>

<script>
import StarRating from 'vue-star-rating'
import ReviewCard from './ReviewCard.vue'

export default {
  name: 'Modal',
  data: function() {
    return {
      movie: null,
      reviews: null,
      reviewLoad: false,
      rating: 0,
    }
  },
  components: {
      StarRating,
      ReviewCard,
  },
  computed: {
      videoSrc: function () {
        return 'https://www.youtube.com/embed/' + this.movie.trailer + '?autoplay=1&mute=1'
      }
  },
  methods: {
    modalClicked: function (e) {
        if (e.target.matches('.background')){
            this.$store.dispatch('modalOff');
        }
    },
    openForm: function () {
        const formContainer = document.querySelector('.form-container');
        let height = 0;
        formContainer.childNodes.forEach(node => {
            height += node.getBoundingClientRect().height;
        })
        formContainer.style.height = `${height}px`;
        formContainer.classList.add('open');
    },
    closeForm: function () {
        const formContainer = document.querySelector('.form-container');
        formContainer.style.height = `0`;
        formContainer.classList.remove('open');
    },
    setRating: function (rating) {
        const rating2str = String(rating*2)
        const params = {
            movieId: this.movie.id,
            rating: rating2str
        }
        this.$store.dispatch('setRate', params)
        .catch(err => {
            alert(err.message + ': 예기치 못한 오류 발생')
            this.$router.go(this.$router.currentRoute)
        })
    },
    reviewSubmit: function (e) {
        const params = {
            movieId: this.movie.id,
            form: e.target,
        }
        this.$store.dispatch('review_create', params)
        .then(res => {
            if(this.reviews.length === 5) this.reviews.pop();
            this.reviews.unshift(res)
            this.closeForm()
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
    },
    goReviewList: function () {
        this.$router.push({ name: 'ReviewList', params: { id: this.movie.id } })
    }
  },
  created: function () {
    for(let i = 0; i < this.$store.state.movieList.length; i++) {
        const movie = this.$store.state.movieList[i]
        if(movie.id == this.$store.state.modalMovieId) {
            this.movie = movie;
            this.rating = movie.rank / 2
            break;
        }
    }
    this.$store.dispatch('getReviewList', this.movie.id)
    .then(res => {
        this.reviews = res.slice(0, 5);
        this.reviewLoad = true;
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
  },
  mounted: function () {
    const article = document.querySelector('.article')
    const { top, left, width, height } = this.$store.state.scaleCard.getBoundingClientRect()
    article.style.position = 'absolute';
    article.style.top = `${top}px`
    article.style.left = `${left}px`
    article.style.width = `${width}px`
    article.style.height = `${height}px`
    setTimeout(() => {
        article.style.transition = '.4s';
        let bwidth;
        let bleft;
        if (window.innerWidth - 6*16 > 1200) {
            bwidth = 1200;
            bleft = (window.innerWidth - 1200) / 2
        } else {
            bwidth = window.innerWidth - 6*16
            bleft = 3*16;
        }
        article.style.top = `1rem`;
        article.style.left = `${bleft}px`;
        article.style.width = `${bwidth}px`;
        article.style.height = '100%';
        setTimeout(() => {
            article.style = '';
        }, 500);
    }, 0)
  }
}
</script>

<style scoped>
    .background {
        position: fixed;
        overflow-y: scroll;
        background-color: rgba(0, 0, 0, 0.5);
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1000;
        padding: 1rem 3rem;
    }
    .article {
        width: 100%;
        max-width: 1200px;
        background-color: #222;
        border-radius: 10px;
        margin: 0 auto;
        color: white;
    }
    .loading {
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .loading > .circle {
        width: 20px;
        height: 20px;
        background: white;
        margin: .8rem;
        border-radius: 50%;
        animation: circleMove infinite alternate .6s;
    }
    .loading > .circle:nth-child(2) {
        animation-delay: .2s;
    }
    .loading > .circle:nth-child(3) {
        animation-delay: .4s;
    }
    .article-content {
        width: 100%;
        padding: 1rem;
    }
    .video-container {
        position: relative;
        width: 100%;
        padding-bottom: 56.25%;
    }
    .video-container > iframe {
        position: absolute;
        width: 100%;
        height: 100%;
    }
    .star-rating-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .star-rating-container > h3 {
        font-size: 1.3rem;
        margin: 1em 0;
        color: #ffd055;
    }
    .movie-info {
        margin: 1rem;
    }
    .movie-info > h3{
        font-size: 2rem;
        text-align: center;
        margin: 1em 0;
        font-weight: bold;
    }
    .movie-info > p{
        font-size: 1.2rem;
        line-height: 1.5;
    }
    
    h4{
        font-size: 1.6rem;
        margin: 1em 0;
        font-weight: bold;
    }
    .article-content > h4 {
        text-align: center;
    }
    .article-content > * {
        z-index: 1;
    }
    .form-container {
        overflow: hidden;
        z-index: 0;
        height: 0;
        transition: .5s;
    }
    .form-container > * {
        transform: translate3d(0, -100%, 0);
        transition: .5s;
    }
    .review-form {
        padding: 1rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .review-form > textarea,
    .review-form > input {
        width: 100%;
        border-radius: 10px;
        margin: .5rem 0;
        font-size: 1.2rem;
    }
    .review-form > input {
        height: 2rem;
    }
    .review-form > textarea {
        height: 5rem;
    }
    .review-form > *:focus {
        outline: none;
    }
    
    .open > * {
        transform: translate3d(0, 0, 0);
    }
    .review-header {
        position: relative;
        display: flex;
        justify-content: center;
    }
    .btn.form-open {
        position: absolute;
        right: 10px;
        top: 50%;
        bottom: auto;
        transition: 0s;
        transform: translate3d(0, -50%, 0);
    }

    .close-container {
        position: relative;
        display: flex;
        justify-content: center;
    }
    .close-container > .pin {
        position: absolute;
        width: 100%;
        border: 1px solid white;
        top: 50%;
        transform: translate3d(0, -50%, 0);
        z-index: 0;
    }
    .close-container > .btn {
        z-index: 100;
        border-radius: 50%;
        font-size: 20px;
        width: 40px;
        height: 40px;
    }

    .review-list-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    @keyframes circleMove {
        from {
            transform: translate3d(0, 0, 0);
        }
        to {
            transform: translate3d(0, -80%, 0);
        }
    }
</style>