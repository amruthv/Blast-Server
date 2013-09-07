#!/usr/bin/python



import json
import urllib
from geopy import geocoders,distance
import urllib2
import httplib
from BeautifulSoup import BeautifulSoup
import os
from collections import defaultdict
try:
    import cPickle as pickle
except ImportError:
    import pickle # fall back on Python version
import sqlite3 as lite
import datetime
import opml
import simplejson




class ContentHandler:    
    def __init__(self,basedir):
        self.basedir = os.path.abspath(basedir)
        self.build_database(basedir)


    def connect_to_database(self):
        con = None
        try:
            con = lite.connect('content.db')

        except lite.Error, e:
            
            print "Error %s:" % e.args[0]
            sys.exit(1)
        
        return con

    def add_to_database(self,input):
        con = self.connect_to_database()
        cur = con.cursor() 
        USERID=input[0]
        CONTENT=input[1]
        GPS=input[2]+','+input[3]
        TIME=str(datetime.datetime.utcnow())
        with con:
            cur.execute('INSERT INTO BLASTS(USERID,CONTENT,GPS,TIME) VALUES('+"'"+USERID+"'"+','+"'"+CONTENT+"'"+','+"'"+GPS+"'"+','+"'"+TIME+"'"+');')

        con.close()    

    
    def build_database(self,basedir):
        con = self.connect_to_database()
        cur = con.cursor()    
        cur.execute('DROP TABLE BLASTS')
        cur.execute("CREATE TABLE IF NOT EXISTS BLASTS(BLASTID INTEGER PRIMARY KEY,USERID VARCHAR(5),CONTENT VARCHAR(50), GPS VARCHAR(50), TIME VARCHAR(20));")
        
        BLASTID='0001'
        USERID='YAJIT'
        CONTENT='EMERGENCY CAR ACCIDENT'
        g=geocoders.GoogleV3()
        _, ne = g.geocode('500 Memorial Drive, Cambridge, MA')
        GPS=str(ne[0])+','+str(ne[1])
        TIME=str(datetime.datetime.utcnow())
        #print 'INSERT INTO BLASTS(BLASTID,USERID,CONTENT,GPS,TIME) VALUES('+"'"+BLASTID+"'"+','+"'"+USERID+"'"+','+"'"+CONTENT+"'"+','+"'"+GPS+"'"+','+"'"+TIME+"'"+');'
        with con:
            cur.execute('INSERT INTO BLASTS(USERID,CONTENT,GPS,TIME) VALUES('+"'"+USERID+"'"+','+"'"+CONTENT+"'"+','+"'"+GPS+"'"+','+"'"+TIME+"'"+');')

        con.close()    

            

            

    def get_music_database(self,database_file):
        #take database file and return its contents as string
        if database_file=='local':
            f=open('inventory_database.json','r')
        else:
            f=open(database_file,'r')
        json_file=f.read()
        return json_file


    def get_blastIDs(self,location):
        con=self.connect_to_database()
        cur = con.cursor()
        #cur.execute


        #distance=distance.distance(location,ge).mi
        return ['0001']


    

    def build_json_file(self,ID_list): 
        con=self.connect_to_database()
        cur = con.cursor()
        json_data=""
        blasts=[]
        for ID in ID_list:
            cur.execute("select USERID from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict={'USERID':cur.fetchone()}
            cur.execute("select CONTENT from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['CONTENT']=cur.fetchone()
            cur.execute("select GPS from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['GPS']=cur.fetchone()
            cur.execute("select TIME from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['TIME']=cur.fetchone()
            blasts.append(blast_as_dict)
        
        return simplejson.dumps(blasts)

            



            
#contenthandler = ContentHandler('./Content')
#contenthandler.build_json_file(['0001'])


