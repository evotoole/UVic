import sys
import struct
from struct import *
from typing import Dict, List, Tuple, ByteString

#the known formatting of headers that we are dealing with
CAP_HEADER_FORMAT = "IHHiIII"
PACKET_HEADER_FORMAT = "IIII"
ETHERNET_HEADER_FORMAT = "!6s6sH"
IPV4_HEADER_FORMAT = "!BBHHHBBH4s4s"
TCP_HEADER_FORMAT = "!HHLLBBHHH" 
#used to check what endianess the magic number in cap header specifies
BIG_END_MAGIC_NUM = b'\xa1\xb2\xc3\xd4'

#takes a list of dictionaries corresponding to the packets from the cap file
#organizes list dictionary further for easy analysis.
def organize_LD(filename: str) -> List[Dict]:
    LD_packs = read_cap(filename)

    for index in range(1, len(LD_packs)):
        eth_head = struct.unpack(ETHERNET_HEADER_FORMAT, LD_packs[index]['data'][:14])
        #tup format: dest Mac adress, source Mac adress, ether type
    
        
        IPv_len = LD_packs[index]['data'][14]
        IPv_len = IPv_len & 0x0F
        IPv_len = IPv_len * 4
        IPv_head = struct.unpack(IPV4_HEADER_FORMAT, LD_packs[index]['data'][14:14+IPv_len])
        LD_packs[index]['data'] = LD_packs[index]['data'][14+IPv_len:]
        #tup format (example): Version and IHL: 70 Type of Service: 0 Total Length: 60 
        #Identification: 7238 Flags and Fragment Offset: 16384 TTL: 64 Protocol: 6 
        #Checksum: 45862 Source IP: 192.168.0.104 Destination IP

        if IPv_head[6] == 6:
            protocol = "TCP"
        else:
            protocol = "UDP"


        if protocol == "UDP":
            protocol_header = LD_packs[index]['data'][:8]
            payload = LD_packs[index]['data'][8:]

        elif protocol == "TCP":

            offset = (LD_packs[index]['data'][12] >> 4) & 0xF
            offset = offset * 4
    
            protocol_header = struct.unpack(TCP_HEADER_FORMAT, LD_packs[index]['data'][:20])

            #format of TCP tuple: src_port, rec_port, Seq #, ACK #, data offset/flags,
            #flags, window size, checksum, urgent pointer
            payload = LD_packs[index]['data'][offset:]


        LD_packs[index]['eth_head'] = eth_head
        LD_packs[index]['IPv_head'] = IPv_head
        LD_packs[index]['trans_head'] = protocol_header
        LD_packs[index]['payload'] = payload
        del(LD_packs[index]['data'])


    LD_packs = break_up_packs(LD_packs, protocol)

    LD_packs = add_IP(LD_packs)

    LD_packs = add_port(LD_packs)

    tuple_groups, LD_packs = get_tups(LD_packs)

    connection_dict = group_by_tuple(LD_packs, tuple_groups)

    connection_dict = merge_symmetric_tup(connection_dict)
    print(len(connection_dict))

    return LD_packs


#reads through a given cap file and splits/organizes headers, fields, and data, for easy analysis
def read_cap(filename: str) -> List[Dict]:
    pack_list_dict = []
    big_endian = False
    read_as = ''
 
    ph = "init" #set ph to init for while loop condition
    with open(filename, 'rb') as cap_file:
        
        #append the cap file header to the first position in our list of tuples
        cap_head_packed = cap_file.read(24)
        cap_head_unpacked = struct.unpack(CAP_HEADER_FORMAT, cap_head_packed)
        pack_list_dict.append(cap_header_tuple_to_dict(cap_head_unpacked))
    

        #check the endianess given the magic number. on the mac M1 chip, little endian is assumed
        #so if big endian, we must force this. (ie we must correct for big endian)
        if pack_list_dict[0]['magic'] == struct.unpack("<I", BIG_END_MAGIC_NUM)[0]:
            big_endian = True
            read_as = '!'
        
        while ph != b'':
            ph_packed = cap_file.read(16)
            if ph_packed == b'':
                break
                
            #read as specifies whether or not to read as big endian.
            #this makes it so this program works on a mac with and m1 chip for big
            #or little endian magic num.
            ph_unpacked = struct.unpack(read_as + PACKET_HEADER_FORMAT, ph_packed)
    
            pd_packed = cap_file.read(ph_unpacked[2])
            #print(ph_unpacked, pd_packed)
            pack_list_dict.append(pack_header_tuple_to_dict(ph_unpacked, pd_packed))
            
   
    return pack_list_dict

def merge_symmetric_tup(connection_dict):
    to_delete = set()  # Store keys to delete
    marked_dict = dict.fromkeys(connection_dict.keys(), False)

    for element1 in list(connection_dict.keys()):  # Use list() to avoid runtime issues
        for element2 in list(connection_dict.keys()):
            if (element1 != element2) and (
                element1[0] == element2[1] and element1[1] == element2[0]
                and element1[2] == element2[3] and element1[3] == element2[2]):
               
                connection_dict[element1].append(connection_dict[element2])

                if (marked_dict[element2] or marked_dict[element1]) == False:
                    marked_dict[element2] = True
                # Mark for deletion instead of deleting inside loop
     

    for key in marked_dict.keys():
        if marked_dict[key]:
            del connection_dict[key]

    return connection_dict



def add_port(LD_packs):
    for index in range(1, len(LD_packs)):
        LD_packs[index]['src_port'] = LD_packs[index]['trans_head'][0]
        LD_packs[index]['dest_port'] = LD_packs[index]['trans_head'][1]
    return LD_packs

def group_by_tuple(LD_packs, tuple_list):
    connect_dict = dict.fromkeys(tuple_list, [])
    for index in range(1, len(LD_packs)):
        connect_dict[LD_packs[index]['tuple']] = [LD_packs[index]]

    return connect_dict

def get_tups(LD_packs):
    unique_tups = []
    print(len(LD_packs))
    for index in range(1, len(LD_packs)):
        new_tup = (LD_packs[index]['src_port'], LD_packs[index]['dest_port'], LD_packs[index]['src_IP'], LD_packs[index]['dest_IP'])
        LD_packs[index]['tuple'] = new_tup
        if new_tup not in unique_tups:
            unique_tups.append(new_tup)
    return (unique_tups, LD_packs)

def break_up_packs(LD_packs, trans_prot):

    for index in range(1, len(LD_packs)):
        
        if trans_prot == 'TCP':
            LD_packs[index]['offset_reserved_flags'] = LD_packs[index]['trans_head'][5]
            LD_packs[index]['Flag_ACK'] = ((LD_packs[index]['offset_reserved_flags'] >> 4) & 1)
            LD_packs[index]['Flag_SYN'] = ((LD_packs[index]['offset_reserved_flags'] >> 1) & 1)
            LD_packs[index]['Flag_FIN'] = (LD_packs[index]['offset_reserved_flags'] & 1)
            LD_packs[index]['Flag_RST'] = (LD_packs[index]['offset_reserved_flags'] >> 2) & 1
            print(LD_packs[index]['Flag_RST'])
        else:
            # if needed do this for UDP as well. 
            pass

    return LD_packs

def add_IP(LD_packs):
    for index in range(1, len(LD_packs)):
        LD_packs[index]['src_IP'] = LD_packs[index]['IPv_head'][8]
        LD_packs[index]['dest_IP'] = LD_packs[index]['IPv_head'][9]
    return LD_packs

#based on the IPv4 header, returns whether TCP or UDP is used.
def get_protocol(IP_head) -> str:
    sig_bytes = IP_head[9]
    if sig_bytes == 6:
        return 'TCP'
    return 'UDP'

#converts the cap file header to a dict
def cap_header_tuple_to_dict(tup: Tuple) -> Dict[str, Dict]:
    return {'magic':tup[0], 'version_maj':tup[1], 'version_min':tup[2],\
            'thiszone':tup[3], 'sigfigs':tup[4], 'snaplen': tup[5], 'network':tup[6]}

#converts each packet header to a header dictionary to be added to a list.
def pack_header_tuple_to_dict(ph_tup: Tuple, pd_byte: ByteString) -> Dict[str, Dict[str, int] | ByteString]:
    return {'pkt_head':{'ts_sec': ph_tup[0], 'ts_usec': ph_tup[1], 'incl_len': ph_tup[2], 'orig_len': ph_tup[3]},\
            'data': pd_byte}



if len(sys.argv) == 2:
    filename = sys.argv[1]
    organize_LD(filename)
else:
    print('------------------------------------------------------------------')
    print("Invalid commandline input.\nMake sure exactly one file is passed.")
    print('------------------------------------------------------------------')