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

def connect_http(URI, path, port_8000 = False) -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #FOR TESTING IGNORE
    if port_8000:
        try:
            client_socket.connect((URI, 8000))

        except Exception as e:
            print(f"Provided URL: \"{URI}\" is invalid")
            print("Try again")
            print("IN: connect_http")
            return

    else:
        try:
            client_socket.connect((URI, HTTP_PORT))

        except Exception as e:
            print(f"Provided URL: \"{URI}\" is invalid")
            print("Try again")
            print("IN: connect_http")
            return

    request = f"HEAD /{path} HTTP/1.1\r\n"
    request += f"Host:{URI}\r\n" 
    request += f"Connection: keep-alive\r\n"
    request += f"Upgrade: h2c\r\n"
    request += f"Connection: keep-alive\r\n"
    request += f"Accept: */*\r\n"
    request += f"\r\n"
 
    client_socket.sendall(request.encode('utf-8'))
    response = client_socket.recv(10000).decode('utf-8')
    
    response_check(response, URI, port_8000)



def get_h2_allowed(URI, port_8000 = False) -> bool:
    context = ssl.create_default_context()
    context.set_alpn_protocols(['h2', 'http/1.1'])
    client_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=URI)

    
    if port_8000:
        try:
            client_socket.connect((URI, 8000))

        except Exception as e:
            print(f"Provided URL: \"{URI}\" is invalid")
            print("Try again")
            return

    else:
        try:
            client_socket.connect((URI, HTTPS_PORT))

        except Exception as e:
            print(f"Provided URL: \"{URI}\" is invalid")
            print("Try again")
            print("IN: get_h2_allowed")
            return

    selected = client_socket.selected_alpn_protocol()

    return client_socket.selected_alpn_protocol() == 'h2'




#if needed connect via HTTPS
def connect_https(URI, path, port_8000 = False) -> None: 
    print("HOST", URI)
    print("PATH", path)
    context = ssl.create_default_context()
    context.set_alpn_protocols(['http/1.1'])
    
    client_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=URI)
    
    if port_8000:
        try:
            client_socket.connect((URI, 8000))

        except Exception as e:
            print(f"Provided URL: \"{URI}\" is invalid")
            print("Try again")
            print("IN: connect_http")
            return

    else:
        try:
            client_socket.connect((URI, HTTPS_PORT))

        except Exception as e:
            print(f"Provided URL: \"{URI}\" is invalid")
            print("Try again")
            print("IN: connect_https")
            return

    request = f"HEAD /{path} HTTP/1.1\r\n" 
    request += f"Host: {URI}\r\n"
    request += f"Connection: keep-alive\r\n"
    request += f"Accept: */*\r\n"
    request += f"\r\n"
    
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(5000)
    response = response.decode('utf-8', errors='replace')
    print(response)
    response_check(response, URI, port_8000)
   
def get_location(response) -> tuple:
    pattern = re.compile('Location: http.+/', re.IGNORECASE)
    new_uri = re.findall(pattern, response)
    content_tuple = parse_uri(new_uri[0])
    new_uri = content_tuple[0]
    new_uri = new_uri[18:]
    path = content_tuple[1][1:]
    path = get_path(response, new_uri)
    return (new_uri, path)

def get_path(response,new_uri) -> str:
    path = ''
    pattern = re.compile('Location: http.+', re.IGNORECASE)
    new_uri = re.findall(pattern, response)
    new_uri = new_uri[0].split('/')
   
    while '.ca' not in new_uri[0] and '.com' not in new_uri[0]:
        new_uri.pop(0)
    new_uri.pop(0)

 
    for index, item in enumerate(new_uri):
        if index != len(new_uri)-1:
            path += item.strip()+"/"

        elif item.strip() == "":
            path += item.strip()+"/"
        else:
            path += item.strip()
    
    if path == '/':
        path = ''
    if len(path) > 1:
        if path[-1] == '/' and path[-2] == '/':
            path = path[:-1]

    return path


def print_body_header(body, headers) -> None:
    print("HEADERS")
    print("----------------------------")
    print(headers)
    print("----------------------------")
    print("BODY")
    print("----------------------------")
    print(body)



def get_cookies(headers) -> list:
    pattern = re.compile('Set-Cookie:.+;', re.IGNORECASE)
    cookies_temp_list = re.findall(pattern, headers)
    cookie_names = []
    for index, cookie in enumerate(cookies_temp_list):
        cookies_temp_list[index] = cookie.split("=")
        cookie_names.append((cookies_temp_list[index][0])[11:])
    return cookie_names


def parse_uri(URI) -> tuple:
    path = ""
    
    for char in range(len(URI)):
        if (URI[char] == '.' and (char+1 < len(URI))):
            
            if URI[char+1] == 'c' and (char+2 < len(URI)):
                
                if URI[char+2] == 'o' and (char+3 < len(URI)):
                    if URI[char+3] == 'm':
                        if char+4 < len(URI):
                            path = URI[char+4:]
                            URI = URI[:char+4]
                            return (URI, path)
                        else:
                            return (URI, path)
                elif URI[char+2] == 'a':
                    if char+3 < len(URI):

                        path = URI[char+3:]
                        URI = URI[:char+3]
                        return (URI, path)
                    else:
                        return (URI, path)


def response_check(response, location, port_8000) -> None:
    
    if ('301 Moved Permanently' in response) or ('302 Moved Temporarily' in response) or ('308 Permanent Redirect' in response) or ('302 Found' in response) or ('303 See Other' in response):
        location = get_location(response)
        path = location[1]
        location = location[0]
        if ("Location: https" in response) or ("location: https" in response):
            connect_https(location, path, port_8000)
            
        else:
            connect_http(location, path, port_8000)

    elif ('400 Bad Request' in response):
        print("Error 400 Bad Request --invalid URL")
        return 
        
    elif ('404 Not Found' in response):
        print("Error: 404 Not Found --invalid URL")
        return 

    elif ('HTTP2' in response) or ('http2' in response):
        print(f"website: {URI}")
        print("supports http2 yes")
        return 
    
    elif('405 Method Not Allowed' in response):
        connect_https(URI, port_8000)

    elif ('200 OK' in response):
        
        h2_resp = 'no'
        if get_h2_allowed(location, port_8000) == True:
            h2_resp = 'yes'
        
        print(f"supports http2 {h2_resp}")
        print("List of Cookies:")
        cookies_list = get_cookies(response)
        for cookie in cookies_list:
            print(f"cookie name:{cookie}")
        print("Password-protected: no")

    elif ('403 403' in response) or ('403 Forbidden' in response) or ('401 401' in response) or ('401 Unauthorized' in response):
        h2_resp = 'no'
        if get_h2_allowed(location, port_8000) == True:
            h2_resp = 'yes'
        
        print(f"supports http2 {h2_resp}")
        print("List of Cookies:")
        cookies_list = get_cookies(response)
        for cookie in cookies_list:
            print(f"cookie name:{cookie}")
        print("Password-protected: yes")
        return
    

content_tuple = parse_uri(URI)

connect_http(content_tuple[0], content_tuple[1])

#for testing:
#connect_http('localhost', "", True)