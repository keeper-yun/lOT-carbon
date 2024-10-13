
#include <U8g2lib.h>
#include <Wire.h>

// OLED设置为I2C模式，指定为SH1106的128x64分辨率
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);


const int co2ModeGet = A0;  // CO2传感器的模拟引脚
const int fanPin = 9;       // MOS管控制风扇的引脚
const int buzzerPin = 8;    // 定义蜂鸣器信号引脚为D8

int co2Value = 0;           // 用于存储CO2浓度值
int ppm = 1019;

void setup() {
  Serial.begin(9600);       // 初始化串口通信
  u8g2.begin();
  pinMode(fanPin, OUTPUT);  // 设置风扇引脚为输出
  pinMode(buzzerPin,OUTPUT);
  digitalWrite(buzzerPin, 0);

}


void error(){
  u8g2.setFont(u8g2_font_ncenB08_tr);  // 选择字体
  u8g2.drawStr(5,55,"Warning CO2 alarm!!!"); // 显示CO2浓度标题
  u8g2.sendBuffer();
}


void voice(){

  digitalWrite(buzzerPin, 1);
  delay(100);
  digitalWrite(buzzerPin, 0);

}


void read_co2() {

  co2Value = analogRead(co2ModeGet);
  
  Serial.print("测得CO2浓度为: ");
  Serial.print(co2Value);     // 打印CO2浓度
  Serial.println(" ppm");

  u8g2.clearBuffer();          // 清空显示缓冲区
  u8g2.setFont(u8g2_font_ncenB08_tr);  // 选择字体
  u8g2.drawStr(5,15,"CO2 Concentration:"); // 显示CO2浓度标题

  // 将CO2浓度数据显示到OLED屏幕上
  u8g2.setCursor(5, 35);
  u8g2.print(co2Value);
  u8g2.print(" ppm");

  u8g2.sendBuffer();
}


void loop() {
  delay(1000);

  read_co2();               // 读取并打印CO2浓度
  
  if (co2Value >= ppm) {   // 如果CO2浓度达到一定阈值
    Serial.println("CO2浓度过高,启动风扇...");
    digitalWrite(fanPin, HIGH);  // 启动风扇

    voice();
    error();

    delay(5000);            // 风扇运行5秒
  } else {
    digitalWrite(fanPin, LOW);   // 保持风扇关闭
  }

}