'''
Please read the README first to understand the main logic of the Firewall class.
'''
import ip
import utils
import math

MAX_PORT = 65535
MAX_IP = 255

'''
Firewall class that implements the interface functions defined in the assignment.
Can be initialized as Firewall(file_path)
Can specify custom bin size if needed.
'''
class Firewall:
    '''
    Class attributes which are fixed across all instances of objects.
    As we only have a maximum of two bins for direction and protocol (inbound, outbound) and (TCP, UDP) respectively,
    they are fixed across all objects.
    '''
    no_direction_bins = 2
    no_protocol_bins = 2

    '''
    The constructor defines instance attributes and calling some helper functions to build the data structures necessary.
    '''
    def __init__(self, file_path, no_port_bins=10, no_ip_bins=10):
        self.file_path = file_path
        self.no_port_bins = no_port_bins
        self.no_ip_bins = no_ip_bins
        self.port_ranges = []
        self.ip_ranges = []
        self.port_increments = 0
        self.ip_increments = 0
        self.rules = []

        self.initialize_ranges()
        self.initialize_DS()
        self.read_file()
    
    '''
    initialize_ranges computes the ranges of the different bins for the ports and the IP Addresses.
    The results of these ranges are stored in the lists port_ranges and ip_ranges.
    '''
    def initialize_ranges(self):
        # Computes the length of each bin for both ports and IP Addresses.
        self.port_increments = int(math.floor(MAX_PORT / self.no_port_bins))
        self.ip_increments = int(math.floor((MAX_IP + 1) / self.no_ip_bins))
        
        # Computes the range of each port bin.
        for i in range(self.no_port_bins):
            if(i < self.no_port_bins - 1):
                self.port_ranges.append((self.port_increments * i + 1, min(self.port_increments * (i + 1), MAX_PORT)))
            else:
                self.port_ranges.append((self.port_increments * i + 1, MAX_PORT))

        # Computes the range of each IP bin.
        for i in range(self.no_ip_bins):
            if(i < self.no_ip_bins - 1):
                self.ip_ranges.append((ip.IP(str(self.ip_increments * i) + ".0.0.0"), ip.IP(str(min(self.ip_increments * (i + 1) - 1, MAX_IP)) + ".255.255.255")))
            else:
                self.ip_ranges.append((ip.IP(str(self.ip_increments * i) + ".0.0.0"), ip.IP(str(MAX_IP) + ".255.255.255")))
    
    '''
    initialize_DS initializes the rules data structure with appropriate sizes of the different bins.
    '''
    def initialize_DS(self):
        # Defines a list of size: [(# direction bins) x (# protocol bins) x (# port_bins) x (# ip_bins)]
        for _ in range(self.no_direction_bins):
            tlist1 = []
            for _ in range(self.no_protocol_bins):
                tlist2 = []
                for _ in range(self.no_port_bins):
                    tlist3 = []
                    for _ in range(self.no_ip_bins):
                        tlist3.append([])
                    tlist2.append(tlist3)
                tlist1.append(tlist2)
            self.rules.append(tlist1)
    
    '''
    read_file reads the input file and calls the add_rule functon to add each rule to the rules DS.
    '''
    def read_file(self):
        f = open(self.file_path, "r")
        line = f.readline()
        while line:
            self.add_rule(line.rstrip())
            line = f.readline()
    
    '''
    add_rule adds each rule to the rules DS by placing it in all the bins that the rule overlaps with.
    '''
    def add_rule(self, rule):
        L = rule.split(",")
        idx1 = 0 if L[0] == 'inbound' else 1
        idx2 = 0 if L[1] == 'tcp' else 1

        start_port = 0
        end_port = 0
        # Check if port specified is a range or a single port.
        if '-' in L[2]:
            start_port = int(L[2].split("-")[0])
            end_port = int(L[2].split("-")[1])
        else:
            start_port = int(L[2])
            end_port = start_port
        
        # Check if IP specified is a range or a single IP address.
        start_ip = ip.IP("0.0.0.0") 
        end_ip = ip.IP("0.0.0.0")
        if '-' in L[3]:
            start_ip = ip.IP(L[3].split("-")[0])
            end_ip = ip.IP(L[3].split("-")[1])
        else:
            start_ip = ip.IP(L[3])
            end_ip = ip.IP(L[3])
        
        # Adds rule to all ranges overlapping.
        for idx3, port_range in enumerate(self.port_ranges):
            if(utils.overlap(start_port, end_port, port_range[0], port_range[1])):
                for idx4, ip_range in enumerate(self.ip_ranges):
                    if(utils.overlap(start_ip, end_ip, ip_range[0], ip_range[1])):
                        self.rules[idx1][idx2][idx3][idx4].append([max(port_range[0], start_port), min(port_range[1], end_port), max(ip_range[0], start_ip), min(ip_range[1], end_ip)])
    
    '''
    accept_packet takes input as a packet and computes the bin it belongs to.
    Then all the rules in that bin are checked to see if they can accept that packet.
    Returns true if at least one rule in that bin accomodates that packet.
    '''
    def accept_packet(self, direction, protocol, port, ip_addr):
        # Computes the index in which the packet falls in,
        idx1 = 0 if direction == 'inbound' else 1
        idx2 = 0 if protocol == 'tcp' else 1
        idx3 = min(math.ceil(port / self.port_increments) - 1, self.no_port_bins - 1)
        idx4 = min(math.floor(int(ip_addr.split(".")[0]) / self.ip_increments), self.no_ip_bins - 1)
        
        # Takes care of a special case if size of bin are 1.
        if(self.port_increments == 1):
            idx3 = min(port - 1, self.no_port_bins - 1)
        if(self.ip_increments == 1):
            idx4 = min(int(ip_addr.split(".")[0]), self.no_ip_bins - 1)
        
        # Checks if any rule in that bin overlaps with this packet.
        for i in self.rules[idx1][idx2][idx3][idx4]:
            if utils.overlap(port, port, i[0], i[1]) and utils.overlap(ip.IP(ip_addr), ip.IP(ip_addr), i[2], i[3]):
                return True

        return False
