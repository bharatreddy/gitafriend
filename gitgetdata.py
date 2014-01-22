class GetGit(object):
    """
    A Class to use github api to download data for the git-a-friend project
    The class makes multiple requests for a single user and retrieves info
    It can also be used to print the retireved info and also check usage limit

    Author : Bharat Kunduri
    """
    
    def __init__( self, userName='bharatreddy' ):
        # The personalized access token string
        self.accToken = '94944ead59b631c8144fd3d5632513579665e4ba'
        self.userName = userName

    def getSingleUserData( self ):
        """
        Get All the relevant data of the user...
        Remember we need a lot of stuff and it means 
        we query multiple times per user...
        I'm starting with my username unless specified.
        create a new Urllib2 Request object
        """   
        import json
        import urllib2
        import re
       
        req = urllib2.Request( 'https://api.github.com/users/' + self.userName )
        # add any additional headers you like 
        req.add_header( 'Accept', 'application/json' )
        req.add_header( "Content-type", "application/x-www-form-urlencoded" )
        # add the authentication header, required
        req.add_header( "Authorization", "token " + self.accToken )
        # make the request and print the results
        res = urllib2.urlopen( req )
        # Store the results in a JSON file
        userResJson = json.loads( res.read() )
        # These are the information we can retrieve from the user json
        # id, login, name, created/start date, num. of followers and num. of . following
        userIdData = userResJson['id']
        userLoginData = userResJson['login']
        userStartDateData = userResJson['created_at']
        userNumFlwrsData = userResJson['followers']
        userNumFlwngData = userResJson['following']
        # Sometimes we don't have 'name' keyword in the Json
        # In that case populate it with a login 
        if 'name' in userResJson :
            # Sometimes we get None for a username for some reason...
            if userResJson['name'] == None :
                userNameData = userResJson['login']
            else :
                userNameData = userResJson['name']
        else :
            userNameData = userResJson['login']
        
        # now get List of Followers, Following, repos, orgs from the urls
        # The same stuff we did above
        reqFlwr = urllib2.Request( userResJson["followers_url"] )
        reqRepo = urllib2.Request( userResJson["repos_url"] )
        reqOrgs = urllib2.Request( userResJson["organizations_url"] )
        # Add the headers like we did above
        reqFlwr.add_header( "Accept", "application/json" )
        reqFlwr.add_header( "Content-type", \
            "application/x-www-form-urlencoded" )
        reqFlwr.add_header( "Authorization", \
            "token 94944ead59b631c8144fd3d5632513579665e4ba" )
        reqRepo.add_header( "Accept", "application/json" )
        reqRepo.add_header( "Content-type", \
            "application/x-www-form-urlencoded" )
        reqRepo.add_header( "Authorization", \
            "token 94944ead59b631c8144fd3d5632513579665e4ba" )
        reqOrgs.add_header( "Accept", "application/json" )
        reqOrgs.add_header( "Content-type", \
            "application/x-www-form-urlencoded" )
        reqOrgs.add_header( "Authorization", \
            "token 94944ead59b631c8144fd3d5632513579665e4ba" )
        # Followers data
        res = urllib2.urlopen( reqFlwr )
        ResJson2 = json.loads( res.read() )
        # store the followers in a list
        followerList = [ ResJson2[x]['login'] \
        for x in range( len( ResJson2 ) ) ]
        # Things get a little complicated with following and starred repos 
        # There are some unwanted stuff in the urls returned, filter them now
        # We need to do some string operations
        # with the following_url and starred_url to remove all the '{' stuff
        flwngStrng = userResJson["following_url"]
        repStrdStrng = userResJson["starred_url"]
        chkSubStrng = '{'
        flst = re.search( chkSubStrng, flwngStrng )
        rsst = re.search( chkSubStrng, repStrdStrng )
        # Now get the correct url by removing the { part
        flwngStrng = flwngStrng[ 0: flst.start() ]
        repStrdStrng = repStrdStrng[ 0: rsst.start() ]
        # Now pass the requests and get the Jsons for following_url
        reqFlng = urllib2.Request( flwngStrng )
        reqFlng.add_header( "Accept", "application/json" )
        reqFlng.add_header( "Content-type", \
            "application/x-www-form-urlencoded" )
        reqFlng.add_header( "Authorization", \
            "token 94944ead59b631c8144fd3d5632513579665e4ba" )
        res = urllib2.urlopen( reqFlng )
        flwngJson = json.loads( res.read() )
        # Get a List of all people following the user
        followingList = [ flwngJson[y]['login'] \
        for y in range( len( flwngJson ) ) ] 
        # Now pass the requests and get the Jsons for starred Repos
        reqStrd = urllib2.Request( repStrdStrng )
        reqStrd.add_header( "Accept", "application/json" )
        reqStrd.add_header( "Content-type", \
            "application/x-www-form-urlencoded" )
        reqStrd.add_header( "Authorization", \
            "token 94944ead59b631c8144fd3d5632513579665e4ba" )
        reqStrd.add_header( "Authorization", \
            "token 94944ead59b631c8144fd3d5632513579665e4ba" )
        try :
            res = urllib2.urlopen( reqStrd )
            strdRepoJson = json.loads( res.read() )
            # List of all the repos starred
            starredRepoList = [ strdRepoJson[y]['name'] \
            for y in range( len( strdRepoJson ) ) ]
        except urllib2.HTTPError, e:
               print e.code
               starredRepoList = []
        except urllib2.URLError, e:
               print e.args
               starredRepoList = []
        # Now move on to getting the list of languages the user codes in..
        try :
            res = urllib2.urlopen( reqRepo )
            ResJson3 = json.loads( res.read() )
            repoList =  [ ResJson3[x]['name'] for x in range( len( ResJson3 ) ) ]
        except urllib2.HTTPError, e:
               print e.code
               repoList = []
        except urllib2.URLError, e:
               print e.args
               repoList = []
        languateList = []
        for rr in range( len( ResJson3 ) ) :
            currVal = ResJson3[rr]
            # Again we query github for more info..
            # AS we do above
            reqLang = urllib2.Request( currVal[ 'languages_url' ] )
            reqLang.add_header( "Accept", "application/json" )
            reqLang.add_header( "Content-type", \
                "application/x-www-form-urlencoded" )
            reqLang.add_header( "Authorization", \
                "token 94944ead59b631c8144fd3d5632513579665e4ba" )
            try :
                res = urllib2.urlopen( reqLang )
                ResJson5 = json.loads( res.read() )
                for ll in ResJson5.keys() :
                    if ll not in languateList :
                        languateList.append( ll )
            except urllib2.HTTPError, e:
                   print e.code
            except urllib2.URLError, e:
                   print e.args
        # We are not yet done with the language list, we also need repos 
        # we contribute to ( from organizations etc.... )
        try :
            res = urllib2.urlopen( reqOrgs )
            ResJson4 = json.loads( res.read() )
            # At the same time we can get a list of organizations of interest
            orgsList = [ ResJson4[x]['login'] for x in range( len( ResJson4 ) ) ]
            # Now loop through the organization list
            # Get their repos... and check if the user contributed
            # to the repos.. if so get the list of the languages in the repo.
            for kk in range( len( ResJson4 ) ):
                currVal = ResJson4[ kk ]
                req = urllib2.Request( ResJson4[kk]['repos_url'] )
                req.add_header( "Accept", "application/json" )
                req.add_header( "Content-type", \
                    "application/x-www-form-urlencoded" )
                req.add_header( "Authorization", \
                    "token 94944ead59b631c8144fd3d5632513579665e4ba" )
                res = urllib2.urlopen( req )
                ResJson6 = json.loads( res.read() )
                for jk in range( len( ResJson6 ) ):
                    # More github queries....
                    # This never ends....
                    req = urllib2.Request( ResJson6[jk]['contributors_url'] )
                    req.add_header( "Accept", "application/json" )
                    req.add_header( "Content-type", \
                        "application/x-www-form-urlencoded" )
                    req.add_header( "Authorization", \
                        "token 94944ead59b631c8144fd3d5632513579665e4ba" )
                    try:
                        res = urllib2.urlopen( req )
                        ResJson7 = json.loads( res.read() )
                        for lk in range( len( ResJson7 ) ):
                            if userResJson["login"] ==  ResJson7[lk]['login']  :
                                if ResJson6[0]['name'] not in repoList :
                                    # More queries for language info...
                                    repoList.append( ResJson6[0]['name'] )
                                    req = urllib2.Request( ResJson6[jk]['languages_url'] )
                                    req.add_header( "Accept", "application/json" )
                                    req.add_header( "Content-type", \
                                        "application/x-www-form-urlencoded" )
                                    req.add_header( "Authorization", \
                                        "token 94944ead59b631c8144fd3d5632513579665e4ba" )
                                    res = urllib2.urlopen( req )
                                    ResJson8 = json.loads( res.read() )
                                    for ll in ResJson8.keys() :
                                        if ll not in languateList :
                                            languateList.append( ll )
                    except urllib2.HTTPError, e:
                       print e.code
                    except urllib2.URLError, e:
                       print e.args
        except urllib2.HTTPError, e:
               print e.code
               orgsList = []
        except urllib2.URLError, e:
               print e.args
               orgsList = []
        # Return the data we need
        return userIdData, userLoginData, userStartDateData, \
            userNumFlwrsData, userNumFlwngData, userNameData, followerList, \
            followingList, repoList, starredRepoList, orgsList, languateList

    def printCurrUserData( self ):
        """
        This function is to check if code is running and where currently
        we just print user details to screen
        no need to call te 'getSingleUserData' func, it is called internally
        """
        # Basically some pretty printing stuff
        printerData = self.getSingleUserData()
        print 'user-id : ', printerData[0]
        print 'login : ', printerData[1]
        print 'Name : ', printerData[5]
        print 'start-date : ', printerData[2]
        print 'list of organizations : ', printerData[10]
        print 'Num. of followers : ', printerData[3]
        print 'Num. of people following the user : ', printerData[4]
        if printerData[4] < 10 :
            print 'list of followers : ', printerData[6]
        else :
            print 'user is a git celeb to many people following'
        if printerData[3] < 10 :
            print 'list of people following : ', printerData[7]
        else :
            print 'following many people.. too many to print'
        print 'list of repos contributed to : ', printerData[8]
        print 'list of repos starred : ', printerData[9]
        print 'list of languages used : ', printerData[11]

    def checkUseLimit( self ):
        """
        This function is to check if we exceeded the usage limit
        """
        import urllib2
        import json

        # The link to checking rate limit
        req = urllib2.Request( 'https://api.github.com/rate_limit' )
        # add any additional headers you like 
        req.add_header( 'Accept', 'application/json' )
        req.add_header( "Content-type", "application/x-www-form-urlencoded" )
        # add the authentication header, required
        req.add_header( "Authorization", "token " + self.accToken )
        # make the request and print the results
        res = urllib2.urlopen( req )
        # Store the results in a JSON file
        chkLimJson = json.loads( res.read() )
        # Return the remaining limit
        return chkLimJson['rate']['remaining']