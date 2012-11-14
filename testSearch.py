import search as s

print 'Testing search on just name'
print s.getList('assassin', 'name') 
print '\n'
print 'testing with halo and image'
game = s.getList('halo', 'name', 'id', 'image') 
print game
print '\n'
id = game['Halo Wars']['id']
print game.keys()
print 'accessing the search result \'Halo Zero\' to get id=' + id 
print '\n'
print 'Using Id to test get game details'
print s.getGameDetsById(id, 'name', 'id', 'original_release_date', 'deck' )
id = '123215431464257'
print s.getGameDetsById(id, 'name', 'id', 'original_release_date', 'deck' )


