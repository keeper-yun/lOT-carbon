#include <U8g2lib.h>
#include <Wire.h>

// 使用U8G2库并设置为I2C模式，指定为SH1106的128x64分辨率
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup() {
  // 初始化OLED显示屏
  u8g2.begin();

  // 设置初始显示内容
  u8g2.clearBuffer();          // 清空缓冲区
  u8g2.setFont(u8g2_font_ncenB08_tr);  // 选择字体
  u8g2.drawStr(0,10,"Hello, guo!"); // 显示文字
  u8g2.sendBuffer();           // 发送缓冲区内容到屏幕
}

void loop() {
  // 可在这里更新显示内容
}
