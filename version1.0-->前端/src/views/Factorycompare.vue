<template>
    <div ref="chart" style="width: 1000px; height: 500px;"></div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Factorycompare',
  
    data() {
      return {
        chartData: {
          xAxisData: [], // 日期
          seriesData: [], // 每个工厂的排放数据
          factoryNames: [] // 工厂名称
        }
      };
    },
  
    methods: {
      fetchData() {
        axios.get('http://localhost:8181/monitoring/findByDate')
          .then(resp => {
            const groupedData = {};
  
            // 按日期和工厂分组计算总排放量
            resp.data.forEach(item => {
              const date = item.timestamp.split(' ')[0]; // 提取日期部分
              const factoryName = item.factoryName;
              const output = item.co2_Output;
  
              if (!groupedData[date]) {
                groupedData[date] = {};
              }
  
              if (!groupedData[date][factoryName]) {
                groupedData[date][factoryName] = 0;
              }
  
              groupedData[date][factoryName] += output; // 累计排放量
            });
  
            // 准备 x 轴和系列数据
            this.chartData.xAxisData = Object.keys(groupedData).sort(); // x 轴数据（日期）
            this.chartData.factoryNames = [...new Set(resp.data.map(item => item.factoryName))]; // 唯一的工厂名称
  
            this.chartData.seriesData = this.chartData.factoryNames.map(factory => {
              return this.chartData.xAxisData.map(date => {
                return groupedData[date][factory] ; // 如果没有数据则用 0
              });
            });
  
            this.updateChart();
          })
          .catch(error => {
            console.error('获取数据时出错:', error);
          });
      },
  
      updateChart() {
        if (!this.$echarts) {
          console.error('ECharts 不可用!');
          return;
        }
  
        const chart = this.$echarts.init(this.$refs.chart);

        console.log('xAxisData:', this.chartData.xAxisData);
        console.log('seriesData:', this.chartData.seriesData);
        console.log('factoryData:',this.chartData.factoryNames);

  
        const option = {
          title: {
            text: '每周工厂碳排放总量',
          },
          tooltip: {
            trigger: 'axis',
          },
          legend: {
            data: this.chartData.factoryNames, // 工厂名称
          },
          xAxis: {
            type: 'category',
            data: this.chartData.xAxisData, // x 轴数据（日期）
          },
          yAxis: {
            type: 'value',
            name: '排放量 (kg)'
            },
          series: this.chartData.factoryNames.map((factory, index) => ({
            name: factory,
            type: 'line',
            stack: '总量', // 开启堆叠
            data: this.chartData.seriesData[index], // 每个工厂的数据
          })),
        };
  
        chart.setOption(option);
      }

    },
  
    mounted() {
      this.fetchData();
    }
  };
  </script>
  