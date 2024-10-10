const int fanPin = 9; // MOS管控制引脚

void setup() {
  pinMode(fanPin, OUTPUT); // 设置引脚为输出模式
}

void loop() {
  digitalWrite(fanPin, 1); // 打开风扇
  delay(3000);                 // 运行3秒
  digitalWrite(fanPin, 0);  // 关闭风扇
  delay(3000);                 // 停止3秒
}
