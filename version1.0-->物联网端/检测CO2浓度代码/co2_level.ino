const int co2ModeGet = A0;  // 模拟引脚
const int co2DigitalGet = 2;   // 数字引脚

void setup() {
  Serial.begin(9600);           // 初始化串口通信
  pinMode(co2status, INPUT); // 设置数字引脚为输入
}

void loop() {
  int co2Value = analogRead(co2ModeGet); // 读取模拟值
  int co2Status = digitalRead(co2DigitalGet); // 读取数字值

  Serial.print("测得CO2浓度为: ");
  Serial.print(co2Value); // 打印模拟值
  Serial.println(" ppm");
  Serial.print("CO2状态: ");
  Serial.println(co2Status); // 打印数字值

  delay(1000); // 每秒读取一次
}



