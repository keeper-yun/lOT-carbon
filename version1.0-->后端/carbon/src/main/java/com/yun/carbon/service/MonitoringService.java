package com.yun.carbon.service;

import com.yun.carbon.dto.MonitoringDataDTO;

import java.util.Date;
import java.util.List;

public interface MonitoringService {
    List<MonitoringDataDTO> findAllRecords();
    List<MonitoringDataDTO> findLatestMonitoringDataForAllFactories();

    List<MonitoringDataDTO> findMonitoringDataInRange(Date startDate, Date endDate);

}
