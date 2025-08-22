import network
import socket
from time import sleep
from picozero import pico_temp_sensor
from ssd1306 import SSD1306_I2C
from machine import Pin,I2C

ssid = 'GROUP10N'
password = 'password'
i2c=I2C(0,scl=Pin(13),sda=Pin(12),freq=200000)
oled=SSD1306_I2C(128,64,i2c)

def connect():
#Connect to WLAN
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)
  while wlan.isconnected() == False:
  print('Waiting for connection...')
  sleep(1)
  ip = wlan.ifconfig()[0]
  print(f'Connected on {ip}')
  oled.text(f'Connected on {ip}',5,5)
  oled.show()
  return ip

def open_socket(ip):
# Open a socket
  address = (ip, 80)
  connection = socket.socket()
  connection.bind(address)
  connection.listen(1)
  print(connection)
  return connection

def webpage(temperature, mls,fs,hs,nls):
#Template HTML
  html = f"""
  <!DOCTYPE html>
  <html>
  <body style="background-color: #ccffff; text-align: center">
  <h1 style="background-color: #8efffc; top: 100px">
  SMART HOME AUTOMATION USING RASPBERRY PI PICO W
  </h1>
  <div
  style="
  position: absolute;
  background-color: #8efffc;
  width: 200px;
  height: 150px;
  left: 250px;
  top: 100px;
  padding: 10px;
  "
  >
  <h3>MAIN LIGHT</h3>
  <form action="./mlon">
  <input
  type="submit"
  value="ON "
  style="
  32
  position: absolute;
  background-color: #0a6e0d;
  color: #ffffff;
  left: 58px;
  top: 75px;
  "
  />
  </form>
  <form action="./mloff">
  <input
  type="submit"
  value="OFF "
  style="
  position: absolute;
  background-color: #0a6e0d;
  color: #ffffff;
  left: 130px;
  top: 75px;
  "
  />
  </form>
  <p style="position: absolute; left: 35px; top: 110px">
  MAIN LIGHT is {mls}
  </p>
  </div>
  <div
  style="
  position: absolute;
  background-color: #8efffc;
  width: 200px;
  height: 150px;
  left: 550px;
  33
  top: 100px;
  padding: 10px;
  "
  >
  <h3>FAN</h3>
  <form action="./fon">
  <input
  type="submit"
  value="ON "
  style="
  position: absolute;
  background-color: #0a6e0d;
  color: #ffffff;
  left: 58px;
  top: 75px;
  "
  />
  </form>
  <form action="./foff">
  <input
  type="submit"
  value="OFF"
  style="
  position: absolute;
  background-color: #0a6e0d;
  color: #ffffff;
  left: 130px;
  top: 75px;
  "
  />
  </form>
  <p style="position: absolute; left: 75px; top: 110px">FAN is {fs}</p>
  34
  </div>
  <div
  style="
  position: absolute;
  background-color: #8efffc;
  width: 200px;
  height: 150px;
  left: 250px;
  top: 300px;
  padding: 10px;
  "
  >
  <h3>HEATER</h3>
  <form action="./hon">
  <input
  type="submit"
  value="ON "
  style="
  position: absolute;
  background-color: #0a6e0d;
  color: #ffffff;
  left: 58px;
  top: 75px;
  "
  />
  </form>
  <form action="./hoff">
  <input
  type="submit"
  value="OFF"
  style="
  position: absolute;
  35
  background-color: #0a6e0d;
  color: #ffffff;
  left: 130px;
  top: 75px;
  "
  />
  </form>
  <p style="position: absolute; left: 60px; top: 110px">HEATER is {hs}</p>
  </div>
  <div
  style="
  position: absolute;
  background-color: #8efffc;
  width: 200px;
  height: 150px;
  left: 550px;
  top: 300px;
  padding: 10px;
  "
  >
  <h3>NIGHT LAMP</h3>
  <form action="./nlon">
  <input
  type="submit"
  value="ON "
  style="
  position: absolute;
  background-color: #0a6e0d;
  color: #ffffff;
  left: 58px;
  top: 75px;
  "
  36
  />
  </form>
  <form action="./nloff">
  <input
  type="submit"
  value="OFF"
  style="
  position: absolute;
  background-color: #0a6e0d;
  color: #ffffff;
  left: 130px;
  top: 75px;
  "
  />
  </form>
  <p style="position: absolute; left: 35px; top: 110px">
  NIGHT LAMP is {nls}
  </p>
  </div>
  <p
  style="
  position: absolute;
  background-color: #8efffc;
  width: 300px;
  height: 40px;
  left: 350px;
  top: 500px;
  padding: 10px;
  "
  >
  Temperature is {temperature}
  37
  </p>
  </body>
  </html>
  """
  return str(html)
def serve(connection):
#Start a web server
  hs=mls=fs=nls= 'OFF'
  ml=Pin(5,Pin.OUT)
  fan=Pin(4,Pin.OUT)
  heater=Pin(3,Pin.OUT)
  lamp=Pin(2,Pin.OUT)
  ml.value(1)
  fan.value(1)
  heater.value(1)
  lamp.value(1)
  temperature = 0
  while True:
    client = connection.accept()[0]
    request = client.recv(1024)
    request = str(request)
    try:
      request = request.split()[1]
    except IndexError:
      pass
    if request == '/mlon?':
      ml.value(0)
      mls = 'ON'
      oled.fill(0)
      oled.text("Main Light is ON.",5,15)
      oled.show()
    elif request =='/mloff?':
      ml.value(1)
      mls= 'OFF'
      oled.fill(0)
      oled.text("Main Light is OFF.",5,25)
      oled.show()
    if request == '/fon?':
      fan.value(0)
      fs = 'ON'
      oled.fill(0)
      oled.text("Fan is ON.",5,35)
      oled.show()
    elif request =='/foff?':
      fan.value(1)
      fs= 'OFF'
      oled.fill(0)
      oled.text("Fan is OFF.",5,45)
      oled.show()
    if request == '/hon?':
      heater.value(0)
      hs = 'ON'
      oled.fill(0)
      oled.text("Heater is ON.",5,55)
      oled.show()
    
    elif request =='/hoff?':
      heater.value(1)
      hs= 'OFF'
      oled.fill(0)
      oled.text("Heater is OFF.",5,65)
      oled.show()
    if request == '/nlon?':
      lamp.value(0)
      nls = 'ON'
      oled.fill(0)
      oled.text("Night Lamp is ON.",5,75)
      oled.show()
    elif request =='/nloff?':
      lamp.value(1)
      nls= 'OFF'
      oled.fill(0)
      oled.text("Night Lamp is ON.",5,85)
      oled.show()
      temperature = pico_temp_sensor.temp
      html = webpage(temperature, mls,fs,hs,nls)
      client.send(html)
      client.close()
  try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
  except KeyboardInterrupt:
    machine.reset()  
