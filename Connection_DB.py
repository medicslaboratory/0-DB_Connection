#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:42:30 2020

@author: ldieumegarde

THIS IS AN EXAMPLE FILE TO CONNECT TO THE CoDE:AIR DATABASE
YOU CAN USE PARTS OF THE CODE YOU NEED, AND REMOVE MY COMMENTARIES et al.

"""

import sys
import mysql.connector
import xml.dom.minidom

######################################## IMPORTANT ######################################
######################################## IMPORTANT ######################################
#########################################################################################
### YOU NEED THE FILE 'config.xml' TO CONNECT TO THE DATABASE
### YOU GOT TO CHANGE THE PATH TO THE 'config.xml' FILE WHERE YOU PUT IT ON YOUR COMPUTER
### AND PUT 'config.xml' IN THE .gitignore BEFORE YOU push/commit YOUR CODE.
lexml = xml.dom.minidom.parse("/Users/ldieumegarde/Dropbox (Professional)/MEDICS Team Folder/Research/COVID-19/Database/Database_Connection/config.xml");
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
    
    
""" TIPS ###################################################################################
Objects I suggest you query from (Table and Views). But you can use the tables directly (remove the prefix 'subject_'):
        [See 'Shema_DB_Production.pdf' on Dropbox for DB structure]
        [See 'CoDE_AIR _DIC.pdf' on Dropbox for fields definitions]
    identification,
    subject_diagnostic,
    subject_imaging,
    subject_inclusion,
    subject_interventions,
    subject_laboratory,
    subject_medical_history,
    subject_outcome,
    subject_scores,
    subject_symptoms,
    subject_vital_signs

When you do a query, SELECT * (asterisk) means all fields. You can also do 
    SELECT <table name>.<fields1>, <table name>.<fields2>, ...
Best practice is to use <table name>.<field name>
--->>> Missing date are tagged as '1000-01-01'

If you wanna join 2 tables or views:
    SELECT * 
    FROM subject_inclusion 
    INNER JOIN subject_imaging ON subject_inclusion.subjid = subject_imaging.subjid

if you wanna filter you results by applying a condition:
    SELECT *
    FROM subject_imaging
    WHERE subject_imaging.site = 'JGH'

if you wanna filter you results by applying a condition (NULL condition):    
    SELECT * 
    FROM subject_imaging 
    WHERE subject_imaging.xray_image IS NOT NULL

if you want to order your result:
    SELECT *
    FROM subject_imaging
    WHERE subject_imaging.site = 'JGH'
    ORDER BY subject_imaging.external_id ASC ### (or DESC for z-a)
    
if you wanna filter you results by applying a condition (dates):
    ### note that missing date are tagged as '1000-01-01'
    SELECT * 
    FROM subject_inclusion 
    INNER JOIN subject_imaging ON subject_inclusion.subjid = subject_imaging.subjid
    WHERE subject_inclusion.site = 'JGH'
    AND (
        (subject_imaging.xray_datetime < '2020-03-27' AND subject_imaging.xray_datetime > '2020-03-21') 
        OR (subject_imaging.xray_datetime = '1000-01-01')
        )

if you want all the database:
    SELECT *
    FROM identification
    LEFT JOIN    diagnostic ON diagnostic.subjid_subjid_id = identification.subjid
    LEFT JOIN    imaging ON imaging.subjid_subjid_id = identification.subjid    
    LEFT JOIN    interventions ON interventions.subjid_subjid_id = identification.subjid
    LEFT JOIN    laboratory ON laboratory.subjid_subjid_id = identification.subjid
    LEFT JOIN    medical_history ON medical_history.subjid_subjid_id = identification.subjid
    LEFT JOIN    outcome ON outcome.subjid_subjid_id = identification.subjid
    LEFT JOIN    scores ON scores.subjid_subjid_id = identification.subjid
    LEFT JOIN    symptoms ON symptoms.subjid_subjid_id = identification.subjid
    LEFT JOIN    vital_signs ON vital_signs.subjid_subjid_id = identification.subjid
    WHERE identification.valid = 1

IF YOU WANT A MORE COMPLEX QUERY, ASK ME AND I WILL BUILT IT DIRECTLY IN THE DATABASE (Views) FOR YOU TO USE.
louis.dieumegarde@cervo.ulaval.ca

"""
