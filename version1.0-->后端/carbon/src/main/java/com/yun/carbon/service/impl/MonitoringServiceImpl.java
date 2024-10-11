package com.yun.carbon.service.impl;

import com.yun.carbon.dto.MonitoringDataDTO;
import com.yun.carbon.entity.MonitoringRecord;
import com.yun.carbon.mapper.MonitoringRecordMapper;
import com.yun.carbon.service.MonitoringService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;
import java.util.Optional;

@Service
public class MonitoringServiceImpl implements MonitoringService {

    @Autowired
    private MonitoringRecordMapper monitoringRecordMapper;

    //10秒所有数据都要更新一次
//    @Scheduled(fixedRate = 10000)
//    public void fetchMonitoringData() {
//        List<MonitoringRecord> records = findAllRecords();
//        // 可以在这里进行处理或存储状态
//        System.out.println("Fetched monitoring records: " + records);
//    }
    @Scheduled(fixedRate = 10000)
    public void fetchMonitoringData() {
        List<MonitoringDataDTO> records = findAllRecords();
        // 可以在这里进行处理或存储状态
        System.out.println("(All)Fetched monitoring records: " + records);
    }

    // 定时每10秒读取一条最新数据
//    @Scheduled(fixedRate = 10000)
//    public void fetchMonitoringData2() {
//        Optional<MonitoringRecord> record = monitoringRecordMapper.findTopByOrderByTimestampDesc();
//        record.ifPresent(r -> {
//            // 在这里处理或存储状态
//            System.out.println("Fetched monitoring record: " + r);
//        });
//    }
    @Scheduled(fixedRate = 10000)
    public void fetchMonitoringData2() {
        List<MonitoringDataDTO> records = findLatestMonitoringDataForAllFactories();
        // 遍历每条记录并处理

            // 在这里处理或存储状态
        System.out.println("(Latest)Fetched monitoring record: " + records);
            // 例如，可以将其存储到某个数据结构中或进行其他操作

    }


//    @Override
//    public List<MonitoringRecord> findAllRecords() {
//        return monitoringRecordMapper.findAllMonitoringData();
//    }
    @Override
    public List<MonitoringDataDTO> findAllRecords() {
        return monitoringRecordMapper.findAllMonitoringData();
    }

    @Override
    public List<MonitoringDataDTO> findLatestMonitoringDataForAllFactories() {
        return monitoringRecordMapper.findLatestMonitoringDataForAllFactories();
    }

    @Override
    public List<MonitoringDataDTO> findMonitoringDataInRange(Date startDate, Date endDate) {
        return monitoringRecordMapper.findMonitoringDataInRange(startDate, endDate);
    }

}
