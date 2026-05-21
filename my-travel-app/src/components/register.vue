
<template>
<section style="position: relative; min-height: 100vh; overflow: hidden;">
    <!-- 视频背景 -->
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
  
  <div class="register-container">
    <h2 class="title">注册Wander AI</h2>

    <form @submit.prevent="handleRegister">
      <input type="text" v-model="registerForm.name" placeholder="用户名">
      <input type="text" v-model="registerForm.email" placeholder="邮箱">
      <div style="display:flex;align-items:center;">
        <input type="text" v-model="registerForm.code" placeholder="验证码" style="flex:1; font-size:18px; font-family:'El Messiri',sans-serif; color:rgba(0,0,0);">
        <button
          type="button"
          @click="sendCode"
          :disabled="codeCountdown>0"
          style="height:50px; font-size:18px; font-family:'El Messiri',sans-serif; margin-left:10px; border-radius:100px; background:rgba(255,255,255,0.5); border:5px solid transparent; color:#fff; padding:0 20px; transition:0.3s; cursor:pointer;"
        >
          {{ codeCountdown>0 ? codeCountdown+'s后重试' : '发送验证码' }}
        </button>
      </div>
      <input type="password" v-model="registerForm.password" placeholder="密码">
      <input type="password" v-model="registerForm.confirmPassword" placeholder="确认密码">
      <input type="submit" value="注册">
    </form>
    <div style="width:100%; text-align:center; margin-top: 10px;">
      <button
        type="button"
        @click="$router.push('/login')"
        style="background: none; border: none; color: #007bff; font-size: 16px; cursor: pointer; text-decoration: underline;"
      >
        已有账号？去登录
      </button>
    </div>   

    </div>
  </div>
  </section>

</template>

<script>
export default {
  name: "UserRegister",
  data() {
    return {
      registerForm: {
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      codeCountdown: 0,
      codeTimer: null,
      rules: {
        name: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
        ]
      }
    };
  },
  methods: {
async sendCode() {
      if (!this.registerForm.email) {
        this.$message.error('请先填写邮箱');
        return;
      }
      // 邮箱格式校验
      const emailReg = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
      if (!emailReg.test(this.registerForm.email)) {
        this.$message.error('请输入正确的邮箱格式');
        return;
      }
      try {
        await this.$api.auth.sendEmailCode({ email: this.registerForm.email });
        this.$message.success('验证码已发送');
        this.codeCountdown = 60;
        this.codeTimer = setInterval(() => {
          this.codeCountdown--;
          if (this.codeCountdown <= 0) clearInterval(this.codeTimer);
        }, 1000);
      } catch (e) {
        const msg = e.message || '验证码发送失败';
        this.$message.error(msg);
      }
    },
    validatePassword(rule, value, callback) {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入密码不一致'));
      } else {
        callback();
      }
    },
    async handleRegister() {
      // 简单校验
      if (!this.registerForm.name || !this.registerForm.email || !this.registerForm.password) {
        this.$message.error('请填写完整信息');
        return;
      }
      const emailReg = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
      if (!emailReg.test(this.registerForm.email)) {
        this.$message.error('请输入正确的邮箱格式');
        return;
      }
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.$message.error('两次输入密码不一致');
        return;
      }
      if (!this.registerForm.code) {
        this.$message.error('请输入验证码');
        return;
      }
      try {
        // 调用后端注册接口
        const response = await this.$api.auth.register({
          name: this.registerForm.name,
          email: this.registerForm.email,
          password: this.registerForm.password,
          code: this.registerForm.code
        });
        if (response.data && response.data.success) {
          this.$message.success('注册成功');
          this.$router.push('/login');
        } else {
          this.$message.error(response.data?.error?.message || '注册失败');
        }
      } catch (e) {
        this.$message.error(e.message || '注册失败');
      }
    }

  }
};
</script>

<style lang="less" scoped>
*{
    margin: 0;
    padding: 0;
    font-family: 'El Messiri', sans-serif;
    /* transition: 0.3s; */
}

body {
  background: #031323;
  overflow: hidden;
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

.register-container {
  position: relative;
  width: 400px;
  padding: 50px;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border-radius: 10px;
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
    /* background-color: #ffffff49; */
    /* border-radius: 50px; */
    /* box-shadow: 0 0 30px rgba(255, 255, 255, 0.5) inset; */
}

.register-container::after {
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



.title{
    font-size: 30px;
    margin-bottom: 30px;
    color: #fff;
    text-shadow: 0 0 10px #ff9dff80;
}

input[type="text"],
input[type="password"]{
    width: 100%;
    height: 50px;
    margin: 10px 0;
    box-sizing: border-box;
    color: rgba(0,0,0);
    border: 5px solid transparent;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 100px;
    padding: 5px 20px 0 20px;
    transition: 0.3s;
    font-size: 18px;
    outline: none
}


input[type="text"]:hover,
input[type="password"]:hover {
    background: rgba(255, 255, 255, 0);
    border: 5px solid #ffffff;
}

input[type="submit"] {
    width: 100%;
    height: 50px;
    padding: 10px;
    margin: 15px 0;
    border-radius: 100px;
    border: none;
    background-color: #007bff;
    color:#fff;
    cursor:pointer;
    font-size: 20px;
    letter-spacing: 3px;
}

input::placeholder {
    color: #fff;
}

#password {
    border:none;
    background-color: #ffffff00;
    color: #fff;
    font-size: 18px;
}
</style>