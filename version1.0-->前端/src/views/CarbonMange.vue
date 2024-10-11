<template>
  <div ref="chart" style="width: 1000px; height: 500px;"></div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CarbonMange',

  data() {
    return {
      chartData: {
        xAxisData: [],
        seriesData: [],
      }
    };
  },

  methods: {
    fetchData() {
      axios.get('http://localhost:8181/monitoring/findLatest')
        .then(resp => {
          // 假设 response.data 是你提供的数据数组
          const factoryName = resp.data.map(item => item.factoryName);
          const output = resp.data.map(item => item.co2_Output);

          this.chartData = {
            xAxisData: factoryName,
            seriesData: output
          };

          // 更新图表数据
          this.updateChart();
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },

    updateChart() {
      if (!this.$echarts) {
        console.error('ECharts is not available!');
        return;
      }

      const chart = this.$echarts.init(this.$refs.chart);

      const option = {
        title: {
          text: '碳中和排放动态表',
        },
        tooltip: {},
        xAxis: {
          data: this.chartData.xAxisData,
        },
        yAxis: {},
        series: [
          {
            name: '碳排放量:kg',
            type: 'bar',
            data: this.chartData.seriesData,
            itemStyle: {
              // 设置不同颜色
              color: (params) => {
                // const colors = ['#ff7f50', '#87cefa', '#da70d6', '#32cd32', '#6495ed'];
                const colors = ['#ff7f50', '#da70d6', '#87cefa', '#32cd32', '#fff3cd'];
                return colors[params.dataIndex % colors.length]; // 循环使用颜色
              },
            }
          },
        ],
      };

      chart.setOption(option);
    }
  },

  mounted() {
    // Fetch data and update the chart
    this.fetchData();
  }
};
</script>

