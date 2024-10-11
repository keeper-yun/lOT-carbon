package com.yun.carbon.controller;


import com.yun.carbon.entity.User;
import com.yun.carbon.mapper.UserMapper;
import com.yun.carbon.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/login")
    public String login(@RequestBody User user) {
        User userFromDb = userService.findByUsername(user.getUsername());
        if (userFromDb != null && userFromDb.getPassword().equals(user.getPassword())) {
            return "success";
        } else {
            return "error";
        }
    }

    @Autowired
    private UserMapper userMapper;

    @GetMapping("/findAll")
    public List<User> findAll(){
        return userMapper.findAll();
    }

    @PostMapping("/register")
    public String register(@RequestBody User user) {
        // 检查用户名是否存在
        User existingUser = userService.findByUsername(user.getUsername());
        if (existingUser != null) {
            return "error: 用户名已存在";
        }

        // 保存新用户
        User savedUser = userMapper.save(user);
        if (savedUser != null) {
            return "success";
        } else {
            return "error";
        }
    }

    @GetMapping("/findById/{id}")
    public User findById(@PathVariable("id")Integer id){
        return userMapper.findById(id).get();
    }

    @GetMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id")Integer id){
        userMapper.deleteById(id);
    }

}
