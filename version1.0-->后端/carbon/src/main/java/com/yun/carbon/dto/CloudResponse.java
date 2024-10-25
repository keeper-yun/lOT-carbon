package com.yun.carbon.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class CloudResponse {

//    @JsonProperty("data")
//    private CloudData data;
//
//    public CloudData getData() {
//        return data;
//    }
//
//    public void setData(CloudData data) {
//        this.data = data;
//    }

    @JsonProperty("data")
    private List<ListData> data;

    public List<ListData> getData() {
        return data;
    }

    public void setData(List<ListData> data) {
        this.data = data;
    }

}

