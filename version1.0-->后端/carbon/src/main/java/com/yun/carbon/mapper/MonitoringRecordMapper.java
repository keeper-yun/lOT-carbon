package com.yun.carbon.mapper;

import com.yun.carbon.dto.MonitoringDataDTO;
import com.yun.carbon.entity.MonitoringRecord;
import org.apache.ibatis.annotations.Param;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Date;
import java.util.List;
import java.util.Optional;

@Repository
public interface MonitoringRecordMapper extends JpaRepository<MonitoringRecord, Integer> {
//    Optional<MonitoringRecord> findTopByOrderByTimestampDesc(); // 查询最新的一条记录


    //查询实时数据
@Query("SELECT new com.yun.carbon.dto.MonitoringDataDTO(" +
        "m.recordId, f.factoryName, m.co2_Level, m.co2_Flow, m.co2_Output, m.timestamp, f.location) " +
        "FROM MonitoringRecord m JOIN Factory f ON m.factoryId = f.factoryId " +
        "WHERE m.timestamp = (SELECT MAX(m2.timestamp) FROM MonitoringRecord m2 WHERE m2.factoryId = m.factoryId)")
List<MonitoringDataDTO> findLatestMonitoringDataForAllFactories();

    //查询所有数据
    @Query("SELECT new com.yun.carbon.dto.MonitoringDataDTO(m.recordId, f.factoryName, m.co2_Level, m.co2_Flow, m.co2_Output, m.timestamp, f.location) " +
            "FROM MonitoringRecord m JOIN Factory f ON m.factoryId = f.factoryId")
    List<MonitoringDataDTO> findAllMonitoringData();

    //自己设置时间范围
    @Query("SELECT new com.yun.carbon.dto.MonitoringDataDTO(m.recordId, f.factoryName, m.co2_Level, m.co2_Flow, m.co2_Output, m.timestamp, f.location) " +
            "FROM MonitoringRecord m JOIN Factory f ON m.factoryId = f.factoryId " +
            "WHERE m.timestamp BETWEEN :startDate AND :endDate")
    List<MonitoringDataDTO> findMonitoringDataInRange(@Param("startDate") Date startDate, @Param("endDate") Date endDate);

}
