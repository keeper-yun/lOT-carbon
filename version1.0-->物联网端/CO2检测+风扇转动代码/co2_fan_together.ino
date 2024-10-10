
const int co2ModeGet = A0;  // 模拟引脚
const int fanPin = 9; // MOS管控制引脚

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);           // 初始化串口通信
  pinMode(fanPin, OUTPUT);

}

void loop() {

  delay(1000);
  digitalWrite(fanPin, 0);

  int co2Value = analogRead(co2ModeGet); // 读取模拟值
  Serial.print("测得CO2浓度为: ");
  Serial.print(co2Value); // 打印模拟值
  Serial.println(" ppm");

  if(co2Value > 1020){
    delay(1000);
    digitalWrite(fanPin, 1);
    delay(5000);
  }
  

}
