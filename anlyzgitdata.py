import dbmngr
import json
import datetime
import pandas
import dbmngr

class LoadGitUserDB(object):
    """ Code to retreive the data from the gituserinfo database
        then analyze it and make the recommendations

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
        self.userDataFrame

    def rankUsers( self ):
        """In this part we use the user DataFrame from loadData
           and rank them and store it in a seperate DataFrame
           for later use
        """
        # create a new DataFrame which has user logins as index and columns
        # this we'll use to keep a track of ranks
        self.userScoreDF = pandas.DataFrame( index=self.userLoginList,\
         columns=self.userLoginList )
        # Use a weights dictionary to weigh categories
        weightDict = {}
        weightDict['num_days'] = 0.8
        weightDict['num_flwrs'] = 0.8
        weightDict['flwr_list'] = 2.
        weightDict['num_flwng'] = 0.5
        weightDict['flng_list'] = 1.25
        weightDict['repo_cntr'] = 2.
        weightDict['repo_strd'] = 1.25
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
        print ' calculating scores..'
        for ind in self.userDataFrame.index.unique():
            for col in self.userDataFrame.index.unique():
                dataUser = self.userDataFrame.ix[ind]
                dataCmpr = self.userDataFrame.ix[col]
                print 'scoring...', ind, col
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

                self.userScoreDF.loc[ind][col] = scoreDict
        # We have the dict with different stuff, we need to get ranks now
        # We now need to loop through stuff and  get a final score.
        # make sure the normalization matrix has no zeros
        for j in self.normDict.keys():
            if self.normDict[j] == 0. :
                self.normDict[j] = 1
        # A DF to keep track of the final scores and probably sort them later
        self.userRankDF = pandas.DataFrame( index=self.userLoginList,\
         columns=self.userLoginList )
        # now simply get sum of normalized scores*weight for each category
        print ' calculating ranks..'
        for bb in self.userScoreDF.index.unique():
            for cc in self.userScoreDF.columns:
                currSimilarityScore = 0.
                print 'ranking...', bb, cc
                if bb != cc:
                    # loop through each of the keys in weight/norm dict and calc score
                    for k in self.normDict.keys():
                        currSimilarityScore += ( \
                            self.userScoreDF.loc[bb][cc][k]/self.normDict[k] ) \
                        * weightDict[k]
                # Store the final score in the Rank DF
                self.userRankDF.loc[bb][cc] = currSimilarityScore
        # Now get a list of the best suggestions and store it into the ranks table
        # for that loop through each of the user info and sort
        print ' Ranking and Populating database..'
        for ii in self.userScoreDF.index.unique():
            # sort in descending orde
            print ii
            indsRank = self.userRankDF.sort(ii,ascending=False)
            rankIndex = [ r for r in indsRank.index[0:30] ]
            # include the user login and create an array
            rankList = [ii] + rankIndex
            self.dbObj.popRankDet(rankList)