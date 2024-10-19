package com.yun.carbon.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.springframework.data.jpa.repository.Temporal;

import java.math.BigDecimal;
import java.time.LocalDateTime;
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
