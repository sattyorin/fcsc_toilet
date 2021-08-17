#include <Adafruit_NeoPixel.h>

#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
ros::NodeHandle  nh;
String led_mode = "hoge";

#define LED_DATA_PIN 6
#define BUTTON_PIN 4
#define NUMPIXELS 8
// #define MOVE 0
// #define MOVE2WAIT 1
// #define WAIT 2
Adafruit_NeoPixel pixels(NUMPIXELS, LED_DATA_PIN, NEO_GRB + NEO_KHZ800);

void messageCb( const std_msgs::String& toggle_msg){
  led_mode=toggle_msg.data;
  pixels.clear();
  if(led_mode=="MOVE")for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(255, 0, 0));
  if(led_mode=="MOVE2WAIT")for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(255, 255, 0));
  if(led_mode=="WAIT")for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(0, 255, 0));
  pixels.show();
}
ros::Subscriber<std_msgs::String> sub("toggle_led_state", messageCb );
std_msgs::Bool msg_user_switch_state;
ros::Publisher pub_user_switch_state("user_switch_state", &msg_user_switch_state);


void setup() {
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pixels.begin();
    nh.initNode();
    nh.advertise(pub_user_switch_state);
    nh.subscribe(sub);
}

// void set_led_state(int state){
//   pixels.clear();
//   if(state==MOVE)for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(255, 0, 0));
//   if(state==MOVE2WAIT)for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(255, 255, 0));
//   if(state==WAIT)for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(0, 255, 0));
//   pixels.show();
// }
void loop() {
  msg_user_switch_state.data=digitalRead(BUTTON_PIN);
  pub_user_switch_state.publish(&msg_user_switch_state);
  nh.spinOnce();
  delay(100);
}
