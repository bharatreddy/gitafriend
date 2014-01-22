import gitgetdata
import dbmngr
import json
import datetime
class PopGitUserDB(object):
    """ Code to populate the gituserinfo database
        Crawl through users to populate the database
        I start with my own username

        Author : Bharat Kunduri
    """
    def __init__( self ):
        # The first person to start the crawl with
        self.startUserLogin='phaus'

    def popSingleUserInfo( self, userLogin='bharatreddy' ):
        """ In this function, data for a single user is populated 
            in the respective tables... we have 6 of them
        """
        # Initialize the gitobj... This fetches the git data from the api
        # Right now I'm starting with my own username
        gitObj = gitgetdata.GetGit( userName=userLogin )
        # get the data
        gitData = gitObj.getSingleUserData()
        # Now initialize the database obj
        dbObj = dbmngr.DbAccess( 'gituserinfo', usr='root' )
        # now we need to put our data into proper dicts to store it in the database
        # we'll start with the userdict
        userDict = {}
        userDict['login'] = gitData[1]
        userDict['id'] = gitData[0]
        if len( gitData[5] ) > 25 :
            userDict['name'] = gitData[5][0:25]
        else :
            userDict['name'] = gitData[5]
        
        # We need to convert this datetime string into mysql date
        userDict['start_date'] = datetime.datetime.strptime(gitData[2].split(".")[0],\
         "%Y-%m-%dT%H:%M:%SZ")
        userDict["nflwr"] = gitData[3]
        userDict["nflwng"] = gitData[4]
        # There could be multiple organizations so we do a json.dump
        jsonOrgData = json.dumps( gitData[10] )
        if len( jsonOrgData ) > 190 :
            jsonOrgData = jsonOrgData[0:50]
        userDict["orgnztn"] = jsonOrgData
        # Populate the userdetails table
        dbObj.popUserDet( userDict )
        # Repos Contributed
        # Now we loop through the repos contributed to store them
        for x in range( len( gitData[8] ) ):
            repocntrDict = {}
            repocntrDict['login'] = gitData[1]
            repocntrDict['id'] = gitData[0]
            repocntrDict['repocntrbtd'] = gitData[8][x]
            if len( gitData[8][x] ) < 50 :
                repocntrDict['repocntrbtd'] = gitData[8][x]
            else :
                repocntrDict['repocntrbtd'] = gitData[8][x][0:45]
            dbObj.popRepoCntr( repocntrDict )
        # loop through the repos starred to store them
        for x in range( len( gitData[9] ) ):
            repostrdDict = {}
            repostrdDict['login'] = gitData[1]
            repostrdDict['id'] = gitData[0]
            if len( gitData[9][x] ) < 50 :
                repostrdDict['repostrd'] = gitData[9][x]
            else :
                repostrdDict['repostrd'] = gitData[9][x][0:45]
            dbObj.popRepoStrd( repostrdDict )
        # loop through the prog languages to store them
        for x in range( len( gitData[11] ) ):
            progLangDict = {}
            progLangDict['login'] = gitData[1]
            progLangDict['id'] = gitData[0]
            progLangDict['langused'] = gitData[11][x]
            dbObj.popProgLang( progLangDict )
        # loop through the people following to store them
        for x in range( len( gitData[7] ) ):
            flwngDict = {}
            flwngDict['login'] = gitData[1]
            flwngDict['id'] = gitData[0]
            flwngDict['flnglogin'] = gitData[7][x]
            dbObj.popFlwng( flwngDict )
        # loop through the followers to store them
        for x in range( len( gitData[6] ) ):
            flwrDict = {}
            flwrDict['login'] = gitData[1]
            flwrDict['id'] = gitData[0]
            flwrDict['flwrlogin'] = gitData[6][x]
            dbObj.popFlwr( flwrDict )
        # Since we later do some crawling return the 
        # list of people user follows and people who follow him
        return gitData[7] + gitData[6]

    def crawlUsers( self ):
        """ In this function we crawl through users 
            starting from a given one to populate the database
        """
        import time

        # The list of users to crawl...
        listToCrawl = [ self.startUserLogin ]
        # We need to make a list of users crawled already 
        # to avoid recrawling them
        listCrawlCompleted = []
        # Keep track of how many users are populated in the database already
        countCrawls = 1
        # As long as listToCrawl has users keep crawling....
        while len( listToCrawl ) > 0 :
            # However before proceeding we need to check our usage limit
            # If we exceed the limit wait for some time
            gitChkLimObj = gitgetdata.GetGit()
            limRem = gitChkLimObj.checkUseLimit()
            if limRem > 20 :
                print 'crawling user number : ', countCrawls, ' , with login : '\
                , listToCrawl[0]
                print 'finished crawling : ', len( listCrawlCompleted ), \
                ' users, yet to crawl ', len( listToCrawl ), 'more...'
                nextCrawlArr = self.popSingleUserInfo( userLogin=listToCrawl[0] )
                # Populate of list to crawl with new users
                for nn in nextCrawlArr :
                    if nn not in listToCrawl :
                        if nn not in listCrawlCompleted :
                            listToCrawl.append( nn )
                # Now that we are done with the current user 
                # remove him from the list
                # Also make a list of users already crawled
                listCrawlCompleted.append( listToCrawl[0] )
                listToCrawl.pop(0)
                countCrawls += 1
            else :
                # sleep for about 5 min before trying again
                print 'exceeded usage limit...waiting 5 min'
                time.sleep(300)