from vfd import VFD

vfd = VFD(17, 27)
vfd.open('/dev/ttyAMA0')
vfd.clr()
vfd.close()
vfd.reset()
