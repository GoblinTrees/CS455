import serial

print("in loop")
try:
        ser = serial.Serial()
        ser.port = '/dev/ttyUSB0'
        ser.baudrate = 115200
        ser.bytesize = serial.EIGHTBITS
        ser.parity =serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 1
        ser.open()
        time.sleep(1)
        ser.close()
except Exception as e:
        print("ERROR IN FIRST TRY OF GET DISTANCES:",e)
        pass
searching = True
toReturn = {}
while searching:
        try:
                # data looks like this when it first gets here
                # mc 0f 00000663 000005a3 00000512 000004cb  ffffffff ffffffff ffffffff 095f c1 00146fb7 a0:0 22be
                # 0  1  2        3        4        5        6        7        8        9        10   11 12       13   14
                data=ser.readline()
                print(data)
                for i in range(data.length()):
                        print(data[i]
                
        finally:
                print("error")
        