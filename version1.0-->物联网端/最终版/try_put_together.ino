// #include <SoftwareSerial.h>
#include <Arduino.h>
#define RXTXBUF_SIZE 225
#define WAITTIME 800


// SoftwareSerial mySerial(10,11);//RX--->10  TX--->11
// SoftwareSerial mySerialC(6,7);
// SoftwareSerial mySerialF(3,4); 

const int fanPin = 9;
int WIFI_Reset = 12;
//char *WiFi_RX_BUF[256] = "";   //保存传入的数据
int WiFi_RxCounter = 0;
//int WiFi_RXBUFF_SIZE = 256;
char *RXTX_BUF = new char[RXTXBUF_SIZE];
const char *SSID = "wzc";//路由器名称
const char *PASS = "1104312167";//路由器密码
const char *ANSready = "ready";//回复的ready
//int ServerPort=8080;
//char *ServerIP="192.168.142.128";


char *ClientID= "CO2_READ";          //设备ID-存放客户端ID的缓冲区- 1035997083
char  ClientID_len= strlen(ClientID); //存放客户端ID的长度
char *Username= "TKDr9E8tk0";         //产品ID-存放用户名的缓冲区-569187
char  Username_len= strlen(Username); //存放用户名的长度
char *Passward= "version=2018-10-31&res=products%2FTKDr9E8tk0%2Fdevices%2FCO2_READ&et=3020404379&method=md5&sign=0PMtT22UnJNIAMiOaW1xKA%3D%3D";         //鉴权信息-存放密码的缓冲区-JianQuanXX 
char  Passward_len= strlen(Passward); //存放密码的长度
                                                             //订阅
// char *topicCMD = "AT+MQTTPUB=0,\"" + topic + "\",\"" + dataCMD + "\",1,0";
char *ServerIP= "mqtts.heclouds.com"; //存放服务器IP或是域名-=183.230.40.96，old：183.230.40.39
int  ServerPort = 1883;       //存放服务器的端口号-6002


char *topicPostPub = "$sys/TKDr9E8tk0/CO2_READ/thing/property/post";       //topic=>PUB                                                                     //订阅
char *topicPostSub = "$sys/TKDr9E8tk0/CO2_READ/thing/property/post/reply";  //订阅是要求平台操作或回应，topic，Onenet数据点上传topic（不用改）
//char *topicSetSub = "$sys/TKDr9E8tk0/CO2_READ/thing/property/set";          //订阅
char *topicSetPub = "$sys/TKDr9E8tk0/CO2_READ/thing/property/set_reply";    //topic，Onenet数据点上传topic（不用改）
char *dataCMD = "{\"id\":\"123\",\"version\":\"1.0\",\"params\":{\"PPM\":{\"value\": 418},\"speed\":{\"value\": 0.9}}}";  //更新参数
// char *dataCMD = "{\"id\":\"123\",\"version\":\"1.0\",\"params\":{\"PPM\":{\"value\": 351}}}";  //更新参数


unsigned char   Fixed_len;                     //固定报头长度
unsigned char   Variable_len;                  //可变报头长度
unsigned char   Payload_len;                   //有效负荷长度

char tst;
int t;
int co2Value;
byte buffer[12]; 
int i =0;
byte *buffer2=new byte[128];   //创建一个长度为12的字节数组
double SPEED;
const byte cmd_f[]={0x04,0x03,0x00,0x00,0x00,0x02,0xC4,0X5E};   //测风速指令
int integerPart;
int decimalPart;
int speedPos;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
  Serial1.begin(9600);//与ESP8266通信
  while(!Serial){}  //mySerial
  //同步等待Serial初始化成功
  pinMode(WIFI_Reset,OUTPUT);
  digitalWrite(WIFI_Reset,HIGH);

  pinMode(fanPin,OUTPUT);
  digitalWrite(fanPin,0);

//  mySerial.println("AT+CWMODE=1");//发送指令
  delay(2000);//简单延时改变模式，为了加入AP
  //WiFi_Reset(100);
  //WiFi_SendCmd("AT+CWMODE=1",100);

  //WiFi_JoinAP(100);

  if(WiFi_Connect_IoTServer()==0){
    delay(2000);
    WiFi_RxCounter = 0;
    memset(RXTX_BUF, 0 ,RXTXBUF_SIZE );

    while(Serial1.read()>=0){}
    MQTT_ConectPack();
    MQTT_TXData(RXTX_BUF,Fixed_len+Variable_len+Payload_len);
    MQTT_WaitBK("\x20\x02",50);

    delay(500);

    while(Serial1.read()>=0){}
      MQTT_Subscribe(topicPostSub,0);
      MQTT_TXData(RXTX_BUF,Fixed_len+Variable_len+Payload_len);
      MQTT_WaitBK("\x90\x03",50);

     delay(500);
    
     while(Serial1.read()>=0){}

     t = 351; 
     if( (t / 1000) >= 1 ){
       dataCMD[strlen(dataCMD)-30] = t / 1000 + '0';
     }else{
       dataCMD[strlen(dataCMD)-30] = t / 1000 + ' ';
     }
     dataCMD[strlen(dataCMD)-29] = (t / 100) % 10 + '0';
     dataCMD[strlen(dataCMD)-28] = (t / 10) % 10 + '0';
     dataCMD[strlen(dataCMD)-27] = t % 10 + '0';


    SPEED = 1.5;
    integerPart = (int)SPEED; 
    decimalPart = (int)((SPEED - integerPart) * 10); 

    if( (integerPart / 10) >= 1 ){
      dataCMD[strlen(dataCMD)-7] = (integerPart / 10) % 10 + '0'; // 十位
    }else{
      dataCMD[strlen(dataCMD)-7] = ' ';
    }
    dataCMD[strlen(dataCMD)-6] = integerPart % 10 + '0'; // 个位
    dataCMD[strlen(dataCMD)-5] = '.'; // 小数点
    dataCMD[strlen(dataCMD)-4] = decimalPart + '0'; // 小数部分


    Serial.println(dataCMD);

    //  MQTT_PublishQos(topicPostPub, dataCMD ,strlen(dataCMD) );
    //  MQTT_TXData(RXTX_BUF,Fixed_len+Variable_len+Payload_len);
    //  MQTT_WaitBK("\x30",100);

     
  }
  
}


void loop() {

     delay(10);

     while(Serial1.read()>=0){}

     t = readCO2(); 
     if( (t / 1000) >= 1 ){
       dataCMD[strlen(dataCMD)-30] = t / 1000 + '0';
     }else{
       dataCMD[strlen(dataCMD)-30] = t / 1000 + ' ';
     }
     dataCMD[strlen(dataCMD)-29] = (t / 100) % 10 + '0';
     dataCMD[strlen(dataCMD)-28] = (t / 10) % 10 + '0';
     dataCMD[strlen(dataCMD)-27] = t % 10 + '0';

     

    delay(10);

    while(Serial1.read()>=0){}

    SPEED = readFLOW();
    integerPart = (int)SPEED; 
    decimalPart = (int)((SPEED - integerPart) * 10); 

    if( (integerPart / 10) >= 1 ){
      dataCMD[strlen(dataCMD)-7] = (integerPart / 10) % 10 + '0'; // 十位
    }else{
      dataCMD[strlen(dataCMD)-7] = ' ';
    }
    dataCMD[strlen(dataCMD)-6] = integerPart % 10 + '0'; // 个位
    dataCMD[strlen(dataCMD)-5] = '.'; // 小数点
    dataCMD[strlen(dataCMD)-4] = decimalPart + '0'; // 小数部分

    Serial.println(dataCMD);

    MQTT_PublishQos(topicPostPub, dataCMD ,strlen(dataCMD) );
    MQTT_TXData(RXTX_BUF,Fixed_len+Variable_len+Payload_len);
    MQTT_WaitBK("\x30",100);

    if(t >= 600)
     fans();

     
}



double readFLOW(){
  
  // mySerialF.begin(9600);
  Serial3.write(cmd_f,(sizeof(cmd_f)/sizeof(cmd_f[0])));  
  delay(1000);
   for (int i = 0; i < 64; i++) 
   {
      buffer2[i] = Serial3.read();
   }
   for(int ii=0;ii<64;ii++)
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


int readCO2(){

  //读CO2浓度代码
      // mySerialC.begin(9600);
      Serial2.begin(9600);
     if(Serial2.available()>=6)   // 如果串口接收到的字节数大于等于6个
   { 
      Serial2.readBytes(buffer, 6);  // 读取6个字节到数组中
      if(buffer[0] == 0x2C)
      {
         co2Value = buffer[1]*256+buffer[2];
      }

      // Serial.println(i);
      // i++;
   }
    Serial.print("CO2: ");  
    Serial.print(co2Value); 
    Serial.println(" ppm");
  return co2Value;
}


void fans(){
  digitalWrite(fanPin, 1); // 打开风扇
  delay(5000);                 // 运行5秒
  digitalWrite(fanPin, 0);  // 关闭风扇
  delay(5000);  
}


/* @参数名:WiFi_Reset 
 * @参数:timeout--->超时时间
 * @返回值:0--->正确 其他:错误
 */
int WiFi_Reset(int timeout){
  WiFi_RxCounter = 0;//WiFi接受数据量变量清零
  memset(RXTX_BUF,0,RXTXBUF_SIZE);//清空WiFi接收缓冲区
  sprintf(RXTX_BUF,"AT+RST\r\n");//发送连接服务器指令
  Serial.print(RXTX_BUF);//回显指令
  Serial1.print(RXTX_BUF);//发送指令
  memset(RXTX_BUF,0,RXTXBUF_SIZE);//清空WiFi接收缓冲区
  while(timeout--){
    delay(50);
    while(Serial1.available()){
      RXTX_BUF[WiFi_RxCounter] = (char)Serial1.read();
      if(RXTX_BUF[WiFi_RxCounter] == ANSready[WiFi_RxCounter])
      {
        WiFi_RxCounter++;
      }
      else
      {
        WiFi_RxCounter = 0;
      }
      if(ANSready[WiFi_RxCounter]=='\0')
      {
        Serial.println(RXTX_BUF);  //串口输出信息
        WiFi_RxCounter = 0;
        memset(RXTX_BUF,0,RXTXBUF_SIZE);
        return 0;
      }
    }


  }
//      WiFi_RxCounter++;
//      delayMicroseconds(800);//延时等待读完整的buffer
//    
//    if(strstr(WiFi_RX_BUF,"OK")) /[表情]rstr--->子串匹配函数，如果匹配到OK说明连接成功
//    break;                    //主动跳出while循环
//  }
//  Serial.print(WiFi_RX_BUF);  //串口输出信息 如果成功则输出成功信息
  if(timeout <= 0)return 1; //  如果超时时间到了，timeout <= 0,返回1 失败
  return 0;//成功
}





/*
 * @函数名：WiFi_SendCmd
 */

 char WiFi_SendCmd(const char* cmd,int timeout)
 {
  WiFi_RxCounter = 0;
  memset(RXTX_BUF,0,RXTXBUF_SIZE);
  Serial1.println(cmd);  //发送指令
  while(timeout--)
  {
    delay(100);
    while(Serial1.available())
    {
      RXTX_BUF[WiFi_RxCounter]=(char)Serial1.read();
      WiFi_RxCounter++;
      delay(20);
    }
    
    if(strstr(RXTX_BUF,"OK"))
      break;
    Serial.print(timeout);
  }
  Serial.println(RXTX_BUF);
  Serial.println("2200443011王子超");
  if(timeout <= 0) return 1;
  else return 0;
 }


/*-------------------------------------------------*/
/*函数名：WiFi连接服务器                           */
/*参  数：无                                       */
/*返回值：0：正确   其他：错误                     */
/*-------------------------------------------------*/
char WiFi_Connect_IoTServer(void)
{ 
  //WiFi_Reset(50);
  Serial.println("准备复位模块");                   
  if(WiFi_Reset(100))                //复位，100ms超时单位，总计5s超时时间
  {                             
    Serial.println("复位失败，准备重启+++");        //返回非0值，进入if
    return 1;                                 //返回1
  }else Serial.println("复位成功+++");                 
  
  Serial.println("准备设置STA模式");                
  if(WiFi_SendCmd("AT+CWMODE=1",100))        //设置STA模式，100ms超时单位，总计5s超时时间
  {             
    Serial.println("设置STA模式失败，准备重启");  //返回非0值，进入if
    return 2;                                 //返回2
  }else Serial.println("设置STA模式成功");          
  
  Serial.println("准备取消自动连接");               
  if(WiFi_SendCmd("AT+CWAUTOCONN=0",50))      //取消自动连接，100ms超时单位，总计5s超时时间
  {       
    Serial.println("取消自动连接失败，准备重启"); //返回非0值，进入if
    return 3;                                 //返回3
  }else Serial.println("取消自动连接成功");         
      
  Serial.println("准备连接路由器");                  
  if(WiFi_SendCmd("AT+CWJAP=\"wzc\",\"1104312167\"",100))               //连接路由器,1s超时单位，总计30s超时时间
  {                          
    Serial.println("连接路由器失败，准备重启");   //返回非0值，进入if
    return 4;                                 //返回4 
  }else Serial.println("连接路由器成功");          

  Serial.println("准备设置透传");                    
  if(WiFi_SendCmd("AT+CIPMODE=1",50))       //设置透传，100ms超时单位，总计5s超时时间
  {           
    Serial.println("设置透传失败，准备重启");     //返回非0值，进入if
    return 8;                                 //返回8
  }else Serial.println("设置透传成功");              
  
  Serial.println("准备关闭多路连接");               
  if(WiFi_SendCmd("AT+CIPMUX=0",50))          //关闭多路连接，100ms超时单位，总计5s超时时间
  {            
    Serial.println("关闭多路连接失败，准备重启"); //返回非0值，进入if
    return 9;                                 //返回9
  }else Serial.println("关闭多路连接成功");         
   
  Serial.println("准备连接服务器");                 
  if(WiFi_SendCmd("AT+CIPSTART=\"TCP\",\"mqtts.heclouds.com\",1883",300))              //连接服务器，100ms超时单位，总计10s超时时间
  {            
    Serial.println("连接服务器失败，准备重启");   //返回非0值，进入if
    return 10;                                //返回10
  }else Serial.println("连接服务器成功");           

  Serial.println("准备进入透传");                 
  if(WiFi_SendCmd("AT+CIPSEND",100))              //连接服务器，100ms超时单位，总计10s超时时间
  {            
    Serial.println("进入透传失败，准备重启");   //返回非0值，进入if
    return 11;                                //返回10
  }else Serial.println("进入透传成功");           
  return 0;                                   //正确返回0
}


void MQTT_TXData(char *tempbuff,int lenght){

  Serial.println("报文发送:");
  for(int i=0;i<lenght;i++){
    Serial.print(tempbuff[i]/16);
    Serial.print(tempbuff[i]%16);
  }
  Serial.println("报文结束");
  for(int i=0;i<lenght;i++)
    Serial1.write(tempbuff[i]);
  
}

/*-------------------------------------------------*/
/*函数名：等待MQTT服务器回复                          */
/*参  数：timeout：超时时间（1s的倍数）                */
/*返回值：0：正确   其他：错误                         */
/*-------------------------------------------------*/
char MQTT_WaitBK(char *flag,int timeout)
{   
  WiFi_RxCounter = 0;                  //WiFi接收数据量变量清零                        
  memset(RXTX_BUF,0,RXTXBUF_SIZE);    //清空WiFi接收缓冲区     
  while(timeout--){                    //等待超时时间到0
    delay(300);                         //延时50ms
    while(Serial1.available())
    {
      RXTX_BUF[WiFi_RxCounter]=(char)Serial1.read();
      WiFi_RxCounter++;
      timeout=1;                       //=1，以便判if断接收结果
      delayMicroseconds(WAITTIME);     //等待 WAITTIME=800s(9600)/80(115200)，拖时间，读完整的buffer
    }
    if(strstr(RXTX_BUF,flag))          //如果接收到表示成功connack=0->\x2002（与上一函数不同之处）
      Serial.println("succ");
      break;                   
    Serial.println();
    Serial.print(timeout);             //串口输出现在的超时时间
  }
  //Serial.print("\r\nresponse:");     //表示成功，否则不成功
  for(int i=0;i<WiFi_RxCounter;i++)
      Serial.write(RXTX_BUF[i]);       //串口输出信息
  Serial.println();
  if(timeout <= 0)return 1;            //如果timeout<=0，说明超时时间到了，也没能收到WIFI GOT IP，返回1
  return 0;                            //正确，返回0
}


void MQTT_ConectPack(void){
 
  int temp,Remaining_len;
  
  Fixed_len = 1;                                                        //连接报文中，固定报头长度暂时先=1
  Variable_len = 10;                                                    //连接报文中，可变报头长度=10
  Payload_len = 2 + ClientID_len + 2 + Username_len + 2 + Passward_len; //连接报文中，负载长度      
  Remaining_len = Variable_len + Payload_len;                           //剩余长度=可变报头长度+负载长度

  //固定报头（Fixed header）:
  RXTX_BUF[0]=0x10;                    //第1个字节(7-4bit)类型:1+0 -》0x10？  
  do{                                   //循环处理固定报头中的剩余长度字节，字节量根据剩余字节的真实长度变化
    temp = Remaining_len%128;           //剩余长度取余128
    Remaining_len = Remaining_len/128;  //剩余长度取整128
    if(Remaining_len>0)                 
      temp |= 0x80;                     //按协议要求位7置位          
    RXTX_BUF[Fixed_len] = temp;        //剩余长度字节记录一个数据
    Fixed_len++;                        //固定报头总长度+1    
  }while(Remaining_len > 0);            //如果Remaining_len>0的话，再次进入循环
  //可变报头（Variable header）:
  RXTX_BUF[Fixed_len + 0] = 0x00;      //可变报头第1个字节 ：固定0x00 MSB            
  RXTX_BUF[Fixed_len + 1] = 0x04;      //可变报头第2个字节 ：固定0x04 LSB
  RXTX_BUF[Fixed_len + 2] = 0x4D;      //可变报头第3个字节 ：固定0x4D M
  RXTX_BUF[Fixed_len + 3] = 0x51;      //可变报头第4个字节 ：固定0x51 Q
  RXTX_BUF[Fixed_len + 4] = 0x54;      //可变报头第5个字节 ：固定0x54 T
  RXTX_BUF[Fixed_len + 5] = 0x54;      //可变报头第6个字节 ：固定0x54 T
  RXTX_BUF[Fixed_len + 6] = 0x04;      //可变报头第7个字节 ：固定0x04 V3.1.1
  RXTX_BUF[Fixed_len + 7] = 0xC2;      //可变报头第8个字节 ：使能用户名和密码校验，不使用遗嘱，不保留会话
  RXTX_BUF[Fixed_len + 8] = 0x00;      //可变报头第9个字节 ：保活时间高字节 0x01
  RXTX_BUF[Fixed_len + 9] = 0x3c;      //可变报头第10个字节：保活时间低字节 0x00   256s

  RXTX_BUF[Fixed_len+10] = ClientID_len/256;
  RXTX_BUF[Fixed_len+11] = ClientID_len%256;
  memcpy(&RXTX_BUF[Fixed_len+12] , ClientID , ClientID_len) ;
  
  RXTX_BUF[Fixed_len + 12 + ClientID_len] = Username_len/256;
  RXTX_BUF[Fixed_len + 13 + ClientID_len] = Username_len%256;
  memcpy(&RXTX_BUF[Fixed_len+14+ClientID_len] , Username , Username_len) ;

  RXTX_BUF[Fixed_len + 14 + ClientID_len+Username_len] = Passward_len/256;
  RXTX_BUF[Fixed_len + 15 + ClientID_len+Username_len] = Passward_len%256;
  memcpy(&RXTX_BUF[Fixed_len + 16 + ClientID_len + Username_len] , Passward , Passward_len) ;
  
}


/*函数名：SUBSCRIBE订阅topic报文                              */
/*参  数：QoS：订阅等级                                       */
/*参  数：topic_name：订阅topic报文名称                        */
/*功  能：按协议包装订阅信息包（仅topic和Qos）                   */
/*返回值：无                                                 */
void MQTT_Subscribe(char *topic_name,int Qos ){
  Fixed_len = 2;                                                       //连接报文中，固定报头长度暂时先=1
  Variable_len = 2;
  Payload_len = 2 + strlen(topic_name) + 1;

  RXTX_BUF[0]=0x82; 
  RXTX_BUF[1]=Variable_len + Payload_len; 

  RXTX_BUF[2] = 0x00;
  RXTX_BUF[3] = 0x01;

  RXTX_BUF[4] = strlen(topic_name)/256;
  RXTX_BUF[5] = strlen(topic_name)%256;

  memcpy(&RXTX_BUF[6],topic_name,strlen(topic_name));
  RXTX_BUF[6 + strlen(topic_name)] = Qos;
  
}



void MQTT_PublishQos(const char *topic,char *data,int data_len){
  
  int temp,Remaining_len;
  
  Fixed_len = 1;
  Variable_len = 2 + strlen(topic);
  Payload_len = data_len;
  Remaining_len = Variable_len + Payload_len;

  RXTX_BUF[0]=0x30;
  do{
    temp = Remaining_len% 128;
    Remaining_len = Remaining_len/128;
    if(Remaining_len>0)
      temp |= 0x80;
    RXTX_BUF[Fixed_len] = temp;
    Fixed_len++;
  }while(Remaining_len>0);

  RXTX_BUF[Fixed_len + 0] = strlen(topic)/256;
  RXTX_BUF[Fixed_len + 1] = strlen(topic)%256;
  memcpy(&RXTX_BUF[Fixed_len + 2],topic,strlen(topic));

  memcpy(&RXTX_BUF[Fixed_len + 2 + strlen(topic) ] , data , data_len) ;
  RXTX_BUF[Fixed_len + 2 + strlen(topic) + data_len ] = '\0';

  
}




 
