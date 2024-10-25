package com.yun.carbon.interceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String username = (String) request.getSession().getAttribute("username");

        // 允许访问注册页面
        String requestURI = request.getRequestURI();
        if (requestURI.equals("/Register")) {
            return true;
        }

        if (username == null || username.isEmpty()) {
            response.sendRedirect("/login");
            return false;
        }

        return true;
    }
}
