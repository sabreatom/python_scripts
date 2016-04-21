#########################################################
#Function:  check periodically if IP has changed        #
#           if it changes send notification to          #
#           email(s)                                    #
#Usage: use with cron for periodical check, usage       #
#       example: send_new_ip.py [smtp email] [password] #
#       [receiver email 1] [receiver email 2] ...       #
#########################################################

import sys
import smtplib
import urllib
import json
import os.path
import time

#################################################
#Function to check current IP address:
#################################################

def chck_cur_ip():
    data = json.loads(urllib.urlopen("http://api.ipify.org?format=json").read())
    return data["ip"]

#################################################
#Main:
#################################################

def main():
    if (len(sys.argv) < 4):   # check that there is enought arguments
        print("Number of arguments is less then 3")
        print("Usage: send_new_ip.py [smtp email] [password] [receiver email 1] [receiver email 2] ...")
        sys.exit(1)
    send_email = sys.argv[1]    # read SMTP email which will send emails
    email_pswrd = sys.argv[2]   # read password for SMTP email
    rcvr_arr = []   # init array of receiving emails   
    for i in range(3,len(sys.argv)):  #fill the array of email receiving emails
        rcvr_arr.append(sys.argv[i])

    # Try to open file which stores last IP address 
    try:
        addr_f = open("ip_addr_store.txt", "r")
    except:
        print("[Error] Couldn't open file ip_addr_store.txt!")
        sys.exit(1)        
    # Read last IP address:
    last_ip_addr = addr_f.readline()
    addr_f.close()

    # Check if IP address has changed from last time
    new_ip_addr = chck_cur_ip()
    if (last_ip_addr.strip('\n') != new_ip_addr):
        #Send messages with new IP address
        msg = "Hello, this message has been send from automatic script, please don't reply!\n"
        msg += "IP address has been changed, new one is: "
        msg += new_ip_addr
        msg += "\n"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(send_email, email_pswrd)
        for i in range(len(rcvr_arr)):
            server.sendmail(send_email, rcvr_arr[i], msg)
            time.sleep(5) # wait for 5 sec between each mail
        server.quit()
        # Write new IP address to storage file
        try:                                                # First clear file content
            addr_f = open("ip_addr_store.txt", "w")
        except:
            print("[Error] Couldn't open file ip_addr_store.txt!")
            sys.exit(1)
        addr_f.close()
        addr_f = open("ip_addr_store.txt", "w")
        addr_f.write(new_ip_addr + '\n')
        addr_f.close()
        print("Messages have been send!\n")

    print("Script finished!\n")
    sys.exit(0)
        

#################################################

if __name__ == "__main__":
    main()
