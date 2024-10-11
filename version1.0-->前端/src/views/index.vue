<template>
  <div id="App">
    <el-container style="height: 90%; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-menu router :default-openeds="['0']">
          <el-submenu
            v-for="(route, index) in filteredRoutes"
            :key="index"
            :index="index.toString()"
          >
            <template #title>
              <i class="el-icon-menu"></i>{{ route.name }}
            </template>
            <el-menu-item
              v-for="(child, childIndex) in route.children"
              :key="childIndex"
              :index="child.path"
              :class="{ 'is-active': $route.path === child.path }"
            >
              {{ child.name }}
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header style="text-align: right; font-size: 10px">
          <h1 style="text-align: center; font-size: 150%">智能碳中和检测系统</h1>

        </el-header>

        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  computed: {
    filteredRoutes() {
      return this.$router.options.routes
        .map(route => ({
          ...route,
          children: route.children ? route.children.filter(child => child.show) : []
        }))
        .filter(route => route.children.length > 0);
    }
  }
}
</script>
