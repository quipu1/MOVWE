import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLogin: false,
    jwtToken: '',
    API_ENDPOINT: 'http://127.0.0.1:8000/',
    movieList: [],
    genreList: [],
    pendingTimeOut: null,
    scaleCard: null,
    modalMovieId: null,
    movieSearch: null,
    genreSearch: null,
    abortController: null,
    searchLoading: false,
  },
  mutations: {
    RESET_SEARCH: function (state){
      state.movieSearch = null
      state.genreSearch = null
    },
    TOKEN: function (state, jwtToken) {
      if (jwtToken) {
        state.jwtToken = jwtToken;
        state.isLogin = true;
      } else {
        state.isLogin = false;
      }
    },
    LOGIN: function (state, data) {
      state.jwtToken = data.token;
      localStorage.setItem('jwt-token', data.token);
      state.isLogin = true;
    },
    LOGOUT: function (state) {
      state.isLogin = false;
      state.jwtToken = '';
    },
    SET_MOVIE_LIST (state, data) {
      state.movieList = data;
    },
    SET_GENRE_LIST (state, data) {
      state.genreList = data;
    },
    REMOVE_TIME_OUT (state) {
      clearTimeout(state.pendingTimeOut);
      state.pendingTimeOut = null;
    },
    SET_SCALE_CARD (state, target) {
      state.scaleCard = target;
    },
    REMOVE_SCALE_CARD (state) {
      const { width, height } = state.scaleCard.getBoundingClientRect();
      state.scaleCard.childNodes[1].style.top = `0px`;
      state.scaleCard.childNodes[1].style.left = `0px`;
      state.scaleCard.childNodes[1].style.width = `${width}px`;
      state.scaleCard.childNodes[1].style.height = `${height}px`;
      state.scaleCard.childNodes[1].style.opacity = '0';
      state.scaleCard.childNodes[1].firstChild.firstChild.src = '';
      setTimeout(() => {
        if (!state.scaleCard) return;
        state.scaleCard.classList.remove('scaleUp');
        state.scaleCard.childNodes[1].style = '';
        state.scaleCard = null; 
      }, 500)
    },
    PICK_CHANGE (state, movieID) {
      for (let i=0; i < state.movieList.length; i++) {
        const movie = state.movieList[i]
        if (movie.id === movieID) {
          movie.user_picked = !movie.user_picked
          return;
        }
      }
    },
    MODAL_OPEN (state, data) {
      state.modalMovieId = data;
    },
    MODAL_OFF (state) {
      state.modalMovieId = null;
    },
    SET_MOVIE_RATE (state, params) {
      for (let i=0; i < state.movieList.length; i++) {
        const movie = state.movieList[i]
        if (movie.id === params.movieId) {
          movie.rank = parseInt(params.rating)
          return;
        }
      }
    },
    SEARCH_PREVIEW_RESULT (state, result) {
      state.movieSearch = result.movie_count
      state.genreSearch = result.genre_count
    }
  },
  actions: {
    searchDetail: async function (context, query) {
      const url = context.state.API_ENDPOINT + `api/v1/search?q=${query}`
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        },
      });
      if (res.status === 200) {
        const result = await res.json()
        return result
      } else {
        throw new Error(res.status)
      }
    },
    searchPreview: async function (context, query) {
      const url = context.state.API_ENDPOINT + `api/v1/search/preview?q=${query}`
      context.state.searchLoadgin = true
      if (context.state.abortController){
        context.state.abortController.abort()
        context.state.abortController = null
      }
      context.state.abortController = new AbortController()
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        },
      });
      
      if (res.status === 200) {
        const result = await res.json()
        context.commit('SEARCH_PREVIEW_RESULT', result)
        context.state.abortController = null;
        context.state.searchLoading = false
        return result
      } else {
        context.state.abortController = null;
        context.state.searchLoading = false;
        throw new Error(res.status)
      }
    },
    resetSearch: function (context) {
      context.commit('RESET_SEARCH')
    },
    getToken: function (context) {
      const token = localStorage.getItem('jwt-token');
      context.commit('TOKEN', token);
    },
    login: async function (context, formData) {
      const url = context.state.API_ENDPOINT + 'accounts/api-token-auth/';
      const data = {
        username: formData.username.value,
        password: formData.password.value,
      }
      try {
        const res = await fetch(url, {
          method: 'POST',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });
        if (res.status === 200) {
          const resdata = await res.json();
          context.commit('LOGIN', resdata);
        } else {
          throw new Error('아이디 혹은 비밀번호가 올바르지 않습니다.')
        }
      } catch (err) {
        console.log(err.message)
        throw err;
      }
    },
    signup: async function (context, formData) {
      const url = context.state.API_ENDPOINT + 'accounts/signup/'
      const data = {
        username: formData.username.value,
        password: formData.password.value,
        passwordConfirmation: formData.passwordConfirmation.value
      }
      try {
        const res = await fetch(url, {
          method: 'POST',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });
        return res
      } catch (err) {
        console.log(err.message)
        throw err
      }
    },
    logOut: function (context) {
      localStorage.removeItem('jwt-token')
      context.commit('LOGOUT')
    },
    getMovieList: async function (context) {
      if (context.state.movieList.length > 0) {
        return
      } else {
        const url = context.state.API_ENDPOINT + 'api/v1/movies/'
        const res = await fetch(url, {
          method: 'GET',
          headers: {
            'Authorization': 'JWT ' + context.state.jwtToken
          }
        })
        if (res.status === 200) {
          const resdata = await res.json()
          context.commit('SET_MOVIE_LIST', resdata)
        } else {
          throw new Error(res.status)
        }
      }
    },
    getMovieOne: async function (context, movieId) {
      const url = context.state.API_ENDPOINT + `api/v1/movie/${movieId}`
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        }
      })
      if (res.status === 200) {
        const result = await res.json()
        return result;
      } else {
        throw new Error(res.status)
      }
    },
    getGenreList: async function (context) {
      if (context.state.movieList.length > 0) {
        return
      } else {
        const url = context.state.API_ENDPOINT + 'api/v1/genres/'
        const res = await fetch(url, {
          method: 'GET',
          headers: {
            'Authorization': 'JWT ' + context.state.jwtToken
          }
        })
        if (res.status === 200) {
          const resdata = await res.json()
          context.commit('SET_GENRE_LIST', resdata)
        } else {
          throw new Error(res.status)
        }
      }
    },
    pickClick: async function(context, movieID) {
      const url = context.state.API_ENDPOINT + `api/v1/movie/${movieID}/pick/`
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        }
      })
      if (res.status === 200) {
        context.commit('PICK_CHANGE', movieID);
        return await res.json()
      } else {
        throw new Error(res.status)
      }
    },
    mouseEnter: function (context, target) {
      if (context.state.pendingTimeOut) {
        context.commit('REMOVE_TIME_OUT')
      }
      context.state.pendingTimeOut = setTimeout(() => {
        target.classList.add('scaleUp')
        context.commit('SET_SCALE_CARD', target)
        const detail = target.childNodes[1];
        const {left, width, height } = target.getBoundingClientRect()
        const moveTop = - (height*1.5 - height) / 2
        let moveLeft = - (width*1.5 - width) / 2
        if (moveLeft + left < 0) moveLeft = 0
        else if (left + moveLeft + width*1.5 > window.innerWidth) moveLeft = -(width*1.5 - width)
        detail.style.width = `${width*1.5}px`;
        detail.style.height = `${height*1.5}px`;
        detail.style.top = `${moveTop}px`;
        detail.style.left = `${moveLeft}px`;
        detail.firstChild.firstChild.src = detail.firstChild.firstChild.dataset.src;
      }, 700);
    },
    mouseLeave: function (context) {
      if (context.state.pendingTimeOut) {
        context.commit('REMOVE_TIME_OUT')
      }
      if (context.state.scaleCard) {
        context.commit('REMOVE_SCALE_CARD')
      }
    },
    modalOpen: function (context) {
      if (context.state.scaleCard) {
        const movieID = context.state.scaleCard.dataset.movie
        context.commit('MODAL_OPEN', movieID)
      }
    },
    modalOff: function (context) {
      context.commit('MODAL_OFF')
    },
    getReviewList: async function(context, movieID) {
      const url = context.state.API_ENDPOINT + `api/v1/movie/${movieID}/review/`
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        }
      })
      if (res.status === 200) {
        const data = await res.json()
        return data
      } else {
        throw new Error(res.status)
      }
    },
    setRate: async function (context, params) {
      const url = context.state.API_ENDPOINT + `api/v1/movie/${params.movieId}/rank/`
      const data = {
        rank: String(params.rating)
      }
      const res = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + context.state.jwtToken
        },
        body: JSON.stringify(data)
      })
      if (res.status === 201 || res.status === 200) {
        const result = await res.json()
        context.commit('SET_MOVIE_RATE', params)
        return result
      } else {
        throw new Error(res.status)
      }
    },
    review_create: async function (context, params) {
      const url = context.state.API_ENDPOINT + `api/v1/movie/${params.movieId}/review/`
      const form = params.form
      const data = {
        title: form.title.value.trim(),
        content: form.content.value.trim()
      }
      const res = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + context.state.jwtToken
        },
        body: JSON.stringify(data)
      })
      if (res.status === 201) {
        const result = await res.json()
        return result
      } else if (res.status === 400) {
        const result = await res.json()
        throw new Error(result.message)
      } else {
        throw new Error(res.status)
      }
    },
    reviewModify: async function (context, params) {
      const url = context.state.API_ENDPOINT + `api/v1/review/${params.reviewId}/`
      const form = params.form
      const data = {
        title: form.title.value.trim(),
        content: form.content.value.trim()
      }
      const res = await fetch(url, {
        method: 'PUT',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + context.state.jwtToken
        },
        body: JSON.stringify(data)
      })
      if (res.status === 200) {
        const result = await res.json()
        return result
      } else {
        return new Error(res.status)
      }
    },
    getReviewDetail: async function (context, reviewId) {
      const url = context.state.API_ENDPOINT + `api/v1/review/${reviewId}/`
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        }
      })
      if (res.status === 200) {
        const result = await res.json()
        return result
      } else {
        throw new Error(res.status)
      }
    },
    comment_create: async function (context, params) {
      const url = context.state.API_ENDPOINT + `api/v1/review/${params.reviewId}/comment/`
      const form = params.form
      const data = {
        content: form.content.value.trim()
      }
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + context.state.jwtToken
        },
        body: JSON.stringify(data)
      })
      if (res.status === 201) {
        const result = await res.json()
        return result
      } else if (res.status === 400) {
        const result = await res.json()
        throw new Error(result.message)
      } else {
        throw new Error(res.status)
      }
    },
    review_like: async function (context, reviewId) {
      const url = context.state.API_ENDPOINT + `api/v1/review/${reviewId}/like/`;
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        },
      })
      if (res.status === 200) {
        const result = await res.json()
        return result
      } else {
        throw new Error(res.status)
      }
    },
    review_delete: async function (context, reviewId) {
      const url = context.state.API_ENDPOINT + `api/v1/review/${reviewId}/`
      const res = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        },
      })
      if (res.status === 204) {
        return res
      } else {
        const err = res.json()
        throw new Error(err.message)
      }
    },
    comment_delete: async function (context, commentId) {
      const url = context.state.API_ENDPOINT + `api/v1/comment/${commentId}/`
      const res = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        },
      })
      if (res.status === 204) {
        return res
      } else {
        const err = res.json()
        throw new Error(err.message)
      }
    },
    getMoviePick: async function (context) {
      const url = context.state.API_ENDPOINT + `api/v1/movies/pick/`
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        },
      })
      if (res.status === 200) {
        return await res.json()
      } else {
        throw new Error(res.status)
      }
    },
    getMovieRecommend: async function (context) {
      const url = context.state.API_ENDPOINT + `api/v1/movies/recommend/`
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': 'JWT ' + context.state.jwtToken
        },
      })
      if (res.status === 200) {
        return await res.json()
      } else {
        throw new Error(res.status)
      }
    }
  },
  getters: {
    popularMovieList: function (state) {
      return state.movieList
    },
    genreMoviesArray: function (state) {
      const returnArray = []
      state.genreList.forEach(genre => {
        const genreMovies = {
          name: genre.name,
          data: [],
        }
        state.movieList.forEach(movie => {
          for (let i = 0; i < movie.genres.length; i++) {
            if (movie.genres[i].id === genre.id) {
              genreMovies.data.push(movie);
              break;
            }
          }
        })
        if(genreMovies.data.length > 0) returnArray.push(genreMovies);
      })
      return returnArray;
    }
  },
  modules: {
  }
})
