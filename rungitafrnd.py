from flask import Flask, render_template, request
import MySQLdb
import json
app = Flask(__name__)

db = MySQLdb.connect( user='root', host='localhost', port=3306, db='gituserinfo' )

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/dataUser")
#, userDict=userD3List
def dataUser():
    # Query the database for some initial stuff
    queryMainGraph = """
            SELECT userdetail.nflwr, count(repocontr.login), repocontr.login
            FROM repocontr JOIN userdetail 
            ON repocontr.login=userdetail.login 
            GROUP BY repocontr.login;
            """
    db.query( queryMainGraph )
    userSmryRet = db.store_result().fetch_row( maxrows=0 )
    # print userSmryRet
    userdet = [ s for s in userSmryRet ]

    return json.dumps( [ { 'login': userdet[r][2], 'nflwrs':userdet[r][0], 'nrepos':userdet[r][1] }
         for r in range( len( userdet ) ) ] )

@app.route("/userpage")
def userpage():
    loginId = request.args.get('loginInput')
    # get the top 10 results
    queryStr = "select * from gitranks where login='"+loginId+"' limit 10;"
    db.query( queryStr )
    query_results = db.store_result().fetch_row( maxrows=0 )
    userlist = ""
    count = 0
    userlist = []
    for result in query_results[0] :
        if json.dumps(result) == '"'+loginId+'"' :
            continue
        # do some filtering to remove the "" marks around user name
        userlist.append( json.dumps(result)[1:-1] )
    # We have the list of suggested friends now
    # get the details of each suggestion
    nameUserList = []
    startDateUserList =[]
    nFlwrUserList =[]
    # loop through each user and collect the details
    for uu in userlist :
        qryStr = "select name, start_date, nflwr from userdetail where login='"+uu+"';"
        db.query( qryStr )
        query_results = db.store_result().fetch_row( maxrows=0 )
        nameUserList.append( query_results[0][0].decode('utf-8') )
        print query_results[0][0]
        # convert the datetime format to an appropriate format
        startDateUserList.append( query_results[0][1].strftime('%m/%d/%Y') )
        nFlwrUserList.append( query_results[0][2] )

    return render_template( 'users.html', gitfriends=userlist, userid=loginId,\
    nameList=nameUserList, startdateList=startDateUserList, nFlwrList=nFlwrUserList )

@app.route("/getFrndDet/<frndid>/<userid>")
def getFrndDet( frndid=None, userid=None ):
    userid = userid
    frndid = frndid
    # For querying purposes we need to put "" around userid
    # since they are not present by default
    userid = '"' + userid + '"'
    frndid = '"' + frndid + '"'
    # Now we need to query the tables in the database to 
    # to return the common stuff between the user and the friend
    # userdetail table -- for common organizations
    # this is a bit different since we stored stuff as a string
    # so we get individual results and find common orgs
    queryStrOrgsUser = "select orgnztn from userdetail where login="+userid+";"
    queryStrOrgsFrnd = "select orgnztn from userdetail where login="+frndid+";"
    db.query( queryStrOrgsUser )
    query_results_user = db.store_result().fetch_row( maxrows=0 )
    userOrgList = []
    # query_results_user = json.loads( query_results_user )
    for result in json.loads( query_results_user[0][0] ) :
        userOrgList.append( result )
    # get the frnds organizations
    db.query( queryStrOrgsFrnd )
    query_results_user = db.store_result().fetch_row( maxrows=0 )
    frndOrgList = []
    for result in json.loads( query_results_user[0][0] ) :
        frndOrgList.append(result)
    # Now get the common Orgs (if any)
    commonOrgList = []
    for uo in userOrgList :
        if uo in frndOrgList :
            commonOrgList.append( str(uo) )
    if len( commonOrgList ) == 0:
        commonOrgList = [None]
    # Now get the follower list
    qryStr = 'select user1.flwrlogin from follower user1 join follower user2 on user2.login='\
     + frndid + ' and user1.flwrlogin = user2.flwrlogin where user1.login= '+userid;
    db.query( qryStr )
    query_results = db.store_result().fetch_row( maxrows=0 )
    commonFlwrList = []
    for result in query_results :
        commonFlwrList.append( result[0] )
    if len( commonFlwrList ) == 0:
        commonFlwrList = [None]
    # Now get the list of people both follow
    qryStr = 'select user1.flnglogin from following user1 join following user2 on user2.login='\
     + frndid + ' and user1.flnglogin = user2.flnglogin where user1.login= '+userid;
    db.query( qryStr )
    query_results = db.store_result().fetch_row( maxrows=0 )
    commonFlngList = []
    for result in query_results :
        commonFlngList.append( result[0] )
    if len( commonFlngList ) == 0:
        commonFlngList = [None]
    # Now get the common proglangs list
    qryStr = 'select user1.langused from proglang user1 join proglang user2 on user2.login='\
     + frndid + ' and user1.langused = user2.langused where user1.login= '+userid;
    db.query( qryStr )
    query_results = db.store_result().fetch_row( maxrows=0 )
    commonProgLangList = []
    for result in query_results :
        commonProgLangList.append( result[0] )
    if len( commonProgLangList ) == 0:
        commonProgLangList = [None]
    # Now get the common repos contr to list
    qryStr = 'select user1.repocntrbtd from repocontr user1 join repocontr user2 on user2.login='\
     + frndid + ' and user1.repocntrbtd = user2.repocntrbtd where user1.login= '+userid;
    db.query( qryStr )
    query_results = db.store_result().fetch_row( maxrows=0 )
    commonRepoContrList = []
    for result in query_results :
        commonRepoContrList.append( result[0] )
    if len( commonRepoContrList ) == 0:
        commonRepoContrList = [None]
    # Now get the common repos starred to list
    qryStr = 'select user1.repostrd from repostarred user1 join repostarred user2 on user2.login='\
     + frndid + ' and user1.repostrd = user2.repostrd where user1.login= '+userid;
    db.query( qryStr )
    query_results = db.store_result().fetch_row( maxrows=0 )
    commonRepoStrdList = []
    for result in query_results :
        commonRepoStrdList.append( result[0] )
    if len( commonRepoStrdList ) == 0:
        commonRepoStrdList = [None]
    # pass the lists to the html file
    return render_template( 'frndy.html', orgl=commonOrgList, \
        cfwl=commonFlwrList, crcl=commonRepoContrList, \
        crsl=commonRepoStrdList, cfnl=commonFlngList, cpll=commonProgLangList )


@app.route("/<pagename>")
def regularpage( pagename=None ):
    """
    if route not found
    """
    return "No such page as " + pagename + " please go back!!! "


if __name__ == "__main__":
    app.debug=True
    app.run()