**项目名：-->  智能碳中和检测系统项目  -->  碳然生“卫”-智能碳中和检测系统**
 * 项目制作人：王子超，熊梓妍
 * 项目结构：物联网端，后端，web前端，微信小程序端，数据预测端，DeepSeek问答端
 * 暂无
<br><br><br><br/>

**项目概要**
  * 一.设计背景
  * 二.系统总体架构
  * 三.技术应用
<br><br><br/>

**一.设计背景**
* (1) 中国政府提出了“双碳”目标，即在2030年前实现碳达峰、2060年前实现碳排放。
* (2) 实现这一目标需要对碳排放进行精准监测、高效管理与科学分析，这对技术手段提出了更高的要求。
* (3) 因此，我们设计了一款智能碳排放监测系统，专注于对CO2、N2O和CH4的精准监测与分析。这些气体是工业领域碳排放的关键因素，因此成为我们系统的主要监测对象。
<br><br><br/>

**二.系统架构**
  <br><br/>
  * ![结构图2](https://github.com/user-attachments/assets/15999918-6d4a-486f-8614-f140fa2d9c6d)
  <br><br/>
  * 系统拥有两条完整链路，分别是：上行链路，下行链路。
  <br><br/>
  * （1）上行链路
     <br><br/>CO2传感器
    * ![image](https://github.com/user-attachments/assets/64529595-56e4-40ca-a1be-bc55129c2c7d)

     <br><br/>N2O传感器，CH4传感器
    * ![1741141641717](https://github.com/user-attachments/assets/a0a1945e-3b89-44b8-a4e7-a7c5a0a9fab4)
      
     <br><br/>Arduino MEGA 2560主板
    * ![image](https://github.com/user-attachments/assets/f12de09c-02e2-405b-99d3-a1febb043ebc)
      
    <br><br/>ATK-ESP8266 WIFI模块
    * ![image](https://github.com/user-attachments/assets/db366952-c17d-44f7-b17a-0f932e5a8de9)
     
    * 上行链路：从左侧传感器开始，分别有CO2传感器（二氧化碳），N2O传感器（一氧化二氮），CH4传感器（甲烷），流速传感器（空气流速）。
      <br/>1.传感器采集到的数据为RS485信号,而Arduino MEGA 2560主板只能采集TTL信号，故采用RS485转TTL模块，将RS485信号转化成TTL信号让Arduino MEGA 2560主板接收。
      <br/>2.Arduino MEGA 2560主板与ATK-ESP8266 WIFI模块相连接（看正负电压，引脚等通过杜邦线连接），用C语言编程发送MQTT信号，发送报文等等给 OneNET云平台。（在物联网端代码中有源码的）
      <br/>3.OneNET云平台注册设备等在‘开发者文档’里有的，包括订阅，发送数据信号等。
      <br><br/>
      ![image](https://github.com/user-attachments/assets/d2897c6b-f2f1-4c1f-b30f-bcd25ed77710)
      ![image](https://github.com/user-attachments/assets/3be313c8-eb18-49c4-81df-8d8bebac7968)
      <br/>4.https://iot-api.heclouds.com/thingmodel/query-device-property?product_id=产品名称&device_name=设备名称 ，这是实时采集到的数据API接口，OneNET云平台给出的就是json数据，后端SpringBoot调用这个接口就能拿到数据，后面写入数据库，调给前端，小程序什么的就是程序员常规操作了。注：在后端代码中可以看到我是如何调用的。（不止一个api接口，还可以查询历史数据）
      ![image](https://github.com/user-attachments/assets/ae81e134-879e-4dda-affb-ab49d28bd968)
      <br/>5.这里我使用的是物模型，就是OneJson的数据协议。
   <br><br/>
   
  * （2）下行链路
     * 
      

      

      






