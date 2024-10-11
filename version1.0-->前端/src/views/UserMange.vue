<template>
    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        label="管理员编号"
        prop="userId">
      </el-table-column>
      <el-table-column
        label="账号"
        prop="username">
      </el-table-column>
      <el-table-column
        label="密码"
        prop="password">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作">
        <template #default="scope">
          <el-button
            size="mini"
            type="warning"
            @click="Edit(scope.row)">修改</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="Delete( scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </template>
  
  <script>
    import Axios from 'axios';
    export default {
      data() {
        return {
          tableData: []
          
        }
      },
      methods: {
        Edit(row) {
        this.$router.push({
          path:'/UpdateUser',
          query:{
            id:row.userId
          }
        })
        
      },
      Delete(row){
        // alert(row.username)
        console.log(row)
        const _this = this;
        Axios.get('http://localhost:8181/user/deleteById/'+row.userId).then(function(resp){
          _this.$alert(' 管理员“' + row.username + '”失去管理权限!', '删除管理员', {
          confirmButtonText: '确定',
          callback: action => {
            // _this.$router.push('/UserMange')
            window.location.reload()
          }
        })
        })
      },

      },
      created(){
        const _this = this
        Axios.get('http://localhost:8181/user/findAll').then(function(resp){
            console.log(resp.data)
                _this.tableData = resp.data.slice(1)
            
        })
      }
    }
  </script>