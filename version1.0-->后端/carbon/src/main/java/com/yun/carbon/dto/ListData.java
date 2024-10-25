package com.yun.carbon.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ListData {
    @JsonProperty("time")
    private long time; // 时间戳
    @JsonProperty("value")
    private String value; // CO2 浓度值
    @JsonProperty("identifier")
    private String identifier;

    // getters and setters

    public String getIdentifier() {
        return identifier;
    }

    public void setIdentifier(String identifier) {
        this.identifier = identifier;
    }

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
