<template>
  <div class="card-root">
    <div class="card-container" @mouseenter="mouseEnter" @mouseleave="mouseLeave" :data-movie="movie.id">
      <img :src="movie.poster_path" alt="포스터 이미지">
      <div class="detail">
        <div class="video-container">
          <iframe :data-src="videoSrc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"></iframe>
        </div>
        <div class="detail-description">
          <div class="rating-container">
            <StarRating :increment="0.5" :star-size="25" :read-only="true" :rating="movie.vote_average/2" :show-rating="false"/>
            <div>{{ movieRateRounded }}</div>
          </div>
          <div class="header">
            <h3>{{ movie.title }}</h3>
            <div class="button-container">
              <button @click="pickClick">
                <i class="fas fa-check" v-if="picked"></i>
                <i class="fas fa-plus" v-else></i>
              </button>
              <button @click="modalOpen"><i class="fas fa-info"></i></button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StarRating from 'vue-star-rating'
export default {
  name: 'MovieCard',
  components: {
    StarRating
  },
  props: {
    movie: Object,
    index: {
      type: Number,
      default: 0
    }
  },
  data: function () {
    return {
      videoSrc: 'https://www.youtube.com/embed/' + this.movie.trailer + '?autoplay=1&mute=1',
      scaleCard: null,
    }
  },
  computed: {
    movieRateRounded: function () {
      return this.movie.vote_average.toFixed(1)
    },
    picked: function () {
      return this.movie.user_picked
    }
  }
  ,
  methods: {
    mouseEnter: function (e) {
      if (!this.scaleCard) this.scaleCard = e.target;
      this.$store.dispatch('mouseEnter', e.target);
    },
    mouseLeave: function () {
      this.$store.dispatch('mouseLeave')
    },
    pickClick: function (e) {
      this.$store.dispatch('pickClick', this.movie.id)
      .then((res) => {
        // this.movie.user_picked = !this.movie.user_picked
        this.$emit('pick', this.index, res.pick, e.target)
      })
    },
    modalOpen: function() {
      this.$store.dispatch('modalOpen')
    }
  }
}
</script>

<style scoped>
  img {
    /* 5개 */
    width: 16vw;
    height: 24vw;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 12px;
    overflow: hidden;
    object-fit: cover;
 }
 .card-root {
   width: 16vw;
   margin: 0 2vw;
   /* position: relative; */
 }
 .card-container {
   position: relative;
 }

 .detail {
   position: absolute;
   display: none;
   top: 0;
   left: 0;
   width: 100%;
   height: 100%;
   background: black;
   border-radius: 12px;
   transition: .5s;
   z-index: 1000;
 }
 .detail h3 {
   font-size: 1.3rem;
   margin-left: 10px;
 }

  .detail > .video-container {
    position: relative;
    width: 100%;
    padding-bottom: 56.25%;
  }

  .video-container > iframe {
    position: absolute;
    width: 100%;
    height: 100%;
  }

 .scaleUp > .detail {
   display: flex;
   flex-direction: column;
 }

 .detail-description {
   margin: auto 0;
 }
 .detail-description > .header {
   display: flex;
   justify-content: space-between;
   align-items: center;
 }
 .rating-container {
   display: flex;
   justify-content: center;
   align-items: center;
   margin: 1rem auto;
 }
 .rating-container > div {
   font-size: 1.2rem;
   margin-left: 0.6rem;
 }
  .button-container {
    min-width: 30%;
    display: flex;
    justify-content: flex-end;
  }

  .button-container > button {
    width: 40px;
    height: 40px;
    margin-right: 10px;
    border: 3px #e0dfdf solid;
    color: inherit;
    border-radius: 50%;
    background: inherit;
  }

  .button-container > button:hover {
    color: #222;
    background: #e0dfdf;
  }

  .button-container > button > i {
    pointer-events: none;
  }
 
 @media (max-width: 1200px) {
    img {
      /* 4개 */
      width: 21vw;
      height: 31.5vw;
    }
    .card-root {
      width: 21vw;
    }
 }

 @media (max-width: 1000px) {
    img {
      /* 3개 */
      width: calc(88vw/3);
      height: calc((88vw/3)/2*3);
    }
    .card-root {
      width: calc(88vw/3);
    }

 }

 @media (max-width: 800px) {
    img {
      /* 2 */
      width: 46vw;
      height: 69vw;
    }
    .card-root {
      width: 46vw;
    }
   
 }



</style>