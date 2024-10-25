//package com.yun.carbon.dto;
//
//import com.fasterxml.jackson.annotation.JsonProperty;
//
//import java.math.BigDecimal;
//import java.util.Date;
//
//public class MonitoringDataDTOnet {
//    @JsonProperty("time")
//    private long timestamp; // 保持为 long 类型以处理时间戳
//
//    @JsonProperty("value")
//    private BigDecimal co2Level; // CO2 浓度值
//
//    // getters and setters
//    public long getTimestamp() {
//        return timestamp;
//    }
//
//    public void setTimestamp(long timestamp) {
//        this.timestamp = timestamp;
//    }
//
//    public BigDecimal getCo2Level() {
//        return co2Level;
//    }
//
//    public void setCo2Level(BigDecimal co2Level) {
//        this.co2Level = co2Level;
//    }
//}