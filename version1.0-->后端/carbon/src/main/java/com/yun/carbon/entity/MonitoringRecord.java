package com.yun.carbon.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

import java.math.BigDecimal;
import java.util.Date;

@Entity
@Data
public class MonitoringRecord {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer recordId;
    private Integer factoryId;
    private BigDecimal co2_Level;
    private BigDecimal co2_Flow;
    private BigDecimal co2_Output;
    private Date timestamp;

}
