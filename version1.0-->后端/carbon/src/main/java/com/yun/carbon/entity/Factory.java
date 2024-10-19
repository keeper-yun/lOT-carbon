package com.yun.carbon.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

@Entity
@Data
public class Factory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long factoryId;
    private String factoryName;
    private String location;
    private String phone;
}

