import sys
from PIL import Image
from PIL import ImageOps
from vfd import VFD

def vfdimg(filename):
  img = Image.open(filename)
  img = ImageOps.grayscale(img)
  size = img.size
  table = []
  for x in range(0, size[0]):
    line = []
    dat = 0
    cnt = 0
    for y in range(0, size[1]):
      p = img.getpixel((x, y))
      dat = dat << 1
      if p == 0:
        dat += 1
      cnt += 1
      if cnt >= 8:
        line.append(dat)
        dat = 0
        cnt = 0
    if cnt > 0:
      while cnt < 8:
        dat = dat << 1
        cnt += 1
      line.append(dat)
    table.append(line)
  return table

if __name__ == '__main__':
  vfd = VFD(17, 27)
  vfd.open('/dev/ttyAMA0')
  img = vfdimg(sys.argv[1])
  vfd.drawimg(img)
  vfd.close()
