<template>
  <div @click="goReviewDetail" class="review-item-container">
      <div class="review-item-header">
          <div class="header-left header-item">
            <h5>{{ review.username }}</h5>
            {{presentDay}}
          </div>
          <div class="header-right header-item">
              <StarRating :star-size="15" :read-only="true" :rating="review.rank/2" :show-rating="false" :increment="0.5"/>
              <div>
                  좋아요 {{ review.like_count }}
              </div>
              <div>
                  댓글 {{ review.comment_count }}
              </div>
          </div>
      </div>
      <div class="review-item-title">
          {{ review.title }}
      </div>
  </div>
</template>

<script>
import StarRating from 'vue-star-rating'
export default {
    name: 'ReviewCard',
    components: {
        StarRating,
    },
    props: {
        review: Object
    },
    data: function () {
        return {
        }
    },
    methods: {
        goReviewDetail: function () {
            this.$router.push({ name: 'Review', params: { id: this.review.id } })
        }
    },
    computed: {
        date: function () {
            return new Date(this.review.created_at)
        },
        presentDay: function () {
            const nowDate = new Date()
            let hour = nowDate.getHours() - this.date.getHours()
            let min = nowDate.getMinutes() - this.date.getMinutes()
            let day = nowDate.getDate() - this.date.getDate()
            let month = nowDate.getMonth() - this.date.getMonth()
            let year = nowDate.getYear() - this.date.getYear()
            year -= month < 0 ? 1 : 0
            if (year > 0) return `${year}년 전`
            month *= month > 0 ? 1 : -1
            if (month > 0) return `${month}달 전`
            day *= day > 0 ? 1:-1
            if (day > 0) return `${day}일 전`
            hour -= min < 0 ? 1 : 0
            if (hour > 0) return `${hour}시간 전`
            min *= min > 0 ? 1 : -1
            if (min > 0) return `${min}분 전`
            return `1분 미만`
        }
    }
}
</script>

<style scoped>
    .review-item-container {
        width: 100%;
        max-width: 1000px;
        margin: 1rem auto;
        border-radius: 10px;
        background-color: white;
        color: black;
        transition: .4s;
        cursor: pointer;
    }
    .review-item-container:hover .review-item-title {
        text-decoration: underline;
    }
    .review-item-header {
        width: 100%;
        padding: .5rem;
        border-bottom: 3px solid;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .review-item-header h5 {
        font-weight: bold;
        margin-right: .3rem;
        font-size: 1.2rem;
    }
    .review-item-title {
        padding: 1rem;
    }
    .header-item {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .header-right > * {
        margin-left: .3rem;
    }
</style>