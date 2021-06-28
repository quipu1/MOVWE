<template>
  <div class="home-main">
      <div v-if="loading">영화에 의한</div>
      <div v-if="loading">영화를 위한</div>
      <div v-if="loading">세상을 만들어 갑니다.</div>
      <div v-else class="loading">
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
      </div>
      <canvas width="1850" height="750"></canvas>
  </div>
</template>

<script>
export default {
    name: 'HomeMain',
    data: function () {
        return {
            canvas: null,
            context: null,
            imgs: [],
            loadImg: 0,
            imgIndex: 0,
            interval: null,
            canvasInterval: null,
            sectionNum: 1,
            loading: false,
        }
    },
    methods: {
        draw: function () {
            if (this.imgIndex === 30){
                this.imgIndex = 0;
                return;
            }
            this.context.drawImage(this.imgs[this.imgIndex], 0, 0)
            this.imgIndex += 1
        },
        plusImg: function () {
            this.loadImg ++;
        },
        setLayout: function () {
            const vw = window.innerWidth;
            const ratio = (vw / 1850)/1.5;
            this.canvas.style.transform = `scale(${ratio})`
            // const { height } = this.canvas.getBoundingClientRect()
            const main = document.querySelector('.home-main')
            main.style.height = `${1000*ratio}px`
        },
        anime: function () {
            const main = document.querySelector('.home-main')
            if (this.canvasInterval) {
                clearInterval(this.canvasInterval)
                this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.imgIndex = 0;
            }
            main.setAttribute('id', `section-${this.sectionNum}`);
            if(this.sectionNum === 4) {
                this.canvasInterval = setInterval(this.draw, 1000/30)
                this.sectionNum = 0;
            }
            this.sectionNum ++;
        }
    },
    watch: {
        loadImg: function () {
            if(this.loadImg === 30) {
                this.loading = true
                this.interval = setInterval(this.anime, 2500)
            }
        }
    },
    mounted: function () {
      for (let i=0; i< 30; i++) {
          const img = new Image()
          let str = i;
          if (str < 10) str = '0' + str
          img.src = require(`../assets/path_000${str}.png`)
          this.imgs.push(img)
          this.imgs[i].addEventListener('load', this.plusImg);
      }
      this.canvas = document.querySelector('canvas')
      this.context = this.canvas.getContext('2d')
      this.setLayout();
      window.addEventListener('resize', this.setLayout)
    },
    destroyed: function () {
        this.imgs.forEach(img => {
            img.removeEventListener('load', this.plusImg)
        })
        if (this.interval) {
            clearInterval(this.interval)
        }
        if (this.canvasInterval) {
            clearInterval(this.canvasInterval)
        }
        window.removeEventListener('resize', this.setLayout)
    }
}
</script>

<style>
    .home-main {
        margin-top: 100px; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #111;
    }
    canvas {
        display: none;
        /* opacity: 0; */
        background: #111;
    }
    .home-main > div {
        /* transition: .5s; */
        font-size: 8vw;
        color: #BD9ACC;
        display: none;
    }
    .loading {
        display: flex !important;
    }
    #section-1 > div:nth-child(1) {
        display: block;
        animation: fadeInOut 2.5s forwards;
    }
    #section-2 > div:nth-child(2) {
        display: block;
        animation: fadeInOut 2.5s forwards;
    }
    #section-3 > div:nth-child(3) {
        display: block;
        animation: fadeInOut 2.5s forwards;
    }
    #section-4 > canvas {
        display: block;
        animation: forcanvas 2.5s forwards;
    }

    @keyframes fadeInOut {
        0% {
            transform: translate3d(0, 30%, 0);
            opacity: 0;
        }
        50%{
            opacity: 1;
        }
        100% {
            opacity: 0;
            transform: translate3d(0, -30%, 0);
        }     
    }
    @keyframes forcanvas {
        0% {
            opacity: 0;
        }
        50%{
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }
</style>