"""
@Author : wh1t3kn16ht (Stavros Gkounis)
@Tool : Simple Network Scanner (SNS)
@Version: v1.0
@Description: This tool have 2 modes of scanning:
              1) ICMP Scanner (Checks if the hosts are alive)
              2) Full Open Scanner (Completes the 3-way handshake)

@Tested On: Ubuntu 18.04 LTS, Windows 10
@Python version: Python3
"""


#Libraries needed
import socket
import os
import platform
from datetime import datetime
from optparse import OptionParser


#My Signature
def signature():
    print(" ______________                                                                            ")
    print("|\ ___________ /|                                                                          ")
    print("| |  /|,| |   | |         *****************************************************************")
    print("| | |,x,| |   | |          ╔═╗┬┌┬┐┌─┐┬  ┌─┐  ╔╗╔┌─┐┌┬┐┬ ┬┌─┐┬─┐┬┌─  ╔═╗┌─┐┌─┐┌┐┌┌┐┌┌─┐┬─┐  ")
    print("| | |,x,' |   | |          ╚═╗││││├─┘│  ├┤   ║║║├┤  │ ││││ │├┬┘├┴┐  ╚═╗│  ├─┤││││││├┤ ├┬┘  ")
    print("| | |,x   ,   | |          ╚═╝┴┴ ┴┴  ┴─┘└─┘  ╝╚╝└─┘ ┴ └┴┘└─┘┴└─┴ ┴  ╚═╝└─┘┴ ┴┘└┘┘└┘└─┘┴└─  ")
    print("| | |/    |%==| |                      written by wh1t3kn16ht (Stavros Gkounis)            ")
    print("| |    /] ,   | |         *****************************************************************")
    print("| |   [/ ()   | |                                                                          ")
    print("| |       |   | |                                                                          ")
    print("| |       |   | |                                                                          ")
    print("| |       |   | |                                                                          ")
    print("| |      ,'   | |                                                                          ")
    print("| |   ,'      | |                                                                          ")
    print("|_|,'_________|_|                                                                          ")

# Let's make it a real tool ;)
def arguments():
    parser = OptionParser() # This is our friend. It's going to do all the hard work for us

    parser.add_option('-m', '--mode', type='string', action='store', dest='Mode',
                       help='Possible mode: [Ping Sweeping(icmp), TCP Full Open Scan (sT)')

    parser.add_option('-a', '--address', type='string', action='store', dest='Address',
                       help='Provide the address of the ip address or targeted host ip in mode icmp or sT respectively')

    parser.add_option('--minip', type='int', action='store', dest='MinIP',
                       help='Provide the minimum host address [10 for 192.168.1.10] (only with icmp mode)')

    parser.add_option('--maxip', type='int', action='store', dest='MaxIP',
                       help='Provide the maximum host address [243 for 192.168.1.243] (only with icmp mode)')

    parser.add_option('--minport', type='int', action='store', dest='MinPort',
                       help='Provide the minimum port number (only with sT mode)')

    parser.add_option('--maxport', type='int', action='store', dest='MaxPort',
                       help='Provide the maximum port number (only with sT mode)')

    options,args = parser.parse_args()
    return options.Mode, options.Address, options.MinIP, options.MaxIP, options.MinPort, options.MaxPort

def pingSweeping(ip_address, minip, maxip):
    splitted_ip_address = ip_address.split('.') # In IPv4 the IP addresses (32-bit) are written in dotted decimal notation
    delimiter = '.'  # Due to dotted decimal notation

    network_address = splitted_ip_address[0] + delimiter + splitted_ip_address[1] + delimiter + splitted_ip_address[2] + delimiter  # Now we have 192.168.1. in network address.
                                                                                                                                    
    operatingSystem = platform.system()
    if(operatingSystem == "Windows"):
        part_of_executed_command = "ping -n 1 " # In Windows the command is: ping -n 1 [IP ADDRESS]
    elif(operatingSystem == "Linux"):
        part_of_executed_command = "ping -c 1 " # In  GNU Linux the command is: ping -c 1 [IP ADDRESS]
    else:
        part_of_executed_command = "ping -c 1 " # The other possibility is to be a mac os x. Same as GNU Linux

    startTime = datetime.now()
    print('\n' +'\033[1;94m' + "[*] Ping sweeping started: " + '\033[0m') # '\n' is added for terminal beauty.
    for host_address in range(minip, maxip + 1):
        tested_ip_address = network_address + str(host_address) # Compine the Network address and Host address in order to take the whole IP address.
        command = part_of_executed_command + tested_ip_address # Command example in Linux for host address .5: ping -c 1 192.168.1.5
        output = os.popen(command,'r',1) # Execute the command

        for response in output.readlines(): # Responses differ from OS to OS
            if(operatingSystem == "Linux"):
                if("bytes from" in response):
                    print('\033[1;92m' + "\t[+] Host with IP address {} is ALIVE".format(tested_ip_address) + '\033[0m')
                    break
                elif("Destination Host Unreachable" in response):
                    print('\033[1;93m' + "\t[-] Host with IP address {} may be DEAD or firewall is ON".format(tested_ip_address) + '\033[0m')
                    break
            elif(operatingSystem == "Windows"):
                if("TTL" in response):
                    print('\033[1;92m' + "\t[+] Host with IP address {} is ALIVE".format(tested_ip_address) + '\033[0m')
                    break
                elif("Destination host unreachable" in response):
                    print('\033[1;93m' + "\t[-] Host with IP address {} may be DEAD or firewall is ON".format(tested_ip_address) + '\033[0m')
                    break
            else:
                if("bytes from" in response):
                    print('\033[1;92m' + "\t[+] Host with IP address {} is ALIVE".format(tested_ip_address) + '\033[0m')
                    break
                elif("Destination Host Unreachable" in response):
                    print('\033[1;93m' + "\t[-] Host with IP address {} may be DEAD or firewall is ON".format(tested_ip_address) + '\033[0m')
                    break

    finishTime = datetime.now()
    totalTime = finishTime - startTime
    print('\033[1;94m' + "[*] Ping sweeping finished in: {}".format(totalTime) +'\033[0m')

def tcp_full_open_scan(target, minPort, maxPort):
    if(target == None):
        print('\n' + '\033[1;91m' + "[!] You have to specify the address" + '\033[0m')
    else:
        print('\n' + '\033[1;94m' + "[*] Scanning target {}".format(target) + '\033[0m')
        startTime = datetime.now()
        try:
            for port in range(minPort,maxPort + 1): # Well-Known ports [0-1023]
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection_result = s.connect_ex((target,port))
                if(connection_result == 0):
                    print('\033[1;92m' + "\t[+] Port {} is open".format(port) + '\033[0m')
                s.close()
            finishTime = datetime.now()
            totalTime = finishTime - startTime
            print('\033[1;94m' + "[*] Scanning finished in: {}".format(totalTime) + '\033[0m')
        except:
            print('\n' + '\033[1;91m' + "An Exception has been risen" + '\033[0m')

def main():
    mode, address, minimum_host_ip, maximum_host_ip, minimum_port_number, maximum_port_number = arguments()
    signature()
    if(mode is None):
        print('\n' + '\033[1;91m' + "[!] You have to specify the mode" + '\033[0m')
    else:
        if((mode == 'icmp') and (address is not None)):
            if ((minimum_host_ip >= 0 and maximum_host_ip >= 0) and (maximum_host_ip > minimum_host_ip)):
                pingSweeping(address,minimum_host_ip,maximum_host_ip)
        elif((mode == 'sT') and (address is not None)):
            if ((minimum_port_number >= 0 and maximum_port_number >= 0) and (maximum_port_number > minimum_port_number)):
                tcp_full_open_scan(address, minimum_port_number, maximum_port_number)
        else:
            print('\n' + '\033[1;93m' + "[!] There is not such mode. Try again" + '\033[0m')
            os.system(exit(1))

if(__name__ == "__main__"):
    main()
else:
    print("It's not supposed to be imported")
