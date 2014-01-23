import dbmngr
import json
import datetime
import pandas
import dbmngr
import numpy

class VldtGitRanker(object):
    """ Code to validate the recommendations
        check the number of actual followers predicted
        by the code.

        Author : Bharat Kunduri
    """
    def __init__( self ):
        """In this part we load the code into a pandas dataframe
        """
        # Need a database obj to start with, ofcourse
        self.dbObj = dbmngr.DbAccess( 'gituserinfo', usr='root' )
        # get a list of all the users
        # the user logins will make the row headers (index)
        self.userLoginList = self.dbObj.retAllUserLogin()
        # Now we need to make the column headers
        # for now I'll use the these columns to measure similarity
        self.colList = [ 'num_days', 'num_flwrs', 'flwr_list', 'num_flwng', \
        'flng_list', 'repo_cntr', 'repo_strd', 'orgnztn', 'lang_used' ]
        self.userDataFrame = pandas.DataFrame( index=self.userLoginList,\
         columns=self.colList )
        # loop through the user logins and populate the 'userDataFrame' DataFrame
        for ull in self.userLoginList :
            currUserDict = self.dbObj.retUserDet( ull )
            self.userDataFrame.loc[ ull ] = pandas.Series( currUserDict )
        # A dataframe to store the ranks
        self.userRankDF = pandas.DataFrame( index=self.userLoginList,\
         columns=self.userLoginList )

    def vldtFlwrs( self ):
        """In this part we use the user DataFrame from loadData
           and rank them and store it in a seperate DataFrame
           for later use
        """
        
        # Use a weights dictionary to weigh categories
        weightDict = {}
        weightDict['num_days'] = 0.7
        weightDict['num_flwrs'] = 0.1
        weightDict['flwr_list'] = 2.
        weightDict['num_flwng'] = 0.05 # This number can be really high sometimes
        weightDict['flng_list'] = 1.25
        weightDict['repo_cntr'] = 2.
        weightDict['repo_strd'] = 1.75
        weightDict['orgnztn'] = 2.
        weightDict['lang_used'] = 0.8
        # Need a dict to store max values as well to normalize later
        self.normDict = {}
        self.normDict['num_days'] = 0.
        self.normDict['num_flwrs'] = 0.
        self.normDict['flwr_list'] = 0.
        self.normDict['num_flwng'] = 0.
        self.normDict['flng_list'] = 0.
        self.normDict['repo_cntr'] = 0.
        self.normDict['repo_strd'] = 0.
        self.normDict['orgnztn'] = 0.
        self.normDict['lang_used'] = 0.
        # now loop through our user dataframe and store the score
        # this score is simply the inverse of eucledian distance. 
        # higher the score (corresponds to lower distance) 
        # more similar people are.
        for ind in self.userDataFrame.index.unique():
            for col in self.userDataFrame.index.unique():
                # Before proceeding we remove the followers 
                # Except for about 4-5 users, who can serve as validation
                # I include me, people I know and a couple of famous people
                excludeUsers = [ ]
                currUserFlwngList = self.dbObj.retFlwrList( ind )
                if (col in currUserFlwngList) and (ind not in excludeUsers) :
                    currSimilarityScore = 0.
                else :
                    dataUser = self.userDataFrame.ix[ind]
                    dataCmpr = self.userDataFrame.ix[col]
                    # keep a dict for each person's score in different areas
                    scoreDict = {}
                    # Score different things
                    # 180 days-six months
                    dist = abs( dataUser['num_days'] - dataCmpr['num_days'] )/180.
                    scoreDict['num_days'] = 1/( 1 + dist )
                    # update the max value for normalization
                    if scoreDict['num_days'] > self.normDict['num_days'] :
                        if ind != col :
                            self.normDict['num_days'] = scoreDict['num_days']
                    # Num Followers
                    # we score in ten's of people
                    dist = abs( dataUser['num_flwrs'] - dataCmpr['num_flwrs'] )/10.
                    scoreDict['num_flwrs'] = 1/( 1 + dist ) 
                    # update the max value for normalization
                    if scoreDict['num_flwrs'] > self.normDict['num_flwrs'] :
                        # Now this goes to 1 for ind=col (same user) so check it
                        if ind != col :
                            self.normDict['num_flwrs'] = scoreDict['num_flwrs']
                    # Num of people following the user
                    # we score in ten's of people again
                    dist = abs( dataUser['num_flwng'] - dataCmpr['num_flwng'] )/10.
                    scoreDict['num_flwng'] = 1/( 1 + dist )
                    # update the max value for normalization
                    if scoreDict['num_flwng'] > self.normDict['num_flwng'] :
                        if ind != col :
                            self.normDict['num_flwng'] = scoreDict['num_flwng']
                    # Follwer List
                    # fraction of my followers that follow you
                    countNumPpl = 0
                    for mf in dataUser['flwr_list'] :
                        if mf in dataCmpr['flwr_list'] :
                            countNumPpl += 1.
                    if len( dataUser['flwr_list'] ) > 0 :
                        scoreDict['flwr_list'] = countNumPpl/len( \
                            dataUser['flwr_list'] )
                    else:
                        scoreDict['flwr_list'] = 0.
                    # Follwing people List
                    # fraction of people I follow that you do too
                    countNumPpl = 0
                    for mf in dataUser['flng_list'] :
                        if mf in dataCmpr['flng_list'] :
                            countNumPpl += 1.
                    if len( dataUser['flng_list'] ) > 0 :
                        scoreDict['flng_list'] = countNumPpl/len( \
                            dataUser['flng_list'] )
                    else :
                        scoreDict['flng_list'] = 0.
                    # Repo Contr List
                    # fraction of repos I contr to that you did as well
                    countRepo = 0
                    for mf in dataUser['repo_cntr'] :
                        if mf in dataCmpr['repo_cntr'] :
                            countRepo += 1.
                    if len( dataUser['repo_cntr'] ) > 0 :
                        scoreDict['repo_cntr'] = countRepo/len( \
                            dataUser['repo_cntr'] )
                    else :
                        scoreDict['repo_cntr'] = 0.
                    # Repo strd List
                    # fraction of repos I starred to that you did as well
                    countRepo = 0
                    for mf in dataUser['repo_strd'] :
                        if mf in dataCmpr['repo_strd'] :
                            countRepo += 1.
                    if len( dataUser['repo_strd'] ) > 0 :
                        scoreDict['repo_strd'] = countRepo/len( \
                            dataUser['repo_strd'] )
                    else :
                        scoreDict['repo_strd'] = 0.
                    # Organizations List
                    # fraction of common organizations
                    countorgs = 0
                    for mf in dataUser['orgnztn'] :
                        if mf in dataCmpr['orgnztn'] :
                            countorgs += 1.
                    if len( dataUser['orgnztn'] ) > 0 :
                        scoreDict['orgnztn'] = countorgs/len( \
                            dataUser['orgnztn'] )
                    else :
                        scoreDict['orgnztn'] = 0.
                    # Prog. Lang. List
                    # fraction of common lang
                    countLangs = 0
                    for mf in dataUser['lang_used'] :
                        if mf in dataCmpr['lang_used'] :
                            countLangs += 1.
                    if len( dataUser['lang_used'] ) > 0 :
                        scoreDict['lang_used'] = countLangs/len( \
                            dataUser['lang_used'] )
                    else :
                        scoreDict['lang_used'] = 0.
                    # I'm skipping the normalization part for now.
                    currSimilarityScore = 0.
                    for k in scoreDict.keys():
                        currSimilarityScore += ( \
                            scoreDict[k] ) * weightDict[k]
                    # Store the final score in the Rank DF
                self.userRankDF.loc[ind][col] = currSimilarityScore
                print 'ranking...', ind, col, currSimilarityScore
        # Now get a list of the best suggestions and store it into the ranks table
        # for that loop through each of the user info and sort
        for ii in self.userRankDF.index.unique():
            # sort in descending order
            print ' Ranking and Populating database for..', ii
            # Sort using numpy
            vals =self.userRankDF.loc[ii].values
            cols =self.userRankDF.columns
            sortedInds = numpy.argsort( vals )[::-1]
            rankList = cols[sortedInds]
            rankList = rankList[0:31] # current user and top 30
            # Just double checking if the first result is the same user
            if ii != rankList[0] :
                print 'wrong ordering..'
                break
            # populate the database
            self.dbObj.popRankDet(rankList)