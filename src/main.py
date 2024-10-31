import network
import socket
from machine import Pin

# Configure LEDs
led1 = Pin(2, Pin.OUT)  # Change pin number as needed
led2 = Pin(4, Pin.OUT)  # Change pin number as needed

# Connect to Wi-Fi
ssid = 'your_SSID'
password = 'your_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi:', wlan.ifconfig())

# HTML content for LED Control
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <title>LightyHub - ODOT!</title>
    <style> 
        .card {{ margin: 20px auto; width: 90%; max-width: 300px; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <a class="navbar-brand" href="#">
            <img src="#" alt="Logo"> LightyHub
        </a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item"><a class="nav-link" href="#">Home</a></li>
            </ul>
        </div>
    </nav>
    <div class="container text-center">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">LIGHTYHUB</h5>
                <h6>LED 1</h6>
                <form action="/led1" method="POST">
                    <button type="submit" name="state" value="on" class="btn btn-success">Turn ON</button>
                    <button type="submit" name="state" value="off" class="btn btn-danger">Turn OFF</button>
                </form>
                <h6>LED 2</h6>
                <form action="/led2" method="POST">
                    <button type="submit" name="state" value="on" class="btn btn-success">Turn ON</button>
                    <button type="submit" name="state" value="off" class="btn btn-danger">Turn OFF</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Socket setup
addr = socket.getaddrinfo('0.0.0.0', 80)[0]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('Request:', request)

    if '/led1' in request:
        if 'state=on' in request:
            led1.on()
        elif 'state=off' in request:
            led1.off()
    elif '/led2' in request:
        if 'state=on' in request:
            led2.on()
        elif 'state=off' in request:
            led2.off()

    # Send the HTML response
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(html)
    cl.close()