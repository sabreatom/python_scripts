#############################################################
#Description:   Python module for Email notifications using #
#               SMTP and Gmail                              #
#Usage:         Import to script                            #
#############################################################

import smtplib

#############################################################
#Gmail SMTP class:
#############################################################

class Gmail_smtp:
    # Constructor
    def __init__(self, mail, passwrd):
        # Store account email:
        self.mail_acc = mail
        # Connect to SMTP:
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        # Start TLS:
        self.server.starttls()
        #Login:
        self.server.login(mail, passwrd)

    # Destructor
    def __del__(self):
        self.server.quit()

    # Send email:
    def send_msg(self, rcvr_mail, subject, msg):
        self.message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (self.mail_acc, rcvr_mail, subject, msg)
        self.server.sendmail(self.mail_acc, rcvr_mail, self.message)
        print("Send mail from %s to email %s"% (self.mail_acc, rcvr_mail))

#############################################################
