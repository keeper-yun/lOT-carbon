package com.yun.carbon.service;

import com.yun.carbon.dto.MonitoringDataDTO;
import com.yun.carbon.entity.MonitoringRecord;

import java.util.Date;
import java.util.List;

public interface MonitoringService {

    //给前端的数据
    List<MonitoringDataDTO> findAllRecords();
    List<MonitoringDataDTO> findLatestMonitoringDataForAllFactories();

    List<MonitoringDataDTO> findMonitoringDataInRange(Date startDate, Date endDate);


    //从OneNet云平台拿的数据



}
