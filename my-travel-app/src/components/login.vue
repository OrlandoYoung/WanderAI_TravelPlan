<!--
 * 登录页面
 *
 * @Author: ShanZhu
 * @Date: 2023-11-23
-->
@import url('https://fonts.googleapis.com/css2?family=El+Messiri:wght@700&display=swap');

<template>

  <section style="position: relative; min-height: 100vh; overflow: hidden;">
    <!-- 视频背景 -->
    <video
      class="absolute top-0 left-0 w-full h-full object-cover z-0"
      src="@/videos/island.mp4"
      autoplay
      muted
      loop
      playsinline
      style="min-width:100vw; min-height:100vh;"
    ></video>
  
  <div class="box relative z-10">
    
    <div class="square" style="--i:0;"></div>
    <div class="square" style="--i:1;"></div>
    <div class="square" style="--i:2;"></div>
    <div class="square" style="--i:3;"></div>
    <div class="square" style="--i:4;"></div>
    <div class="square" style="--i:5;"></div>
    
   <div class="container"> 
    <div class="form"> 
      <h2>登录WanderAI</h2>
      <form @submit.prevent="login">
        <div class="inputBx">
          <input type="text" v-model="formLabelAlign.email" required="required">
          <span>邮箱</span>
        </div>
        <div class="inputBx password">
          <!-- <input id="password-input" type="password" name="password" required="required"> -->
          <input
            id="password-input"
            v-model="formLabelAlign.password"
            :type="showPassword ? 'text' : 'password'"
            required
          >
          <span>密码</span>
          <!-- <a href="#" class="password-control" :class="{ view: showPassword }" @click.prevent="showHidePassword"></a> -->
        </div>
        <!-- <label class="remember"><input type="checkbox">
          Remember</label> -->
        <div class="inputBx">
          <input type="submit" value="登录"> 

          <!-- <input type="button" value="Log in" @click="login"> -->
        </div>
      </form>
      <!-- <p>Forgot password? <a href="#">Click Here</a></p> -->
      <p>还没有帐户？ <router-link to="/register">去注册</router-link></p>
    </div>
  </div>
    
  </div>
</section>

</template>

<script>
import {mapState} from 'vuex'
export default {
  name: "LoginPage",
  data() {
    return {
      role: 2,
      showPassword: false,
      labelPosition: 'left',
      formLabelAlign: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    //用户登录请求后台处理
    async login() {
      if(this.formLabelAlign.email == undefined || this.formLabelAlign.email == '') {
         this.$message('请输入邮箱');
        return;
      }
      const emailReg = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
      if (!emailReg.test(this.formLabelAlign.email)) {
        this.$message('请输入正确的邮箱格式');
        return;
      }
      if(this.formLabelAlign.password == "") {
        this.$message('请输入密码');
        return;
      }

      try {
        const response = await this.$api.auth.login({
          email: this.formLabelAlign.email,
          password: this.formLabelAlign.password
        });
        const res=response.data; 
        // 登录成功
        if (res.success) {
          this.$message && this.$message.success('登录成功！');
          // 保存token和用户信息
          sessionStorage.setItem('token', res.token);
          localStorage.setItem('user', JSON.stringify(res.user));
          // 跳转到首页或其他页面
          this.$router.push({ path: '/' });
        } else {
          if (res.error && res.error.code === 1001) {
            this.$message && this.$message.error('该邮箱未注册，请先注册');
          } else if (res.error && res.error.code === 1002) {
            this.$message && this.$message.error('密码错误，请重新输入');
          } else {
            this.$message && this.$message.error(res.error?.message || '登录失败，请重试');
          }
        }
      } catch (error) {
        this.$message && this.$message.error('邮箱或密码错误');
      }
    
    },
    clickTag(key) {
      this.role = key
    },

    showHidePassword() {
      this.showPassword = !this.showPassword;
    }
  },
  computed: mapState(["userInfo"]),
  mounted() {

  }
}
</script>


<style lang="less" scoped>
// .remind {
//   border-radius: 4px;
//   padding: 10px 20px;
//   display: flex;
//   position: fixed;
//   right: 20px;
//   bottom: 50%;
//   flex-direction: column;
//   color: #606266;
//   background-color: #fff;
//   border-left: 4px solid #409eff;
//   box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)
// }
// .container {
//   margin-bottom: 32px;
// }
// .container .el-radio-group {
//   margin: 30px 0px;
// }
// a:link {
//   color:#ff962a;
//   text-decoration:none;
// }
// #login {
//   font-size: 14px;
//   color: #000;
//   background-color: #fff;
// }
// #login .bg {
//   position: fixed;
//   top: 0;
//   left: 0;
//   width: 100%;
//   overflow-y: auto;
//   height: 100%;
//   background: url('../../assets/img/loginbg.png')center top / cover no-repeat;
//   background-color: #b6bccdd1 !important;
// }
// #login .main-container {
//   display: flex;
//   justify-content: center;
//   align-items: center;
// }
// #login .main-container .top {
//   margin-top: 150px;
//   font-size: 30px;
//   color: #ff962a;
//   display: flex;
//   justify-content: center;
// }
// #login .top .icon-kaoshi {
//   font-size: 80px;
// }
// #login .top .title {
//   margin-top: 20px;
// }
// #login .bottom {
//   display:flex;
//   justify-content: center;
//   background-color:#fff;
//   border-radius: 5px;
//   box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
// }
// #login .bottom .title {
//   text-align: center;
//   font-size: 30px;
// }
// .bottom .container .title {
//   margin: 30px 0px;;
// }
// .bottom .submit .row-login {
//   width: 100%;
//   background-color: #3186cb;
//   border-color: #ffffff;
//   margin: 20px 0px 10px 0px;
//   padding: 15px 20px;
// }
// .bottom .submit {
//   display: flex;
//   justify-content: center;
// }
// .footer {
//   margin-top: 50px;
//   text-align: center;
// }
// .footer .msg1 {
//   font-size: 18px;
//   color: #fff;
//   margin-bottom: 15px;
// }
// .footer .msg2 {
//   font-size: 14px;
//   color: #e3e3e3;
//   margin-top: 70px;
// }
// .bottom .options {
//   margin-bottom: 40px;
//   color: #ff962a;
//   display: flex;
//   justify-content: space-between;
// }
// .bottom .options > a {
//   color: #ff962a;
// }
// .bottom .options .register span:nth-child(1) {
//   color: #8C8C8C;
// }





* {
  margin: 0;
  padding: 0;
  font-family: 'El Messiri', sans-serif;
}

body {
  background: #031323;
  overflow: hidden;
}

.fas {
  width: 32px;
}

section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
  background-size: 400% 400%;
  animation: gradient 10s ease infinite;
}

@keyframes gradient {
    0% {
      background-position: 0% 50%;
      }
    50% {
      background-position: 100% 50%;
      }
    100% {
      background-position: 0% 50%;
      }
}

.box {
  position: relative;
  
  .square {
    position: absolute;
    background: rgba(173, 216, 230, 0.5);
    backdrop-filter: blur(5px);
    box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 15px;
    animation: square 10s linear infinite;
    animation-delay: calc(-1s * var(--i));
  }
  
  @keyframes square {
    0%,100% {
      transform: translateY(-20px);
    }
    
    50% {
      transform: translateY(20px);
    }
  }
  
  .square:nth-child(1) {
    width: 100px;
    height: 100px;
    top: -15px;
    right: -45px;
  }
  
  .square:nth-child(2) {
    width: 150px;
    height: 150px;
    top: 105px;
    left: -125px;
    z-index: 2;
  }
  
  .square:nth-child(3) {
    width: 60px;
    height: 60px;
    bottom: 85px;
    right: -45px;
    z-index: 2;
  }
  
  .square:nth-child(4) {
    width: 50px;
    height: 50px;
    bottom: 35px;
    left: -95px;
  }
  
  .square:nth-child(5) {
    width: 50px;
    height: 50px;
    top: -15px;
    left: -25px;
  }
  
  .square:nth-child(6) {
    width: 85px;
    height: 85px;
    top: 165px;
    right: -155px;
    z-index: 2;
  }
}

.container {
  position: relative;
  padding: 50px;
  width: 400px;
  min-height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border-radius: 10px;
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
}

.container::after {
  content: '';
  position: absolute;
  top: 5px;
  right: 5px;
  bottom: 5px;
  left: 5px;
  border-radius: 5px;
  pointer-events: none;
  background: linear-gradient( to bottom, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.1) 2%
  );
}

.form {
  position: relative;
  width: 100%;
  height: 100%;

   h2 {
    color: #fff;
    letter-spacing: 2px;
    margin-bottom: 30px;
    font-size: 2.0rem; /* 更大字号 */
    font-family: 'El Messiri', 'Montserrat', 'Arial', sans-serif; /* 更好看的字体 */
    font-weight: 700;
  }

  .inputBx {
    position: relative;
    width: 100%;
    margin-bottom: 20px;
    
    input {
      width: 80%;
      outline: none;
      border: none;
      border: 1px solid rgba(255, 255, 255, 0.2);
      background: rgba(255, 255, 255, 0.2);
      padding: 8px 10px;
      padding-left: 40px;
      border-radius: 15px;
      color: #fff;
      font-size: 16px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    }
    
    .password-control {
      position: absolute;
      top: 11px;
      right: 10px;
      display: inline-block;
      width: 20px;
      height: 20px;
      background: url(https://snipp.ru/demo/495/view.svg) 0 0 no-repeat;
      transition: 0.5s;
}
        
      .view {
         background: url(https://snipp.ru/demo/495/no-view.svg) 0 0 no-repeat;
        transition: 0.5s;
  }

    
  
    .fas {
      position: absolute;
      top: 13px;
      left: 13px;
    }
    
    input[type="submit"] {
      background: #007bff;
      color: #fff;
      max-width: 100px;
      padding: 8px 10px;
      box-shadow: none;
      letter-spacing: 1px;
      cursor: pointer;
      transition: 1.5s;
    }
    
    input[type="submit"]:hover {
      background: linear-gradient(115deg, 
        rgba(0,0,0,0.10), 
        rgba(255,255,255,0.25));
      color: #fff;
      transition: .5s;
    }
    
    input::placeholder {
      color: #fff;
    }
    
    span {
        position: absolute;
        left: 30px;
        padding: 10px;
        display: inline-block;
        color: #fff;
        transition: .5s;
        pointer-events: none;
      }
    
    input:focus ~ span,
    input:valid ~ span {
      transform: translateX(-30px) translateY(-25px);
      font-size: 12px;
    }
  }
  
  p {
    color: #fff;
    font-size: 15px;
    margin-top: 5px;
  
    a {
      color: #fff;
    }
    
    a:hover {
      background-color: #000;
      background-image: linear-gradient(to right, #434343 0%, black 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }
}

.remember {
  position: relative;
  display: inline-block;
  color: #fff;
  margin-bottom: 10px;
  cursor: pointer;
}
</style>
