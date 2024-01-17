from machine import Pin, ADC, I2C, PWM
from ssd1306 import SSD1306_I2C
from hcsr04 import HCSR04
from time import sleep, sleep_ms
import network
import time
import urequests
import gc

Infrarojo = Pin(13, Pin.IN, Pin.PULL_DOWN)
reed = Pin(33, Pin.IN)
led_ver = Pin(5, Pin.OUT)
led_amarelo = Pin(18, Pin.OUT)
led_verde = Pin(19, Pin.OUT)
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128,64,i2c)
sensor = HCSR04(trigger_pin=15, echo_pin=4)
buzzer = PWM(Pin(13), freq=440, duty=512)


def trocartexto_oled(seguir, detente, perigoso, bateu, distancia):
  sleep_ms(50)
  oled.fill(0)
  if seguir:
    oled.text("Distancia Segura",1,0)
  if detente:
    oled.text("Distancia Media ",1,0)
  if perigoso:
    oled.text("Distancia Perigosa ",1,0)
  if bateu:
    oled.text("Voce Bateu",1,0)
  if distancia:
    dis =  round(distance, 0)
    oled.text(f"{str(dis)}",40,15) 
  oled.show()

def SoundBuz(freq, sleep):
    buzzer.freq(freq)
    buzzer.duty(512)
    time.sleep(sleep)

while True:
  
  distance = sensor.distance_cm()
  dis =  round(distance, 0)

  
  valor_Infrarojo = Infrarojo.value()

  if distance < 5: 
    SoundBuz(640, 0.2)
    SoundBuz(880, 0.2)
    led_ver.value(1)
    led_amarelo.value(0)
    led_verde.value(0)
    trocartexto_oled(seguir=False, detente=False, perigoso = False, bateu = True, distancia=True)
    print("<b> Voce Bateu</b>")

   
     # gc.collect() libera a memoria que não esta sendo usada
    gc.collect()
   

  if distance >= 5 and distance < 100:
    SoundBuz(440, 0.4)
    SoundBuz(880, 0.4)
    led_ver.value(1)
    led_amarelo.value(0)
    led_verde.value(0)
    trocartexto_oled(seguir=False, detente= False, perigoso = True, bateu = False, distancia=True)
    print(f"<b>Distancia Perigosa {dis}</b>")
    
    # gc.collect() libera a memoria que não esta sendo usada
    gc.collect()
  
  if distance >= 100 and distance < 200:
    led_ver.value(0)
    led_amarelo.value(1)
    SoundBuz(520, 0.5)
    SoundBuz(720, 0.5)
    trocartexto_oled(seguir= False, detente= True, perigoso = False, bateu = False, distancia=True)
    led_verde.value(0)
    print(f"<b>Distancia Media {dis}</b>")
   
    # gc.collect() libera a memoria que não esta sendo usada
    gc.collect()

  if distance >= 200:
    buzzer.duty(0)
    led_ver.value(0)
    led_amarelo.value(0)
    led_verde.value(1)
    print(f"<b>Distancia Segura {dis}</b>")
    sleep(1)
    
    
    trocartexto_oled(seguir=True, detente=False, perigoso =  False, bateu = False, distancia=True)
    gc.collect()



