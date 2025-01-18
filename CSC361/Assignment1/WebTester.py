import sys
import socket
import ssl
import re

HTTP_PORT = 80
HTTPS_PORT = 443

if (len(sys.argv) != 2):
    print("Error: Ensure you pass exactly one argument in the command line.")
    sys.exit("Leaving program.")

URI = sys.argv[1]

#first attempt to connect via HTTP
def connect_http(URI, port = HTTP_PORT):

    '''
    -HTTP specifically relies on using TCP in the transport layer.
    So use TCP for our socket.

    -AF_NET specifies that we want to use internet protocol version 4
    an IPv4 address is a 32 bit number, typically written as 4 number seperated by dots
    (if we wanted we could use version 6: IPv6)

    -SOCK_STREAM specifies that we want to use TCP. (we could also use UDP)
    But of course not for HTTP.
    '''
  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   

    '''
    80 is the port number for HTTP
    443 for HTTPS
    '''

    client_socket.connect((URI, HTTP_PORT))
    
    '''
    Check if the server support http2.
    Use OPTIONS HTTP method to check
    '''

    request = f"OPTIONS / HTTP/1.1\r\n"
    request += f"Host:{URI}\r\n"
    request += f"Connection: keep-alive\r\n"
    request += f"Upgrade: h2c\r\n"
    request += f"Accept: */*\r\n"
    request += f"\r\n"

    '''
    utf-8 is encoding our string into bytes so it can be trasferred over networks
    '''

    client_socket.send(request.encode('utf-8'))

    '''
    The value passed in recv is maximum quantity of bytes of data we wish to receive
    (the buffer)
    '''

    response = client_socket.recv(10000).decode('utf-8')
    if ('301' in response) or ('302' in response):
        if "Location: https" in response:
            check_http2(get_location(response))

    print(response)


#if needed connect via HTTPS
def check_http2(URI): 
    context = ssl.create_default_context()
    context.set_alpn_protocols(['h2','http/1.1'])
    client_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=URI)
    client_socket.connect((URI, HTTPS_PORT))
    request = f"OPTIONS / HTTP/1.1\r\n"
    request += f"Host:{URI}\r\n"
    request += f"Connection: keep-alive\r\n"
    request += f"Upgrade: h2c\r\n"
    request += f"Accept: */*\r\n"
    request += f"\r\n"
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(10000).decode('utf-8')
    print(response)


    #negotiated_protocol = client_socket.selected_alpn_protocol()
    #print(negotiated_protocol)


def get_location(response):
    pattern = 'Location: http.+/'
    new_uri = re.findall(pattern, response)
    new_uri = new_uri[0] 
    new_uri = new_uri[18:-1]
    return (new_uri)

connect_http(URI)