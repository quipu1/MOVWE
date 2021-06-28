<template>
  <div class="login-div">
    <div class="back-img"></div>
    <form @submit.prevent="signup">
      <div class="header">회원가입</div>
      <input type="text" name="username" placeholder="ID 문자, 숫자만 가능 6자 이상" v-model="username" @input="usernameChange">
      <div v-show="idCheck" class="check box a"><i class="fas fa-check"></i></div>
      <div v-show="idError" class="error box a"><i class="fas fa-times"></i></div>
      <input type="password" name="password" placeholder="PW 문자, 숫자, 특문 포함 8자~20자" v-model="pw" @input="passwordChange">
      <div v-show="pwCheck" class="check box b"><i class="fas fa-check"></i></div>
      <div v-show="pwError" class="error box b"><i class="fas fa-times"></i></div>
      <input type="password" name="passwordConfirmation" placeholder="비밀번호 확인" v-model="pwc" @input="passwordChange">
      <div v-show="pwcCheck" class="check box c"><i class="fas fa-check fa-sm"></i></div>
      <div v-show="pwcError" class="error box c"><i class="fas fa-times"></i></div>
      <button type="submit">회원가입</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SignUpForm',
  methods: {
    signup: function (e) {
      if (this.idError || this.username.length === 0) {
        alert('아이디를 확인하십시오.')
        e.target.username.focus();
        return;
      }
      if (this.pwError || this.pw.length === 0) {
        alert('비밀번호를 확인하십시오.')
        e.target.password.focus();
        return;
      }
      if (this.pwcError || this.pwc.length === 0) {
        alert('비밀번호가 같지 않습니다.')
        e.target.passwordConfirmation.focus();
        this.pwc = '';
        return;
      }
      this.$store.dispatch('signup', e.target)
      .then(() => {
        alert('가입이 완료되었습니다. 로그인 페이지로 이동합니다.')
        this.$router.push({ name: 'Login' })
      })
      .catch(err => {
        alert(err)
      })
    },
    passwordChange: function () {
      const reget = /^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+])(?!.*[^a-zA-z0-9$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$/
      if(reget.test(this.pw.trim())) {
        this.pwCheck = true
        this.pwError = false
      } else {
        this.pwError = true
        this.pwCheck = false
      }
      if(this.pw !== this.pwc || this.pwc.length < 1) {
        this.pwcError = true
        this.pwcCheck = false
      } else {
        this.pwcError = false
        this.pwcCheck = true
      }
    },
    usernameChange: function () {
      const reget = /^[\w\d_]{6,20}$/
      if(reget.test(this.username.trim())) {
        this.idCheck = true
        this.idError = false
      } else {
        this.idCheck = false
        this.idError = true
      }
    }
  },
  data: function () {
    return {
      username: '',
      pw: '',
      pwc: '',
      idCheck: false,
      idError: false,
      pwCheck: false,
      pwError: false,
      pwcCheck: false,
      pwcError: false,
    }
  }
}
</script>

<style scoped>
.login-div {
  position: absolute;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
.back-img {
  background-image: url('../assets/ticket.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  opacity: 0.3;
  position: fixed;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  z-index: 0;
}
form {
  position: relative;
  width: 300px;
  display: flex;
  flex-direction: column;
  z-index: 1;
}

form > .header {
  display: flex;
  justify-content: center;
  font-weight: bold;
  margin-bottom: 1rem;
}

form > input {
  height: 2.5rem;
  font-size: 1rem;
  border: 0px;
  padding: .2rem .5rem
}
form > input:focus {
  outline: none;
}

form > input:nth-of-type(1) {
  border-top-left-radius: .5rem;
  border-top-right-radius: .5rem;
  border-bottom: .3px solid #555;
}

form > input:nth-of-type(3) {
  border-bottom-left-radius: .5rem;
  border-bottom-right-radius: .5rem;
  border-top: .3px solid #555;
  margin-bottom: 1rem;
}

form > button {
  border: none;
  background-color: #48445C;
  color: white;
  font-size: 1rem;
  padding: .5rem;
  border-radius: 100px;
  transition: .5s;
}

form > button:hover {
  background-color: #151129;
}

.errInput {
  border: 2px solid red;
}
.box {
  border: none;
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  right: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 4px;
}
.check {
  background: #0d6efd;
}
.error {
  background: #dc3545;
}

.box.a {
  top: 42px;
}
.box.b {
  top: 82px;
}
.box.c {
  top: 122px;
}


</style>