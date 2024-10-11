package com.yun.carbon.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.math.BigDecimal;
import java.util.Date;

@Data
@AllArgsConstructor
public class MonitoringDataDTO {
    private Integer recordId;
    private String factoryName;
    private BigDecimal co2_Level;
    private BigDecimal co2_Flow;
    private BigDecimal co2_Output;
    private Date timestamp;
    private String location;
}
