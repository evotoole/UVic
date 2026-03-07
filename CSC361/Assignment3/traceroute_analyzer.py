import sys
import struct
from struct import *
from packet import *
import socket
import statistics

#TODO make sure this works for both windows and linux cap files.
#reads through the cap file, splitting up packets
def read_cap(file_name):
    with open(file_name, 'rb') as file:
        global_header_data = file.read(24) #read the first 24 bytes of data = global header

        windows = False #check if windows file
        if 'win' in file_name:
            windows = True
            


        UDP_list = [] #used in linux cap files
        ping_ICMP = [] #used in winows cap files
        error_ICMP_linux = []
        error_ICMP_windows = []
        echo_ICMP = [] 

        packet_list = [] #list of packets with all fields in the packets.

        fragments = {}
        while(1):
            packet_header_data = file.read(16) 
            if packet_header_data == b'':
                break
            
            #unpack the packet header.
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('=IIII', packet_header_data)

            #create an instance of the PacketHeader class
            current_packet_header = PacketHeader(ts_sec, ts_usec, incl_len, orig_len)

            #read the entire packet using incl len in the packet header
            packet_data = file.read(current_packet_header.incl_len)

            #read and unpack the ethernet header from the packet data
            ethernet_header_data = packet_data[:14]
            dest_mac, src_mac, ethertype = struct.unpack('!6s6sH', ethernet_header_data)
            current_ethernet_header = EthernetHeader(dest_mac, src_mac, ethertype)

            #read and unpack the IPv4 IP header
            ip_header = packet_data[14:34]
            version_and_ihl, tos, total_length, identification, flags_and_offset, ttl, \
            protocol, checksum, src_ip, dest_ip = struct.unpack('!BBHHHBBH4s4s', ip_header)
            current_IP_header = IPHeader(version_and_ihl, tos, total_length, identification, flags_and_offset, ttl, protocol, checksum, src_ip, dest_ip)
            
            #print(current_IP_header.protocol)
            #check if the protocol used is ICMP or UDP. else continue to next packet
            if (current_IP_header.protocol != 1 and current_IP_header.protocol != 17):
                continue

            application_data = None
            #create UDP and ICMP lists for identifying corresponding packets
            
            MF_FLAG = 0x2000
            FRAG_OFFSET_MASK = 0x1FFF

            # Is the packet fragmented?
            is_fragment = (flags_and_offset & MF_FLAG) != 0 or (flags_and_offset & FRAG_OFFSET_MASK) != 0
            

            if current_IP_header.protocol == 17:  # UDP and not windows
                
                # Extract the UDP header and data (UDP header is 8 bytes)
                protocol = 'UDP'
                udp_header_data = packet_data[34:42]  # UDP header starts after IP header
                src_port, dest_port, length, checksum = struct.unpack('!HHHH', udp_header_data)
                if src_port == 53 or dest_port == 53:
                    continue 
                if src_port == 123 or dest_port == 123:  # NTP uses port 123
                    continue
                current_application_header = ApplicationHeader(protocol, None, src_port, dest_port, length, None)
                current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                UDP_list.append(current_packet)
                
             
                #print(current_packet.application_header.src_port)

            elif current_IP_header.protocol == 1:  # ICMP 
                protocol = 'ICMP'
                icmp_header = packet_data[34:]  # ICMP header starts after IP header
                type_of_message, code, checksum = struct.unpack('!BBH', icmp_header[:4])
                current_packet = None

                if type_of_message == 8:  # Echo Request
                    sequence_number = struct.unpack('!H', icmp_header[6:8])[0]
                    current_application_header = ApplicationHeader(protocol, code, None, None, None, type_of_message, sequence_number)
                    current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                    ping_ICMP.append(current_packet)

                elif type_of_message == 0:  # Echo Reply
                    sequence_number = struct.unpack('!H', icmp_header[6:8])[0]
                    current_application_header = ApplicationHeader(protocol, code, None, None, None, type_of_message, sequence_number)
                    current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                    echo_ICMP.append(current_packet)


                elif type_of_message in [3, 11]:  # ICMP Error message (Type 3 or 11)
                    sequence_number = None  # Default
                    
                    # Check if there is enough length in the ICMP header
                    if len(icmp_header) >= 36:
                        # Quoted IP header starts at byte 8
                        quoted_ip_header = icmp_header[8:28]  # 20 bytes
                        
                        quoted_protocol = quoted_ip_header[9]  # Protocol byte of the quoted IP header
                        identification = struct.unpack("!H", quoted_ip_header[4:6])[0]  # Identification of the quoted packet
                        
                        # If the quoted packet is ICMP (ping)
                        if quoted_protocol == 1:  # ICMP
                            quoted_icmp_header = icmp_header[28:36]  # ICMP header starts after quoted IP header
                            if len(quoted_icmp_header) >= 8:
                                sequence_number = struct.unpack("!H", quoted_icmp_header[6:8])[0]
                            
                            # Handle the case where this is a ping error
                            current_application_header = ApplicationHeader(protocol, code, None, None, None, type_of_message, sequence_number, identification)
                            current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                            error_ICMP_linux.append(current_packet)

                        # If the quoted packet is UDP (in case of fragmented UDP causing an error)
                        elif quoted_protocol == 17:  # UDP
                            quoted_udp_header = icmp_header[28:36]  # Extract UDP header from quoted packet
                            icmp_src_port, icmp_dest_port = struct.unpack('!HH', quoted_udp_header[:4])

                            # Handle the UDP case (e.g., ICMP error related to UDP fragment)
                            current_application_header = ApplicationHeader(protocol, code, icmp_src_port, icmp_dest_port, None, type_of_message, sequence_number, identification)
                            current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                            error_ICMP_linux.append(current_packet)

                    else:
                        # If the ICMP error doesn't have enough data for the quoted header, handle accordingly.
                        current_application_header = ApplicationHeader(protocol, code, None, None, None, type_of_message, sequence_number)
                        current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                        error_ICMP_linux.append(current_packet)




            if is_fragment:
                if current_IP_header.identification not in fragments:
                    fragments[current_IP_header.identification] = [] 
                fragments[current_IP_header.identification].append(current_packet)

            packet_list.append(current_packet)

        
        #check if cap file is in linux or windows.
        #if windows:
           # print(len(error_ICMP) + len(echo_ICMP))
            #print(len(ping_ICMP))
        if len(ping_ICMP) > 0:
            windows = True

   
        if not windows:
            grouped_ICMP_list_linux = group_ICMP_UDP_linux(UDP_list, error_ICMP_linux)
            grouped_ICMP_list_linux = sort_by_TTL(grouped_ICMP_list_linux)
            list_linux_IPs(grouped_ICMP_list_linux)
     
            if len(fragments) == 0:
                print("The number of fragments created from the original datagram is: 0\n")
                print("The offset of the last fragment is 0")
           # else:
                

            it = 0
            sum = 0
            for id, fragment in fragments.items():
                if it >  0:
                    break
                print(f"the number of fragements created is {len(fragment)}")
                for frag in fragment:
                    mf_flag = (frag.IPHeader.flags_and_offset & 0x2000) >> 13  # MF bit (bit 13)
                    fragment_offset = frag.IPHeader.flags_and_offset & 0x1FFF  # lower 13 bits (in 8-byte blocks)
                    fragment_offset_bytes = fragment_offset * 8
                    if mf_flag == 0:
                        print(f"The offset of the last fragment is: {fragment_offset_bytes}")
                        break
                    it+= 1
                    
                
        
            #calculate_RTT(fragments, error_ICMP_linux, UDP_list, grouped_ICMP_list_linux, UDP_list[0].IPHeader.src_ip)

        else:
            grouped_ICMP_list_windows = group_ICMP_UDP_windows(error_ICMP_linux, ping_ICMP, echo_ICMP)
            list_window_IPs(UDP_list, error_ICMP_linux, echo_ICMP, ping_ICMP, grouped_ICMP_list_windows)
            print("The number of fragments created from the original datagram is: 0\n")
            print("The offset of the last fragment is 0")







def sort_by_TTL(grouped_ICMP_list_linux):
    
    if grouped_ICMP_list_linux is None:
        return []

    sorted_list = []
    while len(grouped_ICMP_list_linux) != 0:
        cur_min = 999999
        min_tup = None
        for tup in grouped_ICMP_list_linux:
            if tup[0].IPHeader.ttl < cur_min:
                min_tup = tup
                cur_min = tup[0].IPHeader.ttl
        if min_tup:
            grouped_ICMP_list_linux.remove(min_tup)
            sorted_list.append(min_tup)
    return sorted_list
        

def group_ICMP_UDP_linux(UDP_list, ICMP_list):
    added = []
    
    grouped_ICMP_UDP_list = []
    for udp in UDP_list:
        found = False
        for icmp in ICMP_list:
            if udp.application_header.src_port == icmp.application_header.src_port:         
                grouped_ICMP_UDP_list.append((udp,icmp,udp.application_header.identification))
                found = True
        
    
    
    return grouped_ICMP_UDP_list
   
    
    
def group_ICMP_UDP_windows(error_ICMP_linux, ping_ICMP, echo_ICMP):
    grouped_ICMP_UDP_list = []
    for icmp_error in error_ICMP_linux:
        error_seq = icmp_error.application_header.sequence_number

        if error_seq is None:
            continue  # Can't match without sequence number
    
        for ping in ping_ICMP: 
            if ping.application_header.sequence_number == error_seq:
                grouped_ICMP_UDP_list.append((ping, icmp_error))
                break  # Match found
            
    #print(f"Grouped Windows ICMP (via sequence numbers): {len(grouped_ICMP_UDP_list)}")
    return grouped_ICMP_UDP_list

    
def list_linux_IPs(grouped_UDP_icmp_list):
    sources = set()
    ultimate_dests = set()
    intermediates = []
    for tup in grouped_UDP_icmp_list:
        sources.add(socket.inet_ntoa(tup[0].IPHeader.src_ip))
        ultimate_dests.add(socket.inet_ntoa(tup[0].IPHeader.dest_ip))
        
    for tup in grouped_UDP_icmp_list:
        if (socket.inet_ntoa(tup[1].IPHeader.src_ip) not in (intermediates)) \
            and (socket.inet_ntoa(tup[1].IPHeader.src_ip) not in (sources))\
            and (socket.inet_ntoa(tup[1].IPHeader.src_ip) not in (ultimate_dests)):

            intermediates.append(socket.inet_ntoa(tup[1].IPHeader.src_ip))

    
    
    source = next(iter(sources))
    ult_dest = next(iter(ultimate_dests))
    print("The IP address of the source node is: ", source)
    print("The IP address of the ultimate destination node is: ", ult_dest)
    print("The IP addresses of the intermediate destination nodes:")
    for index, ip in enumerate(intermediates):
        print(f"router {index+1}: {ip}")
    print("\nThe values in the protocol field of IP headers:")
    print("1: ICMP")
    print("17: UDP")

    
def list_window_IPs(UDP_list, error_ICMP_linux, echo_ICMP, ping_icmp, grouped_icmp):
    sources = set()
    ultimate_dests = set()
    intermediates = set()
   
    for ping in ping_icmp:
        sources.add(socket.inet_ntoa(ping.IPHeader.src_ip))
        ultimate_dests.add(socket.inet_ntoa(ping.IPHeader.dest_ip))

    error_ICMP_linux = sort_errors_TTL(grouped_icmp)

    for item in error_ICMP_linux:
        if (socket.inet_ntoa(item.IPHeader.src_ip) not in sources) and (socket.inet_ntoa(item.IPHeader.src_ip) not in intermediates):
            intermediates.add(socket.inet_ntoa(item.IPHeader.src_ip))
    
    for item in sources:
        print(f"The IP address of the source node: {item}")
    for item in ultimate_dests:
        print(f"The IP address of the ultimate destination node: {item}")
    print("The IP addresses of the intermediate destination nodes:")
    for index, ip in enumerate(intermediates):
        print(f"router {index+1}: {ip}")
    print("\nThe values in the protocol field of IP headers:")
    print("1: ICMP")
    
    

    
def sort_errors_TTL(grouped_icmp):
    min_TTL = 99999
    sorted = []

    while len(grouped_icmp) != 0:
        for error in grouped_icmp:
            if error[0].IPHeader.ttl < min_TTL:
                min = error
                min_TTL = error[0].IPHeader.ttl


        min_TTL = 99999
        grouped_icmp.remove(min)
        sorted.append(min[1])
    

    return sorted

    

file_name = sys.argv[1]
read_cap(file_name)