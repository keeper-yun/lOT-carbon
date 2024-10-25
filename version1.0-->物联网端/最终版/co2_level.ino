
// #include <SoftwareSerial.h>

// SoftwareSerial mySerial(14, 15);

byte buffer[12];   //创建一个长度为12的字节数组
int co2Value;

void setup() {
  Serial.begin(9600);   //硬件串口    波特率：9600
  Serial2.begin(9600); //模拟软串口  波特率：9600
}

void loop() {
  
  delay(1000);
   if(Serial2.available()>=6)   // 如果串口接收到的字节数大于等于6个
   { 
      Serial2.readBytes(buffer, 6);  // 读取6个字节到数组中
      if(buffer[0] == 0x2C)
      {
         co2Value = buffer[1]*256+buffer[2];
      }

   }
   
  Serial.print("CO2: ");  
  Serial.print(co2Value); 
  Serial.println("ppm");

}



