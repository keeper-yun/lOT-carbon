#include <SoftwareSerial.h>

//实例化软串口
SoftwareSerial mySerial(3, 4); // RX, TX

byte buffer2[128];   //创建一个长度为12的字节数组
double SPEED;

const byte cmd_f[]={0x04,0x03,0x00,0x00,0x00,0x02,0xC4,0X5E};   //测风速指令

void setup() 
{
  Serial.begin(9600);   //硬件串口    波特率：9600
  mySerialF.begin(9600); //模拟软串口  波特率：9600
}

void loop() 
{

    SPEED = readFLOW();
}

double readFLOW(){

  mySerialF.write(cmd_f,(sizeof(cmd_f)/sizeof(cmd_f[0])));  
  delay(1000);
   for (int i = 0; i < 128; i++) 
   {
      buffer2[i] = mySerialF.read();
   }
   for(int ii=0;ii<128;ii++)
   {
    if(buffer2[ii]==0x04 && buffer2[ii+1]==0x03  && ii<110)
    {
       SPEED = buffer2[ii+6]/10.0;         
    }
   }
    Serial.print("Speed:");
    Serial.print(SPEED);  
    Serial.print(" m/s"); 
    Serial.println(" ");
   return SPEED;

}
