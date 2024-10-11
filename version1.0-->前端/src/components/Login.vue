
<template>
    <div class="login-background"></div> <!-- 背景元素 -->
    <div class="login-container">
      <h2>登录</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">用户名:</label>
          <input type="text" v-model="username" id="username" required>
        </div>
        <div class="form-group">
          <label for="password">密码:</label>
          <input type="password" v-model="password" id="password" required>
        </div>
        <div class="button-group">
          <button type="submit" class="login-button">登录</button>
          <button type="button" class="register-button" @click="goToRegister">注册</button>
        </div>
      </form>
      <p class="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        message: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://localhost:8181/user/login', {
            username: this.username,
            password: this.password
          });
          if (response.data === 'success') {
            sessionStorage.setItem('user', this.username);
            this.$router.push('/CarbonMange');
          } else {
            this.message = '账号密码不正确!';
          }
        } catch (error) {
          console.error('Error during login:', error);
          this.message = '登录时出错!';
        }
      },
      goToRegister() {
        this.$router.push('/Register'); // 跳转到注册页面
      }
    }
  };
  </script>
  
  <style scoped>

    .auth-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.8); /* 半透明白色背景 */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: relative; /* 用于定位背景 */
    z-index: 1; /* 确保内容在背景上方 */
    }

    .login-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('@/assets/flower.jpeg'); /* 设置背景图片路径 */
    background-size: cover; /* 背景覆盖整个容器 */
    background-position: center; /* 背景居中 */
    z-index: -1; /* 使背景在内容后面 */
    }


  .login-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

  }
  
  .login-container h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .form-group input {
    width: calc(100% - 20px);
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-sizing: border-box;
    font-size: 14px;
  }
  
  .button-group {
    display: flex;
    justify-content: space-between;
  }
  
  .login-button {
    width: 40%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
    font-size: 14px;
    cursor: pointer;
  }
  
  .login-button:hover {
    background-color: #0056b3;
  }
  
  .register-button {
    width: 40%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    margin-right: 20px; /* 增加右边距 */
    background-color: #28a745; /* 注册按钮颜色 */
    color: white;
    font-size: 14px;
    cursor: pointer;
  }
  
  .register-button:hover {
    background-color: #218838; /* 注册按钮悬停颜色 */
  }
  
  .message {
    text-align: center;
    margin-top: 15px;
    color: red;
  }
  </style>
  