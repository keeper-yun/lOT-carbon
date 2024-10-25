// /**********************************************************************************
//  * 描述    ：Arduino UNO, 波特率：9600, 485读取风速大小  
//  * 硬件连接：        
//  * 485风速传感器：12V+ -> 12V; GND -> GND;  A -> A; B -> B; GND -> GND; 
//  * 485转TTL模块：GND -> GND; VCC -> 5V; RXD -> D6; TXD -> D7;  ----模拟软串口   波特率：9600
//  * 功能描述：软件模拟串口外接485风速传感器读取风速 
//  *          硬件串口输出风速值
//  * 使用说明：先下载好程序再接线
// **********************************************************************************/
// #include <SoftwareSerial.h>

// //实例化软串口
// SoftwareSerial mySerial(3, 4); // RX, TX

// byte buffer[128];   //创建一个长度为12的字节数组
// double SPEED,TEMP;

// const byte cmd_f[]={0x04,0x03,0x00,0x00,0x00,0x02,0xC4,0X5E};   //测风速指令
// // const byte cmd_t[]={0x04,0x05,0x00,0x00,0x00,0x02,0x4C,0X5E};   //测温度指令


// void cmd_test1()
// {
//   mySerial.write(cmd_f,(sizeof(cmd_f)/sizeof(cmd_f[0])));  
// }

// // void cmd_test2()
// // {
// //   mySerial.write(cmd_t,(sizeof(cmd_t)/sizeof(cmd_t[0])));  
// // }

// void setup() 
// {
//   Serial.begin(9600);   //硬件串口    波特率：9600
//   mySerial.begin(9600); //模拟软串口  波特率：9600
// }

// void loop() 
// {
//   cmd_test1();
//   delay(1000);
//   // cmd_test2();
//   // delay(100); 

//    for (int i = 0; i < 128; i++) 
//    {
//       buffer[i] = mySerial.read();
//    }
//    for(int ii=0;ii<128;ii++)
//    {
//     if(buffer[ii]==0x04 && buffer[ii+1]==0x03  && ii<110)
//     {
//        SPEED = buffer[ii+6]/10.0;         
//     }
//    }
//   // for(int ii=0;ii<128;ii++)
//   // {
//   //  if(buffer[ii]==0x04 && buffer[ii+1]==0x05  && ii<110)
//   //  {
//   //    TEMP = ((buffer[ii+5]*256+buffer[ii+6])-400)/10.0;         
//   //  }
//   // } 

//     Serial.print("Speed:");
//     Serial.print(SPEED);  
//     Serial.println(" m/s");  
    
//     // Serial.print("Temp:");
//     // Serial.print(TEMP);  
//     // Serial.println(" ℃");  

//     Serial.println(" ");
// }





// #include <SoftwareSerial.h>

// SoftwareSerial mySerialF(3, 4); // RX, TX

byte buffer2[128];   //创建一个长度为12的字节数组
double SPEED;

const byte cmd_f[]={0x04,0x03,0x00,0x00,0x00,0x02,0xC4,0X5E};   //测风速指令

void setup() 
{
  Serial.begin(9600);   //硬件串口    波特率：9600
  Serial3.begin(9600);
  // mySerialF.begin(9600); //模拟软串口  波特率：9600
}

void loop() 
{

    SPEED = readFLOW();
}

double readFLOW(){

  Serial3.write(cmd_f,(sizeof(cmd_f)/sizeof(cmd_f[0])));  
  delay(1000);
   for (int i = 0; i < 128; i++) 
   {
      buffer2[i] = Serial3.read();
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
