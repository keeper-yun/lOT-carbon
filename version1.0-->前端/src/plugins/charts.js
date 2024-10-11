// import * as echarts from 'echarts/core';
// import { BarChart,LineChart } from 'echarts/charts';
// import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components';
// import { CanvasRenderer } from 'echarts/renderers';

// echarts.use([TitleComponent, TooltipComponent, GridComponent, BarChart,LineChart, CanvasRenderer]);

// export default {
//   install(app) {
//     // 将 ECharts 作为全局属性
//     app.config.globalProperties.$echarts = echarts;
//   },
// };


import * as echarts from 'echarts/core';
import {
  BarChart,
  LineChart
} from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent
} from 'echarts/components';
import { LabelLayout, UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

// 注册必须的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  BarChart,
  LineChart,
  LabelLayout,
  UniversalTransition,
  CanvasRenderer
]);

export default {
  install(app) {
    // 将 ECharts 作为全局属性
    app.config.globalProperties.$echarts = echarts;
  },
};
