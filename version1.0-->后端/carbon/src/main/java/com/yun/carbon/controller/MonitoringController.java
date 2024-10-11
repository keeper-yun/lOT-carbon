package com.yun.carbon.controller;

import com.yun.carbon.dto.MonitoringDataDTO;
import com.yun.carbon.entity.MonitoringRecord;
import com.yun.carbon.mapper.MonitoringRecordMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Date;
import java.util.List;
import java.util.TimeZone;

@RestController
@RequestMapping("/monitoring")
public class MonitoringController {

    @Autowired
    private MonitoringRecordMapper monitoringRecordMapper;

//    @GetMapping("/findAll")
//    public List<MonitoringRecord> findAll() {
//        return monitoringRecordMapper.findAll();
//    }
    @GetMapping("/findAll")
    public List<MonitoringDataDTO> findAllData() {
        return monitoringRecordMapper.findAllMonitoringData();
    }


//    @GetMapping("/findLatest")
//    public MonitoringRecord findLatest() {
//        return monitoringRecordMapper.findTopByOrderByTimestampDesc()
//                .orElse(null); // 如果没有记录，返回null
//    }
    @GetMapping("/findLatest")
    public List<MonitoringDataDTO> getLatestMonitoringData() {
        if(monitoringRecordMapper.findAllMonitoringData() != null){
            return monitoringRecordMapper.findLatestMonitoringDataForAllFactories();
        }else{
            return null;
        }
                 // 如果没有记录，返回null
    }


//    所有时间范围接口
//    @GetMapping("/monitoringData")
//    public List<MonitoringDataDTO> getMonitoringData(
//            @RequestParam("startDate") String startDateStr,
//            @RequestParam("endDate") String endDateStr) throws ParseException {
//
//        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
//        Date startDate = sdf.parse(startDateStr);
//        Date endDate = sdf.parse(endDateStr);
//
//        return monitoringRecordMapper.findMonitoringDataInRange(startDate, endDate);
//    }


    @GetMapping("/findByDate")
    public List<MonitoringDataDTO> getMonitoringData() throws ParseException {
        // 获取三周前的日期
        LocalDate threeWeeksAgo = LocalDate.now().minusDays(45);
        Date startDate = Date.from(threeWeeksAgo.atStartOfDay(ZoneId.systemDefault()).toInstant());
        // 当前时间
        Date endDate = new Date();
        // 调用方法获取监测数据
        return monitoringRecordMapper.findMonitoringDataInRange(startDate, endDate);
    }

}
