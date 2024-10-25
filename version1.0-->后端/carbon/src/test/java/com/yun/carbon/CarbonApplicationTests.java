package com.yun.carbon;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Random;

@SpringBootTest
class CarbonApplicationTests {

    @Test
    void contextLoads() {
        Random random = new Random();
        int num = random.nextInt(1,6);
        System.out.println(num);
    }

}
