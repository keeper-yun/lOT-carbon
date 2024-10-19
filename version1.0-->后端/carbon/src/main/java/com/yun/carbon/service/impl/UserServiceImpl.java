package com.yun.carbon.service.impl;


import com.yun.carbon.entity.User;
import com.yun.carbon.mapper.UserMapper;
import com.yun.carbon.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;
    @Override
    public User findByUsername(String username) {
        return userMapper.findByUsername(username);
    }

}

