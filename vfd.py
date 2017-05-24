import time
import wiringpi as wpi
import sys

class VFD:
  def __init__(self, resetPin, busyPin):
    self.serial = None
    self.resetPin = resetPin
    self.busyPin = busyPin
  def waitbusy(self):    
    while wpi.digitalRead(self.busyPin) == wpi.GPIO.HIGH:
      time.sleep(0.001)
  def putc(self, c):
    self.waitbusy()
    wpi.serialPutchar(self.serial, c)
  def puts(self, s):
    for c in s:
      self.putc(ord(c))
  def fontxy(self, x, y):
    self.putc(0x1f)
    self.putc(0x28)
    self.putc(0x67)
    self.putc(0x40)
    self.putc(x)
    self.putc(y)
  def fontwide(self, w):
    # 0: fixed width (right 1 dot space)
    # 1: fixed width (both side 1 dot space)
    # 2: propotional (right 1 dot space)
    # 3: propotional (both side 1 dot space)
    self.putc(0x1f)
    self.putc(0x28)
    self.putc(0x67)
    self.putc(0x03)
    self.putc(w)
  def scrhon(self, n): #n: speed
    self.putc(0x1f)
    self.putc(0x03)
    self.putc(0x1f)
    self.putc(0x73)
    self.putc(n)
  def scroff(self):
    self.putc(0x1f)
    self.putc(0x01)
  def scroll(self, w, c, s):
    # w: width(byte)
    # c: count
    # s: speed (x14msec)
    self.putc(0x1f)
    self.putc(0x28)
    self.putc(0x61)
    self.putc(0x10)
    self.putc(w & 0xff)
    self.putc(w >> 8)
    self.putc(c & 0xff)
    self.putc(c >> 8)
    self.putc(s)
  def scrollandwait(self, w, c, s):
    self.scroll(w, c, s)
    time.sleep(0.014 * c * s)
  def reverse(self, n): #n=1: on, 0: off
    self.putc(0x1f)
    self.putc(0x72)
    self.putc(n)
  def wait(t):  # [0.5s]
    self.putc(0x1f)
    self.putc(0x28)
    self.putc(0x61)
    self.putc(0x01)
    self.putc(t)
  def clr(self):
    self.putc(0x0c)
  def crlf(self):
    self.putc(0x0d)
    self.putc(0x0a)
  def home(self):
    self.putc(0x0b)
  def cursor(self, x, y):
    self.putc(0x1f)
    self.putc(0x24)
    self.putc(x & 0xff)
    self.putc(x >> 8)
    self.putc(y & 0xff)
    self.putc(y >> 8)
  def  charcode(self, n): # n=0:USA, 1:KANA, ...
    self.putc(0x1f)
    self.putc(0x74)
    self.put(n)
  def drawimg(self, img):
    self.putc(0x1f)
    self.putc(0x28)
    self.putc(0x66)
    self.putc(0x11)
    x = len(img)
    y = len(img[0])
    self.putc(x & 0xff)
    self.putc(x >> 8)
    self.putc(y & 0xff)
    self.putc(y >> 8)
    self.putc(0x01)
    for line in img:
      for d in line:
        self.putc(d)
  def open(self, serialName):
    wpi.wiringPiSetupGpio()
    wpi.pinMode(self.resetPin, wpi.GPIO.OUTPUT)
    wpi.pinMode(self.busyPin, wpi.GPIO.INPUT)
    wpi.digitalWrite(self.resetPin, wpi.GPIO.LOW)
    time.sleep(0.1)
    wpi.digitalWrite(self.resetPin, wpi.GPIO.HIGH)
    self.serial = wpi.serialOpen(serialName, 38400)
  def close(self):
    wpi.serialClose(self.serial)
  def reset(self):
    wpi.digitalWrite(self.resetPin, wpi.GPIO.LOW)

if __name__ == '__main__':
  vfd = VFD(17, 27)
  vfd.open('/dev/ttyAMA0')
  vfd.puts(sys.argv[1])
  vfd.cursor(100,0)
  img = [
    [0x00, 0x80], [0x20, 0x82], [0x13, 0xe4], [0x04, 0x10],
    [0x08, 0x08], [0x10, 0x04], [0x10, 0x04], [0x70, 0x07],
    [0x10, 0x04], [0x10, 0x04], [0x08, 0x08], [0x04, 0x10],
    [0x13, 0xe4], [0x20, 0x82], [0x00, 0x80], [0x00, 0x00]]
  vfd.drawimg(img)
  vfd.scrollandwait(4, 1024, 1)
  vfd.reset()
  vfd.close()
  
