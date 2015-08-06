#!/usr/bin/env python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
import sys
import imaplib
import getpass
import email
import email.header
import datetime

EMAIL_ACCOUNT = "aretherebagels@gmail.com"
EMAIL_PASSWORD = "wherearethebagels"
EMAIL_FOLDER = "Inbox"


def process_mailbox(M):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, '(UNSEEN SUBJECT "bagels")')
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print 'Message %s: %s' % (num, subject)

        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")

        text_file = open("./tmp/aretherebagels.txt", "w")
        text_file.write("yes")
        text_file.close()


def run():
    M = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    except imaplib.IMAP4.error:
        print "LOGIN FAILED!!! "
        sys.exit(1)

    print rv, data

    rv, mailboxes = M.list()

    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print "Processing mailbox...\n"
        process_mailbox(M)
        M.close()
    else:
        print "ERROR: Unable to open mailbox ", rv

    M.logout()
