<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">

  <el-form-item label="账号" prop="username">
  <el-input v-model="ruleForm.username"></el-input>
</el-form-item>

<el-form-item label="密码" prop="password">
  <el-input v-model="ruleForm.password"></el-input>
</el-form-item>

<el-form-item>
  <el-button type="primary" @click="submitForm('ruleForm')">更新管理员信息</el-button>
  <el-button @click="resetForm('ruleForm')">清空</el-button>
</el-form-item>


</el-form>

</template>

<script>
import Axios from 'axios';

export default {
  data() {
    return {
      ruleForm: {
        username: '',
        password: '',
      },
      rules: {
          username: [
          { required: true, message: '账号不能为空', trigger: 'blur' },    
          ],
          password: [
          { required: true, message: '密码不能为空', trigger: 'blur' }
          ]
        
      }
    };
  },
  methods: {
    submitForm(formName) {
      const _this = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          Axios.post('http://localhost:8181/user/save',this.ruleForm).then(function(resp){
              if(resp.data=="success"){
                  _this.$message({
                  message: '管理员信息修改成功!',
                  type:'success'
                  });
                  _this.$router.push('/UserMange')
              }else{
                  _this.$message.error('管理员加入失败');
              }
          })
        }else{
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  },
  created(){
      alert(this.$route.query.id);
      const _this = this
      Axios.get('http://localhost:8181/user/findById/'+this.$route.query.id).then(function(resp){
          _this.ruleForm = resp.data
      })
  }
}
</script>