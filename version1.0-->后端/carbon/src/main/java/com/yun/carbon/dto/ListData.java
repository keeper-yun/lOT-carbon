package com.yun.carbon.dto;

public class ListData {
    private long time; // 时间戳
    private String value; // CO2 浓度值

    // getters and setters
    public long getTime() {
        return time;
    }

    public void setTime(long time) {
        this.time = time;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
