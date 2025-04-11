import sys
import struct
from struct import *
from packet import *

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

                elif type_of_message in [3, 11]:  # ICMP Error message (type 3 or 11)
                    if len(icmp_header) >= 32:  # Check if the ICMP error message contains quoted UDP data
                        
                        quoted_udp = icmp_header[28:36]  # Extract UDP header (usually 8 bytes after IP header)
                        icmp_src_port, icmp_dest_port = struct.unpack('!HH', quoted_udp[:4])
                        # Linux-like error message with UDP ports
                        current_application_header = ApplicationHeader(protocol, code, icmp_src_port, icmp_dest_port, None, type_of_message, None)
                        # Store in a Linux-specific ICMP list
                        current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                        error_ICMP_linux.append(current_packet)
                    else:
                        windows = True
                    # Windows-like error message without UDP info
                        current_application_header = ApplicationHeader(protocol, code, None, None, None, type_of_message, None)
                    # Store in a Windows-specific ICMP list
                        current_packet = Packet(current_packet_header, current_ethernet_header, current_IP_header, current_application_header)
                        error_ICMP_windows.append(current_packet)

            packet_list.append(current_packet)

        
        #check if cap file is in linux or windows.
        #if windows:
           # print(len(error_ICMP) + len(echo_ICMP))
            #print(len(ping_ICMP))
        if not windows:
            grouped_ICMP_UDP_list = group_ICMP_UDP_linux(UDP_list, error_ICMP_linux)


def group_ICMP_UDP_linux(UDP_list, ICMP_list):
    print(len(UDP_list))
    print(len(ICMP_list))
    grouped_ICMP_UDP_list = []
    for icmp in ICMP_list:
        for udp in UDP_list:
            if udp.application_header.src_port == icmp.application_header.src_port:
                grouped_ICMP_UDP_list.append((udp,icmp))
    print(len(grouped_ICMP_UDP_list))
    #for item in grouped_ICMP_UDP_list:
        #print("elfkefjslkj")
        #print(len(item))
  

file_name = sys.argv[1]
read_cap(file_name)