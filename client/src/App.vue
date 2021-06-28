<template>
  <div id="app" :class="{ modal: modalOpened}">
    <nav id="nav" :class="{unlogined : !login }">
      <img src="@/assets/logo.png" alt="" @click="goHome">
      <div @click="toggleClick" class="toggle" v-if="login"><i class="fas fa-bars fa-lg"></i></div>
      <div v-if="login" class="nav-container">
        <div class="nav-left">
          <router-link :to="{ name: 'MoviePick' }" >내가 찜한 목록</router-link>
          <router-link :to="{ name: 'MovieRecommend' }">영화 추천</router-link>
        </div>
        <div class="nav-right">
          <form @submit.prevent="searchSubmit">
            <div class="search-icon"><i class="fas fa-search"></i></div>
            <input type="text" v-model="query" @focus="searchFocus" @blur="finishSearch" @input="inputChange" placeholder="enter로 제출">
            <div v-if="search" class="search-container">
              <div v-if="movieSearch || genreSearch">
                <div v-if="movieSearch" class="search-box">
                  {{ query }}(으)로 검색된 영화가 {{ movieSearch }}개 존재합니다.
                </div>
                <div v-if="genreSearch" class="search-box">
                  {{ query }}(으)로 검색된 장르가 {{ genreSearch }}개 존재합니다.
                </div>
              </div>
              <div v-else>
                검색 결과가 존재하지 않습니다.
              </div>
            </div>
          </form>
          <div @click="logOut" class="logout">로그아웃</div>
        </div>
      </div>
      <div v-else>
        <div class="nav-right">
          <div class="sign-btn" @click="goSignUp" v-if="this.$router.currentRoute.name === 'Login'">
            회원가입
          </div>
          <div v-else class="sign-btn" @click="goLogin">
            로그인
          </div>
        </div>
      </div>
    </nav>
    <router-view style="padding: 100px 0;"/>
    <footer v-if="login">
      © 2021, movwe
    </footer>
  </div>
  
</template>

<script>

export default {
  image: {
    logo: './src/assets/logo.png'
  },
  data: function () {
    return {
      toggle: false,
      query: '',
      search: false,
    }
  },
  computed: {
    login: function () {
      return this.$store.state.isLogin;
    },
    modalOpened: function () {
      if (this.$store.state.modalMovieId) {
        document.body.classList.add('modal-open')
        return true;
      } else {
        document.body.classList.remove('modal-open')
        return false;
      }
    },
    movieSearch: function () {
      return this.$store.state.movieSearch
    },
    genreSearch: function () {
      return this.$store.state.genreSearch
    }
  },
  created: function () {
    this.$store.dispatch('getToken');
    if (!this.$store.state.isLogin) {
      if (this.$router.currentRoute.name !== 'Login'){
        this.$router.push({name: 'Login'})
      }
    }
  },
  mounted: function () {
    this.setLayout();
    window.addEventListener('resize', this.setLayout)
  },
  updated: function() {
    this.setLayout();
  },
  methods: {
    searchSubmit: function () {
      if (!this.movieSearch && !this.genreSearch) {
        this.$store.dispatch('resetSearch')
        alert('검색결과가 존재하지 않습니다.')
        return;
      }
      this.$router.push({ name: 'Search', query: { q: this.query } })
      // this.$store.dispatch('resetSearch')
    },
    inputChange: function () {
      if(!this.query.trim()){
        this.$store.dispatch('resetSearch')
        return;
      }
      this.$store.dispatch('searchPreview', this.query)
    },
    finishSearch: function () {
      this.search = false
      this.$store.dispatch('resetSearch')
      this.query = ''
    },
    searchFocus: function () {
      this.search = true
    },
    toggleClick: function () {
      const navCon = document.querySelector('.nav-container')
      if (!this.toggle) {
        this.toggle = true
        let nextheight = 0;
        navCon.childNodes.forEach(node => {
          const { height } = node.getBoundingClientRect()
          nextheight += height;
        })
        navCon.style.height = `${nextheight}px`;
      } else {
        this.toggle = false;
        navCon.removeAttribute("style")
      }
    },
    goSignUp: function () {
      this.$router.push({ name: 'SignUp' })
    },
    goLogin: function () {
      this.$router.push({ name: 'Login' })
    },
    logOut: function () {
      this.$store.dispatch('logOut')
      this.$router.push({ name: 'Login' })
    },
    goHome: function () {
      if (this.$route.name !== 'Home') {
        this.$router.push({ name: 'Home' })
      }
    },
    setLayout: function () {
      this.toggle = false;
      const navCon = document.querySelector('.nav-container')
      if (navCon) document.querySelector('.nav-container').removeAttribute('style')
      const size = window.innerWidth;
      const nav = document.querySelector('#nav');
      if (size < 600) {
        nav.classList.add('short')
      } else {
        nav.classList.remove('short')
      }
    }
  }
}

</script>


<style>
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  background-color: #222;
  color: #e0dfdf;
  font-family: 'Noto Sans KR', sans-serif;
  position: relative;
  min-height: 100vh;
}
body.modal-open {
  overflow: hidden;
  
}
#nav form {
  display: flex;
  align-items: center;
  margin-right: 1rem;
  position: relative;
}
#nav form > input {
  transition: .5s;
  width: 0;
  padding: 0;
  border-radius: 2px;
  border: none;
}
#nav form > input:focus {
  outline: none;
  width: 100px;
  padding: .2rem;
}
.search-icon {
  font-size: 1.4rem;
  margin: 0 .3rem;
}
#nav form:hover > input {
  width: 100px;
  padding: .2rem;
}
#nav form > .search-container {
  position: absolute;
  top: 110%;
  right: 0;
  padding: .3rem;
  background-color: white;
  color: black;
  border-radius: 3px;
  min-width: 350px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
#app {
  /* text-align: center; */
}

#app a {
  text-decoration: none;
}

#nav {
  width: 100%;
  height: 100px;
  padding: 10px;
  display: flex;
  justify-content: stretch;
  align-items: center;
  position: fixed;
  z-index: 10;
  background-color: #222;
}
#nav img {
  height: 100%;
  cursor: pointer;
  margin-right: 1rem;
}

#nav.unlogined {
  background-color: rgba(0, 0, 0, 0);
}

#nav > h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #BD9ACC
}
#nav > .nav-container {
  width: auto;
  display: flex;
  align-items: center;
}
.nav-right {
  position: absolute;
  right: 10px;
  top: 0;
  height: 100%;
  display: flex;
  align-items: center;
}
.toggle {
  display: none;
  font-size: 1.3rem;
  position: absolute;
  right: 10px;
  top: 0;
  height: 100%;
  cursor: pointer;
}
#nav.short > .nav-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  z-index: 0;
  position: absolute;
  top: 100%;
  left: 0;
  overflow: hidden;
  background-color: #222;
  transition: .5s;
  height: 0;
}
#nav.short form {
  display: none !important
}
#nav.short > .nav-container > * {
  padding: 0;
}
#nav.short > .nav-container > * > * {
  display: flex;
  justify-content: center;
  margin: .5rem 0;
  padding: .3rem;
}
#nav.short > .nav-container > .nav-right {
  position: static;
  display: block;
  height: auto;
}
#nav.short > .toggle {
  display: flex;
  align-items: center;
}
.logout {
  cursor: pointer;
}
.logout:hover {
  text-decoration: underline;
}
.sign-btn {
  padding: .7em;
  background: white;
  border-radius: 2rem;
  color: black;
  cursor: pointer;
  transition: .5s;
  /* z-index: 10; */
}

.sign-btn:hover {
  color: white;
  background-color: black;
}

#nav a {
  font-weight: bold;
  color: white;
  margin-right: .7rem;
  letter-spacing: -1px;
}

#nav a.router-link-exact-active {
  color: #999;
  border-bottom: 3px solid #999;
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
@keyframes circleMove {
  from {
      transform: translate3d(0, 0, 0);
  }
  to {
      transform: translate3d(0, -80%, 0);
  }
}
.btn {
  border: none;
  background-color: white;
  color: #222;
  font-size: 1rem;
  padding: .3rem;
  border-radius: 100px;
  transition: .5s;
  font-weight: 700;
}
.btn:hover {
  background-color: black;
  color: white;
}
button > i {
  pointer-events: none;
}
textarea {
  resize: none;
}

footer {
  width: 100%;
  height: 4rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: black;
  z-index: 0;
  position: absolute;
  left: 0;
  bottom: 0;
}
</style>
