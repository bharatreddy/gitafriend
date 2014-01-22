import mysql.connector
from mysql.connector import errorcode
import json
import os
import sys

class DbAccess(object):
    """
    Access database, and populate, retreive github data
    We are using 6 different tables for the data

    Author : Bharat Kunduri
    """
    def __init__(self, db_name, usr='', pwd=None):
        # Connect to the database using the user details
        self.db_name = db_name
        self.db_url = "localhost"
        self.connect(usr, pwd)
        self.cursor = self.cnx.cursor()

    def connect(self, usr, pwd=None):
        """
        Try to connect to DB
        """
        try:
            self.cnx = mysql.connector.connect(user=usr, password=pwd, 
                database=self.db_name, host=self.db_url)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            sys.exit(1)

    def close(self):
        """
        Disconnect from DB
        """
        self.cursor.close()
        self.cnx.close()
    # The part below deals with putting the data into the database
    def popUserDet(self, userDict):
        """
        Populate the userdetail table
        """
        query = ("INSERT INTO userdetail "
               " (login, id, name, start_date, nflwr, nflwng, orgnztn) "
               " VALUES (%s, %s, %s, %s, %s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   login=VALUES(login), "
               "   id=VALUES(id), "
               "   name=VALUES(name), "
               "   start_date=VALUES(start_date), "
               "   nflwr=VALUES(nflwr), "
               "   nflwng=VALUES(nflwng), "
               "   orgnztn=VALUES(orgnztn) ")
        params = (
            userDict['login'], 
            userDict['id'], 
            userDict['name'], 
            userDict['start_date'], 
            userDict["nflwr"], 
            userDict["nflwng"], 
            userDict["orgnztn"])
        self.cursor.execute(query, params)
        self.cnx.commit()

    def popRepoStrd(self, repStrDict):
        """
        Populate the repostarred table
        """
        query = ("INSERT INTO repostarred "
               " (login, id, repostrd) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   login=VALUES(login), "
               "   id=VALUES(id), "
               "   repostrd=VALUES(repostrd) ")
        params = (
            repStrDict['login'], 
            repStrDict['id'], 
            repStrDict['repostrd'])
        self.cursor.execute(query, params)
        self.cnx.commit()

    def popRepoCntr(self, repContrDict):
        """
        Populate the repocntrbtd table
        """
        query = ("INSERT INTO repocontr "
               " (login, id, repocntrbtd) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   login=VALUES(login), "
               "   id=VALUES(id), "
               "   repocntrbtd=VALUES(repocntrbtd)")
        params = (
            repContrDict['login'], 
            repContrDict['id'], 
            repContrDict['repocntrbtd'])
        self.cursor.execute(query, params)
        self.cnx.commit()

    def popProgLang(self, progLangDict):
        """
        Populate the proglang table
        """
        query = ("INSERT INTO proglang "
               " (login, id, langused) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   login=VALUES(login), "
               "   id=VALUES(id), "
               "   langused=VALUES(langused) ")
        params = (
            progLangDict['login'], 
            progLangDict['id'], 
            progLangDict['langused'])
        self.cursor.execute(query, params)
        self.cnx.commit()
        
    def popFlwng(self, flwngDict):
        """
        Populate the following table
        """
        query = ("INSERT INTO following "
               " (login, id, flnglogin) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   login=VALUES(login), "
               "   id=VALUES(id), "
               "   flnglogin=VALUES(flnglogin) ")
        params = (
            flwngDict['login'], 
            flwngDict['id'], 
            flwngDict['flnglogin'])
        self.cursor.execute(query, params)
        self.cnx.commit()

    def popFlwr(self, flwrDict):
        """
        Populate the follower table
        """
        query = ("INSERT INTO follower "
               " (login, id, flwrlogin) "
               " VALUES (%s, %s, %s) "
               " ON DUPLICATE KEY UPDATE "
               "   login=VALUES(login), "
               "   id=VALUES(id), "
               "   flwrlogin=VALUES(flwrlogin) ")
        params = (
            flwrDict['login'], 
            flwrDict['id'], 
            flwrDict['flwrlogin'])
        self.cursor.execute(query, params)
        self.cnx.commit()

    # The part below deals with putting the ranks of the users
    # into the rankusers tabledatabase
    def popRankDet(self, rankList):
        """
        Populate the gitranks table
        """
        query = ("INSERT INTO gitranks2 "
               " (login, rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8," 
                "rank9, rank10, rank11, rank12, rank13, rank14, rank15, rank16, rank17,"
                "rank18, rank19, rank20, rank21, rank22, rank23, rank24, rank25, rank26,"
                "rank27, rank28, rank29, rank30) "
               " VALUES (%s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s"
                ") "
               " ON DUPLICATE KEY UPDATE "
               "   login=VALUES(login), "
               "   rank1=VALUES(rank1), "
               "   rank2=VALUES(rank2), "
               "   rank3=VALUES(rank3), "
               "   rank4=VALUES(rank4), "
               "   rank5=VALUES(rank5), "
               "   rank6=VALUES(rank6), "
               "   rank7=VALUES(rank7), "
               "   rank8=VALUES(rank8), "
               "   rank9=VALUES(rank9), "
               "   rank10=VALUES(rank10), "
               "   rank11=VALUES(rank11), "
               "   rank12=VALUES(rank12), "
               "   rank13=VALUES(rank13), "
               "   rank14=VALUES(rank14), "
               "   rank15=VALUES(rank15), "
               "   rank16=VALUES(rank16), "
               "   rank17=VALUES(rank17), "
               "   rank18=VALUES(rank18), "
               "   rank19=VALUES(rank19), "
               "   rank20=VALUES(rank20), "
               "   rank21=VALUES(rank21), "
               "   rank22=VALUES(rank22), "
               "   rank23=VALUES(rank23), "
               "   rank24=VALUES(rank24), "
               "   rank25=VALUES(rank25), "
               "   rank26=VALUES(rank26), "
               "   rank27=VALUES(rank27), "
               "   rank28=VALUES(rank28), "
               "   rank29=VALUES(rank29), "
               "   rank30=VALUES(rank30) ")
        params = (
            rankList[0], 
            rankList[1], 
            rankList[2], 
            rankList[3], 
            rankList[4], 
            rankList[5],
            rankList[6],
            rankList[7],
            rankList[8],
            rankList[9],
            rankList[10],
            rankList[11], 
            rankList[12], 
            rankList[13], 
            rankList[14], 
            rankList[15],
            rankList[16],
            rankList[17],
            rankList[18],
            rankList[19],
            rankList[20],
            rankList[21], 
            rankList[22], 
            rankList[23], 
            rankList[24], 
            rankList[25],
            rankList[26],
            rankList[27],
            rankList[28],
            rankList[29],
            rankList[30])
        self.cursor.execute(query, params)
        self.cnx.commit()

    # The part below deals with getting the data from the database
    def retAllUserLogin(self):
        """
        Get a list of all the (unique) user-logins in the database
        """
        query = ("""
            SELECT login
            FROM userdetail
            """)
        self.cursor.execute(query)
        return [s[0] for s in self.cursor]

    def retAllLangs(self):
        """
        Get a list of all the languages in the database
        This may be used later for plotting stuff
        """
        query = ("""
            SELECT DISTINCT langused
            FROM proglang
            """)
        self.cursor.execute(query)
        return [s[0] for s in self.cursor]

    def retD3PlotDet(self):
        """
        Get a list of number of follwers and number of repos
        contributed by all users - used for d3 plotting
        """
        query = ("""
            SELECT userdetail.nflwr, count(repocontr.login), repocontr.login
            FROM repocontr JOIN userdetail 
            ON repocontr.login=userdetail.login 
            GROUP BY repocontr.login;
            """)
        self.cursor.execute(query)
        return [s for s in self.cursor]

    def retUserDet(self, userLogin):
        import datetime
        """
        Get info about a single user from the all the databases
        and store it in a dict and return it...
        This dict is later used to populate the Pandas dataframe
        """
        query = ("""
            SELECT start_date, nflwr, nflwng, orgnztn
            FROM userdetail 
            WHERE login=%s
            """)
        self.cursor.execute(query, (userLogin,) )
        # set up the dictionary
        userDict = {}
        # values from the userdetails table
        userdetVals = [s for s in self.cursor]
        # Calculate the number of days the user has been active
        currDate = datetime.date.today()
        numDaysDiff = currDate - userdetVals[0][0]
        userDict['num_days'] = numDaysDiff.days
        userDict['num_flwrs'] = userdetVals[0][1]
        userDict['num_flwng'] = userdetVals[0][2]
        # Some of these strings are bad.. so we need some formatting
        # I had to do that because of limits in how many characters
        # I defined for the database...
        # So basically we are checking if the last letter in the word 
        # is ']' and thereby a complete list
        if userdetVals[0][3][-1] == ']' :
            userDict['orgnztn'] = json.loads( userdetVals[0][3] )
        else :
            orgStr = userdetVals[0][3]
            if userdetVals[0][3][-1] == ',' :
                orgStr = userdetVals[0][3][ 0:len( userdetVals[0][3] )-1 ]
                userDict['orgnztn'] = json.loads( orgStr + ']')
            elif userdetVals[0][3][-1] == ' ' :
                orgStr = userdetVals[0][3][ 0:len( userdetVals[0][3] )-2 ]
                userDict['orgnztn'] = json.loads( str( orgStr + ']' ) )
            else :
                if orgStr[-1] != '"':
                    orgStr = orgStr + '"'
                userDict['orgnztn'] = json.loads( orgStr + ']')
        # get the repo contributed to  and repo starred info
        query = ("""
            SELECT repocntrbtd
            FROM repocontr 
            WHERE login=%s
            """)
        self.cursor.execute(query, (userLogin,) )
        repcntrList = [s[0] for s in self.cursor]
        userDict['repo_cntr'] = repcntrList
        # repo starred list
        query = ("""
            SELECT repostrd
            FROM repostarred 
            WHERE login=%s
            """)
        self.cursor.execute(query, (userLogin,) )
        repstrdList = [s[0] for s in self.cursor]
        userDict['repo_strd'] = repstrdList
        # get the follower  and following people info
        query = ("""
            SELECT flwrlogin
            FROM follower 
            WHERE login=%s
            """)
        self.cursor.execute(query, (userLogin,) )
        flwrList = [s[0] for s in self.cursor]
        userDict['flwr_list'] = flwrList
        # following list
        query = ("""
            SELECT flnglogin
            FROM following 
            WHERE login=%s
            """)
        self.cursor.execute(query, (userLogin,) )
        flwngList = [s[0] for s in self.cursor]
        userDict['flng_list'] = flwngList
        # Finally get a list of the languages used.
        query = ("""
            SELECT langused
            FROM proglang 
            WHERE login=%s
            """)
        self.cursor.execute(query, (userLogin,) )
        langList = [s[0] for s in self.cursor]
        userDict['lang_used'] = langList
        
        return userDict