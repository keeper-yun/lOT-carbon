<!-- <template>
	<div id="app">
		<p>If Echarts is successfully added to this project, you'll see an BarChart below</p>
		<div id="main" :style="{width: '300px', height: '300px'}"></div>
		<HelloWorld msg="Welcome to Your Vue.js App" />
	</div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";

export default {
	name: "app",
	components: {
		HelloWorld,
	},
	mounted() {
		this.initChart();
	},
	methods: {
		initChart() {
			var myChart = this.$echarts.init(document.getElementById("main"));
			myChart.setOption({
				title: {
					text: "ECharts 入门示例",
				},
				tooltip: {},
				xAxis: {
					data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
				},
				yAxis: {},
				series: [
					{
						name: "销量",
						type: "bar",
						data: [5, 20, 36, 10, 10, 20],
					},
				],
			});
		},
	},
};
</script>

<style>
#app {
	font-family: "Avenir", Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px;
}
#main {
	margin: auto;
}
</style> -->



<template>
    <router-view></router-view>
</template>

<style>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>

<script>
export default {};
</script>
