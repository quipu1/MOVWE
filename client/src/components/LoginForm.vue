<template>
  <div class="login-div">
    <div class="back-img"></div>
    <form @submit.prevent="login">
      <div class="header">로그인</div>
      <input type="text" name="username" placeholder="ID">
      <input type="password" name="password" placeholder="password">
      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginForm',
  methods: {
    login: function (e) {
      this.$store.dispatch('login', e.target)
      .then(() => {
        this.$router.push({ name : 'Home' })
      })
      .catch(err => {
        alert(err.message);
        e.target.username.focus();
      })
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
  /* z-index: 100; */
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

form > input:nth-of-type(2) {
  border-bottom-left-radius: .5rem;
  border-bottom-right-radius: .5rem;
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
</style>