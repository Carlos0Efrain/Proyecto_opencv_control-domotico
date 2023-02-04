int motor = 46;
int Foco1 = 47;
int libre1 = 48;
int Foco2 = 49;
int libre2 = 50;
int contacto1= 51;
int libre3 = 52;
int contacto2= 53;
int option;
int a=0;
int r=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(Foco1, OUTPUT);
  pinMode(Foco2, OUTPUT);
  pinMode(contacto1, OUTPUT);
  pinMode(contacto2, OUTPUT);
  pinMode(libre1, OUTPUT);
  pinMode(libre2, OUTPUT);
  pinMode(motor, OUTPUT);
  pinMode(libre3, OUTPUT);  
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    option = Serial.read();
    Serial.println(option);
    
    
      if(option == 'A'){
          digitalWrite(Foco1, LOW);
          delay(50);
        }

      if(option == 'B'){
          digitalWrite(Foco2, LOW);
          delay(50);
        }  
      if(option == 'C'){
          digitalWrite(contacto1, LOW);
          delay(50);
        }

      if(option == 'D'){
          digitalWrite(contacto2, LOW);
          delay(50);
        } 
      if(option == 'E'){
          digitalWrite(motor, LOW);
          delay(50);
        }

      if(option == 'F'){
          digitalWrite(libre1, LOW);
          delay(50);
        }  
      if(option == 'G'){
          digitalWrite(libre2, LOW);
          delay(50);
        }

      if(option == 'H'){
          digitalWrite(libre3, LOW);
          delay(50);
        }  
        
   
    if(option == 'Z'){
      digitalWrite(Foco1, HIGH);
    }
    
    if(option == 'Y'){
      digitalWrite(Foco2, HIGH);
    }
  }
}
