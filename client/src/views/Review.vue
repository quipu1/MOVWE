<template>
<div>
    <div v-if="review" class="review-detail-container">
        <div class="detail-header">
            <h2>{{ review.title }}</h2>
            <div class="header-info">
                <h3>{{ review.username }}</h3>
                <p>{{ review.movie }} |</p>
                <p>{{ date }}</p>
            </div>
            <div class="like-container">
                <button @click="reviewLike">
                    <i class="fas fa-heart" v-if="review.user_like"></i>
                    <i class="far fa-heart" v-else></i>
                </button>
                <p>{{ review.like_count }}</p>
            </div>
        </div>
        <div class="detail-content">
            <p>{{ review.content }}</p>
        </div>
        <div class="user-button-container">
            <button class="listBtn" @click="goReviewList">목록으로</button>
            <button class="modify" @click="modifyReview" v-if="review.user_flag">수정</button>
            <button class="delete" @click="deleteReview" v-if="review.user_flag">삭제</button>
        </div>
        <div class="comment-header">
            <h3>댓글 목록 ({{ review.comment_set.length }})</h3>
            <button class="btn" @click="openForm">댓글 작성</button>
        </div>
        <div class="form-container">
            <form class="comment-form" @submit.prevent="commentSubmit">
                <textarea name="content" placeholder="댓글을 작성하시오"></textarea>
                <button type="submit" class="btn comment-btn">작성 완료</button>
            </form>
            <div class="close-container">
                <div class="pin"></div>
                <button class="btn" @click="closeForm"><i class="fas fa-chevron-up"></i></button>
            </div>
        </div>
        <div v-if="review.comment_set.length" class="comment-container">
            <div v-for="(comment, idx) in review.comment_set" :key="idx" class="comment-item">
                <div>{{ comment.username }}</div>
                <div>{{ comment.content }}</div>
                <button :data-idx="idx" :data-comment="comment.id" @click="deleteComment" class="comment-delete-button" v-if="comment.user_flag"><i class="fas fa-times"></i></button>
            </div>
        </div>
        <div v-else style="display: flex; justify-content: center;">
            <h3>아직 댓글이 없습니다.</h3>
        </div>
    </div>
    <div v-else class="loading">
      <div class="circle"></div>
      <div class="circle"></div>
      <div class="circle"></div>
    </div>
</div>
</template>

<script>
export default {
    name: 'Review',
    data: function () {
        return {
            review: null,
        }
    },
    computed: {
        date: function () {
            const reviewDate = new Date(this.review.updated_at)
            return `${reviewDate.getFullYear()}년 ${reviewDate.getMonth()+1}월 ${reviewDate.getDate()}일`
        }
    },
    methods: {
        goReviewList: function () {
            this.$router.push({ name: 'ReviewList', params: { id: this.review.movie_id } })
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
        commentSubmit: function (e) {
            const params = {
                reviewId: this.review.id,
                form: e.target
            }
            this.$store.dispatch('comment_create', params)
            .then(res => {
                this.review.comment_set.push(res)
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
        reviewLike: function () {
            this.$store.dispatch('review_like', this.review.id)
            .then(res => {
                this.review.user_like = res.liked
                if (res.liked) {
                    this.review.like_count ++;
                } else {
                    this.review.like_count --;
                }
            })
            .catch(err => {
                if (err.message === '401') {
                    alert('로그인 세션이 만료되었습니다.')
                    this.$store.dispatch('logOut')
                    this.$router.push({ name: 'Login' })
                } else if(err.message === '404') {
                    alert('존재하지 않는 게시물 입니다.')
                    this.$router.push({ name: 'Home' })
                } else {
                    alert(err.message)
                }
            })
        },
        modifyReview: function () {
            this.$router.push({ name: 'ReviewFormRouter', params: { id: this.review.movie_id }, query: { reviewid: this.review.id } })
        },
        deleteReview: function () {
            if (confirm('리뷰를 삭제하시겠습니까?')) {
                this.$store.dispatch('review_delete', this.review.id)
                .then(() => {
                    alert('정상적으로 삭제되었습니다.')
                    this.$router.push({ name: 'ReviewList', params: { id: this.review.movie_id } })
                })
                .catch(err => {
                    alert(err.message)
                })
            }
        },
        deleteComment: function (e) {
            const commentId = e.target.dataset.comment
            const commentIdx = e.target.dataset.idx
            if (confirm('댓글을 삭제하시겠습니까?')) {
                this.$store.dispatch('comment_delete', commentId)
                .then(() => {
                    this.review.comment_set.splice(commentIdx, 1)
                    alert('정상적으로 삭제되었습니다.')
                })
                .catch(err => {
                    alert(err.message)
                })
            }
        }
    },
    created: function () {
        this.$store.dispatch('modalOff')
        const reviewId = this.$route.params.id
        this.$store.dispatch('getReviewDetail', reviewId)
        .then(res => {
            this.review = res
            console.log(res)
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
}
</script>

<style scoped>
.review-detail-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto 2rem auto;
    padding: .5rem;
}
.detail-header {
    position: relative;
    border-bottom: 3px solid #999;
}
.detail-content {
    padding: 1rem;
    min-height: 100px;
    border-bottom: 3px solid #999;
    margin-bottom: .5rem;
}
.like-container {
    position: absolute;
    right: 0;
    top: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    transform: translate3d(0, -50%, 0);
    padding: .5rem;
}
.like-container > button {
    margin-right: .4rem;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    font-size: 20px;
    color: #935EA9;
    background-color: white;
}
.like-container > button:hover {
    transition: .5s;
    background-color: #935EA9;
    color: white;
}
h2 {
    font-size: 2rem;
    font-weight: bold;
    padding: .5em 0;
}
h3 {
    font-size: 1.3rem;
}
.header-info {
    display: flex;
    align-items: flex-end;
    padding-bottom: .5rem;
    
}
.header-info > p {
    color: #999;
    margin-left: .5em;
}
.user-button-container {
    display: flex;
    margin: 1rem 0;
}
.user-button-container > button {
    margin-right: .5rem;
    color: white;
    border: none;
    border-radius: 5px;
    padding: .5em;
    font-weight: bold;
    transition: .5s;
}
.user-button-container > button:nth-child(1) {
    background-color: #adb5bd
}
.user-button-container > button:nth-child(2) {
    background-color: #ffc107
}
.user-button-container > button:nth-child(3) {
    background-color: #dc3545
}
.user-button-container > button:hover {
    background-color: white;
}
.user-button-container > .modify:hover {
    color: #ffc107
}
.user-button-container > .delete:hover {
    color: #dc3545
}
.user-button-container > .listBtn:hover {
    color: #adb5bd
}
.comment-header {
    margin-bottom: .5rem;
    display: flex;
    justify-content: space-between
}
.form-container {
    overflow: hidden;
    z-index: 0;
    height: 0;
    transition: .5s;
    margin-bottom: 1rem;
}
.form-container > * {
    transform: translate3d(0, -100%, 0);
    transition: .5s;
}
.open > * {
    transform: translate3d(0, 0, 0);
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
.comment-form > textarea {
    width: 100%;
    height: 4rem;
    font-size: 1.2rem;
    padding: .4em;
    margin-bottom: 1rem;
}
.comment-form > textarea:focus {
    outline: none;
}
.btn.comment-btn {
    border-radius: 2px;
}
.comment-item {
    position: relative;
    display: flex;
    margin: .5rem;
    background-color: white;
    color: black;
    border-radius: 5px;
}
.comment-item > *{
    padding: .7rem;
}
.comment-item > div:nth-child(1) {
    width: 20%;
    border-right: 2px solid #777;
}
.comment-item > div:nth-child(2) {
    width: 80%;
}
.comment-delete-button {
    position: absolute;
    top: 0;
    right: 0;
    width: 20px;
    height: 20px;
    transform: translate3d(50%, -50%, 0);
    font-size: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: none;
    border-radius: 50%;
    color: white;
    background: #dc3545;
}
.comment-delete-button:hover {
    transition: .5s;
    color: #dc3545;
    background: white;
}


</style>