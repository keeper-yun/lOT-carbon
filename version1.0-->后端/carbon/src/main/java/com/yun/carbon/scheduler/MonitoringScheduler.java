//package com.yun.carbon.scheduler;
//
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.scheduling.annotation.Scheduled;
//import org.springframework.stereotype.Component;
//
//import java.util.List;
//
//@Component
//public class MonitoringScheduler {
//
//    @Autowired
//    private MonitoringRecordService monitoringRecordService;
//
//    @Scheduled(fixedRate = 10000)
//    public void fetchMonitoringRecords() {
//        List<MonitoringRecord> records = monitoringRecordService.getMonitoringRecords();
//        // 处理获取的记录，例如保存到缓存中
//    }
//}
//
