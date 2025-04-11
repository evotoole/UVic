class Packet:
    def __init__(self, PacketHeader, ethernet_header, IPHeader, ApplicationHeader):

        self.ethernet_header = ethernet_header
        self.packet_header = PacketHeader
        self.IPHeader = IPHeader
        self.application_header = ApplicationHeader
        pass

class PacketHeader:
    def __init__(self, ts_sec, ts_usec, incl_len, orig_len):
        self.ts_sec = ts_sec
        self.ts_usec = ts_usec
        self.incl_len = incl_len
        self.orig_len = orig_len

class ApplicationHeader:
    def __init__(self, protocol, code, src_port = None, dest_port = None, length = None, type_of_message = None, sequence_number = None):
        self.type_of_message = type_of_message
        self.protocol = protocol
        self.code = code
        self.src_port = src_port
        self.dest_port = dest_port
        self.length = length
        self.sequence_number = sequence_number
        

class IPHeader:
    def __init__(self, version_and_ihl, tos, total_length, identification, flags_and_offset, ttl, protocol, checksum, src_ip, dest_ip):
        self.version_and_ihl = version_and_ihl 
        self.tos = tos 
        self.total_length = total_length 
        self.identification = identification
        self.flags_and_offset  = flags_and_offset
        self.ttl = ttl
        self.protocol = protocol 
        self.checksum = checksum
        self.src_ip = src_ip
        self.dest_ip = dest_ip

class EthernetHeader:
    def __init__(self, dest_mac, src_mac, ethertype):
        self.dest_mac = dest_mac
        self.src_mac = src_mac
        self.ethertype = ethertype

class GlobalHeader:
    def __init__(self):
        pass