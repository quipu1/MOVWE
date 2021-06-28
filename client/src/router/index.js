import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/accounts/Login.vue'
import SignUp from '../views/accounts/SignUp.vue'
import Review from '../views/Review.vue'
import Genre from '../views/Genre.vue'
import ReviewFormRouter from '../views/ReviewFormRouter.vue'
import ReviewList from '../views/ReviewList.vue'
import MoviePick from '../views/MoviePick.vue'
import MovieRecommend from '../views/MovieRecommend.vue'
import Search from '../views/Search.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/sign_in',
    name: 'Login',
    component: Login
  },
  {
    path: '/sign_up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/review/:id',
    name: 'Review',
    component: Review
  },
  {
    path: '/genre/:name',
    name: 'Genre',
    component: Genre
  },
  {
    path: '/movie/:id/review',
    name: 'ReviewFormRouter',
    component: ReviewFormRouter
  },
  {
    path: '/movie/:id/reviewlist',
    name: 'ReviewList',
    component: ReviewList
  },
  {
    path: '/mypick',
    name: 'MoviePick',
    component: MoviePick
  },
  {
    path: '/recommend',
    name: 'MovieRecommend',
    component: MovieRecommend
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
