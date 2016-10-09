// Written:
// by Yash Bhalgat | Kalpesh Patil | Meet Shah
// IIT Bombay


#include <Servo.h> 
#include <stdio.h>
#include <string.h>
#include <math.h>

Servo bottom;  // bottom- azimuth
Servo top;  // top - alt     

int posx = 0,posy=0;    		// variable to store the servo position 

int servo_max = 180;  			// Maximum no of rotation units of servo in one direction

int altservo_offset = 0;
int az_deg = 0;
int alt_deg = 0;

int laserPin1 = 13;
int laserPin = 7;

int prev_alt = 0;
int prev_az = 0;
int current_alt = 0;
int current_az = 0;
int del = 5;

float serialGetFloat(){
	char bytes[9], sign;
	int nbytes = 0;
	float fex;
	bool recv = false;
	
	bytes[8] = '\0';

	Serial.println("float");

	while(!recv){
		if (Serial.available() > 0) {
			sign = Serial.read();//Float with eight representation bytes (including dot and sign)
                        
			while(nbytes < 8)
				if(Serial.available() > 0){
					bytes[nbytes] = Serial.read();
					nbytes++;
				}
			fex = strtod(bytes, NULL);
                        //Serial.println(bytes);
			if(sign=='-')
				fex = 0.0 - fex;
			recv = true;
		}
	}

	Serial.println("_OK_");
	return fex;
}


void laserOn(){
	digitalWrite(laserPin1, HIGH);
        digitalWrite(laserPin, HIGH);
}

void laserOff(){
	digitalWrite(laserPin1, LOW);
        digitalWrite(laserPin, LOW);
}
 
void setup() 
{ 
  top.attach(8);  // top - alt
  bottom.attach(9);  // bottom - azimuth
  Serial.begin(9600);
  Serial.println("init");
  pinMode(laserPin,OUTPUT); 
  pinMode(laserPin1,OUTPUT); 
  digitalWrite(laserPin1, LOW);
  digitalWrite(laserPin, LOW);
  top.write(altservo_offset);
  bottom.write(0);
  int max_alt_input = 180-altservo_offset;
  prev_alt = 0;
  prev_az = 0;
} 
 
 
void loop() 
{ 
        
    float t0;
	float ar, dec, t;
	float ac, alt;
	char comm[5];
	char dir;
	int bytes_recv = 0;
	bool mov_end;

	comm[4]='\0';
	Serial.println("cmd");
	while(bytes_recv < 4)
	{
		//Waiting for a command...
		if (Serial.available() > 0)
			comm[bytes_recv++] = Serial.read();
	}
	
	//Obtaining the expected parameters of the command
	if(strcmp(comm, "set1")==0 || strcmp(comm, "set2")==0 || strcmp(comm, "set3")==0 || strcmp(comm, "goto")==0)
	{       

		ar = serialGetFloat();
		dec = serialGetFloat();
		t = serialGetFloat();
                if((ar>4.6 && ar<4.7) && (dec>0.15 && dec<0.25)){
                    digitalWrite(13, HIGH);
                }

	}
	if(strcmp(comm, "move")==0)
	{
		ac = serialGetFloat();
		alt = serialGetFloat();
		t = serialGetFloat();
	}
	
	//Executing command
		
	if(strcmp(comm, "time")==0)
	{
		t0 = serialGetFloat();
		Serial.println();
		Serial.println("done_time");
	}
	
	else if(strcmp(comm, "set1")==0)
	{	
				Serial.println();
		Serial.println("done_set1");
	}

	else if(strcmp(comm, "set2")==0){		
		Serial.println();
		Serial.println("done_set2");
	}

	else if(strcmp(comm, "set3")==0){		
		Serial.println();
		Serial.println("done_set3");
	}

	else if(strcmp(comm, "goto")==0)
	{

        az_deg = ar*180/3.14159;
        alt_deg = dec*180/3.14159;
        
        if(az_deg > 180){
          az_deg = az_deg-180;
          alt_deg = 180-alt_deg;
        }
        
        current_alt = (int)(min(alt_deg+altservo_offset, 180));
        current_az = (int)(az_deg);

        if(prev_az < current_az){
        	for(int i=prev_az; i<=current_az; i++){
				bottom.write(i);          
				delay(del);
			}
        }
        else{
        	for(int i=prev_az; i>=current_az; i--){
				bottom.write(i);          
				delay(del);
			}
        }

        if(prev_alt < current_alt){
        	for(int i=prev_alt; i<=current_alt; i++){
				top.write(i);          
				delay(del);
			}
        }
        else{
        	for(int i=prev_alt; i>=current_alt; i--){
				top.write(i);          
				delay(del);
			}
        }
        prev_az = current_az;
        prev_alt = current_alt;
        
		Serial.println("done_goto");
	}

	
	else if(strcmp(comm, "movx")==0)
	{
		while(Serial.available()<=0){}
		dir = Serial.read();
        // Serial.println(dir);
        if(dir == '1'){
          posx = (posx+1)%servo_max;
          bottom.write(posx);
        }
        else if(dir == '0') {
          posx = (posx-1)%servo_max;
          bottom.write(posx);
        }
        else{}
                
	}

	else if(strcmp(comm, "movy")==0){
		while(Serial.available()<=0){}
		dir = Serial.read();
        if(dir == '1'){
          posy = (posy+1)%servo_max;
          top.write(posy);
        }
        else if(dir == '0') {
          posy = (posy-1)%servo_max;
          top.write(posy);
        }
        else{}
	}

	else if(strcmp(comm, "init")==0)
	{
		Serial.println();
		Serial.println();
		Serial.println("done_init");
	}
	
	else if(strcmp(comm, "laon")==0)
	{
		laserOn();
		Serial.println();
		Serial.println("done_laserOn");
	}

	else if(strcmp(comm, "loff")==0)
	{
		laserOff();
		Serial.println();
		Serial.println("done_laserOff");
	}

	else if(strcmp(comm, "stop")==0)
	{
		Serial.println("done_stop");
	}

	else	
		Serial.println("ERROR");
  } 

