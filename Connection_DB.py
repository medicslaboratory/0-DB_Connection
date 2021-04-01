#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:42:30 2020

@author: ldieumegarde

THIS IS AN EXAMPLE FILE TO CONNECT TO A DATABASE
YOU CAN USE PARTS OF THE CODE YOU NEED, AND REMOVE MY COMMENTARIES et al.

"""

import sys
import mysql.connector
import xml.dom.minidom

######################################## IMPORTANT ######################################
######################################## IMPORTANT ######################################
#########################################################################################
### YOU NEED THE FILE 'login.xml' TO CONNECT TO THE DATABASE
### YOU GOT TO CHANGE THE PATH TO THE 'login.xml' FILE WHERE YOU PUT IT ON YOUR COMPUTER
### AND PUT 'login.xml' IN THE .gitignore BEFORE YOU push/commit YOUR CODE.
lexml = xml.dom.minidom.parse("/Path_to/login.xml");
#########################################################################################
######################################## IMPORTANT ######################################
######################################## IMPORTANT ######################################

# Get xml info
lehost = lexml.getElementsByTagName('host')[0].firstChild.data
ledb = lexml.getElementsByTagName('db')[0].firstChild.data
leuser = lexml.getElementsByTagName('user')[0].firstChild.data
lepass = lexml.getElementsByTagName('pass')[0].firstChild.data

# Connect to the database
connection = mysql.connector.connect(host=lehost, user=leuser, passwd=lepass, db=ledb)
# Use this line if you got 'caching_sha2_password' error
#connection = mysql.connector.connect(host=lehost, user=leuser, passwd=lepass, db=ledb, auth_plugin='mysql_native_password')
# initialize a pointer
mycursor = connection.cursor(dictionary=True, buffered=True)

# your query
lesql = "SELECT * FROM subject_interventions WHERE subjid < 10"

try:
    # execute your query
    mycursor.execute(lesql)
    # print number of result if you want
    print("There is " + str(mycursor.rowcount) + " result(s) from the query \"" + lesql + "\"")
    # loop through the result (even if only one) 
    for row in mycursor:
        # do your stuff
        print("Patient " + row['external_id'] + ", subjid = " + str(row['subjid']))
except mysql.connector.Error as err:
    sys.exit("Something went wrong: {}".format(err))
finally:
    connection.close()

