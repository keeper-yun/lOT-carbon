<!-- <template>
    <el-form :model="form" @submit.prevent="handleRegister">
      <el-form-item label="用户名" prop="username" required>
        <el-input v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password" required>
        <el-input type="password" v-model="form.password"></el-input>
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-select v-model="form.role" placeholder="选择角色">
          <el-option label="普通用户" value="普通用户"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister">注册</el-button>
      </el-form-item>
    </el-form>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        form: {
          username: '',
          password: '',
          role: '普通用户'  // 默认角色
        }
      };
    },
    methods: {
      handleRegister() {
        axios.post('http://localhost:8181/user/register', this.form)
          .then(response => {
            if (response.data === 'success') {
              this.$message.success('注册成功');
            } else {
              this.$message.error(response.data);
            }
          })
          .catch(error => {
            this.$message.error('注册失败');
            console.error(error);
          });
      }
    }
  };
  </script>
   -->


   <template>
    <div class="register-container">
      <el-card class="register-card" shadow="always">
        <h2 class="register-title">用户注册</h2>
        <el-form :model="form" @submit.native.prevent="handleRegister" label-width="100px">
          <el-form-item label="用户名" prop="username" required>
            <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password" required>
            <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item label="角色" prop="role">
            <el-select v-model="form.role" placeholder="选择角色">
              <el-option label="普通用户" value="普通用户"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleRegister" class="register-button">注册</el-button>
          </el-form-item>
        </el-form>
        <div class="login-link">
          <span>已有账号？</span>
          <el-button type="text" @click="$router.push('/login')">登录</el-button>
        </div>
      </el-card>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        form: {
          username: '',
          password: '',
          role: '普通用户'  // 默认角色
        }
      };
    },
    methods: {
      handleRegister() {
        axios.post('http://localhost:8181/user/register', this.form)
          .then(response => {
            if (response.data === 'success') {
              this.$message.success('注册成功');
              this.$router.push('/login');
            } else {
              this.$message.error(response.data);
            }
          })
          .catch(error => {
            this.$message.error('注册失败');
            console.error(error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f7fa;
  }
  
  .register-card {
    width: 400px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .register-title {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
  }
  
  .register-button {
    width: 100%;
  }
  
  .login-link {
    text-align: center;
    margin-top: 20px;
  }
  </style>
  