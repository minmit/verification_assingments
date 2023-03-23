from z3 import *

import socket, struct

DROP_PORT = 10

class IPPrefix:
    def __init__(self, ip, prefix_len):
        self.ip = ip
        self.prefix_len = prefix_len

    def get_ip(self):
        return self.ip

    def get_len(self):
        return self.prefix_len


def ip2int(ip):
    packed = socket.inet_aton(ip)
    return struct.unpack("!L", packed)[0]

def dstip_matches_prefix(dstip_vars, prefix):
    prefix_len = prefix.get_len()
    prefix_ip_int = ip2int(prefix.get_ip())
    prefix_ip_int = prefix_ip_int >> (32 - prefix_len)

    formulas = []

    loop_range = range(0, prefix_len)
    for i in loop_range:
        rule_val = True if prefix_ip_int % 2 == 1 else False
        index = 32 - prefix_len + i
        f = dstip_vars[index] == rule_val         
        formulas.append(f)
        
        prefix_ip_int = prefix_ip_int >> 1

    return And(formulas)

def create_fib_model(fib_fname):
    
    var_names = [f'd{i}' for i in range(1, 33)]
    var_names_concatenated = ' '.join(var_names)
    dstip_vars = Bools(var_names)

    output_port = Int('port')

    rules = []
    fib_file = open(fib_fname, 'r')
    for line in fib_file.readlines():
        parts = [p.strip() for p in line.strip().split()]
        if len(parts) != 3:
            continue

        try:
            rule_ip = parts[0]
            rule_prefix_len = int(parts[1])
            rule_port = int(parts[2])
            rules.append((IPPrefix(rule_ip, rule_prefix_len), rule_port))
        except e:
            continue
    
    ''' TODO: create a formula
              capturing the forwarding behavior
              specified by the rules
    '''
    fib_model = []

    for rule in rules:
        prefix, rule_port = rule    

        ## TODO: If the packet matches this rule AND
        ##       none of the prior ones, the output port
        ##       should be set according to this rule.
        ## Hint: The formula (f) is of the form Implies(AND(p, q), r),
        ##       where p captures the condition that the packet
        ##       does not match any prior rules, q captures the condition
        ##       that the packet matches the current rules, and r
        ##       captures the fact that output_port should be set
        ##       according to the port in this rule 
       
        f = ...

        fib_model.append(f)

    ## TODO: If the packet doesn't match anything,
    ##       the packet should be dropped
    ## Hint: The formula (f) is of the form Implies(p, q),
    ##       where p captures the condition that the packet
    ##       does not match any of the rules, and q captures
    ##       the fact that output_port should be set to DROP_PORT

    f = ...
    fib_model.append(f)

    return (dstip_vars, output_port, And(fib_model))

def check_property(dstip_vars, output_port, fib_model,
                   prefix_to_check):

    ## TODO: create the formula that checks 
    ##       that no packets from "prefix_to_check"
    ##       will be dropped by the FIB. 
    
    to_check = ...
    
    s = Solver()
    res = s.check(to_check)
  
    if res == unsat:
        print(f'No packets from {prefix_to_check} will be dropped!')

    elif res == sat:
        m = s.model()
        print(f'A packet with the following dstip, that belongs to {prefix_to_check}, will be dropped: ', end = '')
        ip_int = 0
        for i in range(31, -1, -1):
            var = dstip_vars[i]
            var_val = 1 if m.evaluate(var) == True else 0
            ip_int = ip_int * 2 + var_val

        print(socket.inet_ntoa(struct.pack('!L', ip_int)))
