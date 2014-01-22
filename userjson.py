# Use this code to call the database, make a json
# this will be used for d3 plotting
import dbmngr
import json

datObj = dbmngr.DbAccess( 'testgit', usr='root' )
userdet = datObj.retD3PlotDet()
userD3Dict = {}
for r in range( len( userdet ) ) :
    userD3Dict[ userdet[r][2] ] = [ userdet[r][0], userdet[r][1] ]

with open('data.txt', 'w') as outfile:
     json.dump(userD3Dict, outfile, sort_keys = True, indent = 4,
ensure_ascii=False)

f = open("test.txt","w")
f.write("Name\t numflwr\t nrepo\n ")
for j in userdet :
    f.write( str( j[2] )+'\t' + str( j[1] )+'\t' + str( j[2] + '\n' ) )

print '---------------JSON------------'

#jsonD3Users = json.dumps( userD3Dict, sort_keys=True )
