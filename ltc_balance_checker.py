#!/usr/bin/python
import subprocess
import json
import os, sys
import smtplib

fromaddr = 'from_address'
toaddrs = ['to_address', 'to_address2']
ccaddrs = ['cc_addresses']


# Credentials (if needed)  
username = '<gmail_username>'  
password = 'gmail_password' 


def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
  
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

proc = subprocess.Popen(["<some_directory>/litecoind", "getinfo"], stdout=subprocess.PIPE)
(out, err) = proc.communicate()

decoded = json.loads(out)

# print current difficulty
ltc_difficulty =  decoded['difficulty']
print('LTC Difficulty: %s' % ltc_difficulty)
# print current balance
ltc_balance = decoded['balance']
print('LTC Balance: %s LTC' % ltc_balance)

# Current blocks
ltc_blocks = decoded['blocks']
print('LTC Blocks: %s' % ltc_blocks)

the_path = '<some_directory>/balnace.txt'
if os.path.exists(the_path):
        file = open(the_path,'r')
        line = file.readline()
        print("There are %s amount" % line)
        file.close()
        
        if float(ltc_balance) != float(line):
                file = open(the_path, 'w')
                file.write('%s'% ltc_balance)
                file.close()
                print("Earned some LTC")
                
                message = 'We currently have \nLTC Balance %s\nLTC Block %s\nLTD Difficulty %s'% (ltc_balance, ltc_blocks,ltc_difficulty)  
				subject = 'LTC Balance: %s' % ltc_balance

                sendemail(fromaddr,toaddrs,ccaddrs,subject,message,username,password)
                print "email sent!"

else:
        file = open(the_path,'w+')
        file.write('%s' % ltc_balance)
        file.close()
        message = 'We currently have \nLTC Balance %s\nLTC Block %s\nLTD Difficulty %s'% (ltc_balance, ltc_blocks,ltc_difficulty)  
		subject = 'LTC Balance: %s' % ltc_balance

		sendemail(fromaddr,toaddrs,ccaddrs,subject,message,username,password)
		print "email sent!"




