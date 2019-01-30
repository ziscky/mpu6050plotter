import plotly.plotly as py
import plotly.graph_objs as go
import socket
import sys
import json


##OBTAIN FROM PLOT.LY
uname =   ""
api_key = ""

#NodeMCU address
addr = ""
port = 80

#Number of data samples to take
nsamples = 200

#average message length
buff_size = 256


def recvall(sock,nsample):
    arr = []
    for i in range(nsample):
        part = sock.recv(buff_size)

        #extract JSON message from HTTP content and add to list
        partstr = str(part)
        ob = partstr.find('{')
        print(partstr[ob:].strip())
        try:
            obj = json.loads(partstr[ob:].strip())
            arr.append(obj)
        except:
            continue

    return arr


def getTrace(x,y,name,color):
    return  go.Scatter(
        x = x,
        y = y,
        mode = 'lines',
        name = name,
        line=dict(
            color=color
        )
    )

#sign in to plot.ly
py.sign_in(uname,api_key)

#create raw tcp socket connection to server
sock = socket.create_connection((addr,port))
data = recvall(sock,nsamples)


#x-axis -> no. of samples
x = range(0,nsamples)

#y-axis -> accelerometer data
yax = []
yay = []
yaz = []

#y-axis -> gyroscope data
ygx = []
ygy = []
ygz = []

for result in data:
    yax.append(result["ax"])
    yay.append(result["ay"])
    yaz.append(result["az"])
    ygx.append(result["gx"])
    ygy.append(result["gy"])
    ygz.append(result["gz"])


a_xtrace = getTrace(x,yax,"Accelerometer - X","black")
a_ytrace = getTrace(x,yay,"Accelerometer - Y","green")
a_ztrace = getTrace(x,yaz,"Accelerometer - Z","blue")
g_xtrace = getTrace(x,ygx,"Gyroscope - X","red")
g_ytrace = getTrace(x,ygy,"Gyroscope - Y","yellow")
g_ztrace = getTrace(x,ygz,"Gyroscope - Z","orange")


#AccelX Vs GyroX
data = [a_xtrace,g_xtrace]
py.plot(data,filename="MPU6050 - X")

#AccelerometerY Vs GyroY
data = [a_ytrace,g_ytrace]
py.plot(data,filename="MPU6050 - Y")

#AccelerometerZ Vs GyroscopeZ
data = [a_ztrace,g_ztrace]
py.plot(data,filename="MPU6050 - Z")
    
#combined
data = [a_xtrace,g_xtrace,a_ytrace,g_ytrace,a_ztrace,g_ztrace]
py.plot(data,filename="MPU6050 - XYZ")
