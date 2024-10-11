package com.yun.carbon.mapper;

import com.yun.carbon.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserMapper extends JpaRepository<User,Integer> {
    User findByUsername(String username);
}
