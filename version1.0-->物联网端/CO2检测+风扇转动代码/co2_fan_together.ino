const int co2ModeGet = A0;  // CO2传感器的模拟引脚
const int fanPin = 9;       // MOS管控制风扇的引脚
int co2Value = 0;           // 用于存储CO2浓度值
int ppm = 1019;

void setup() {
  Serial.begin(9600);       // 初始化串口通信
  pinMode(fanPin, OUTPUT);  // 设置风扇引脚为输出
}

void read_co2() {

  co2Value = analogRead(co2ModeGet);
  
  Serial.print("测得CO2浓度为: ");
  Serial.print(co2Value);     // 打印CO2浓度
  Serial.println(" ppm");
}

void loop() {
  delay(1000);

  read_co2();               // 读取并打印CO2浓度
  
  if (co2Value >= ppm) {   // 如果CO2浓度达到一定阈值
    Serial.println("CO2浓度过高,启动风扇...");
    digitalWrite(fanPin, HIGH);  // 启动风扇
    delay(5000);            // 风扇运行5秒
  } else {
    digitalWrite(fanPin, LOW);   // 保持风扇关闭
  }

}
