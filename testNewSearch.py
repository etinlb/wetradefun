import newSearch as s
data = s.getList('assassin', 'name', 'id', 'image', 'genres', 'platforms') 
for x in data:
  print x['name']
  print x['image']
  print x['platforms']
  print x['genres']

data = s.getGameDetsById('7004','name', 'genres', 'platforms', 'deck', 'image')
print data['name']
print data['genres']
print data['platforms']
print data['image']
# he view will give you a dictionary with the value game name, 
# image url, deck(short discription of game), genres, platforms, 
# url to game page on Giantbomb, and current number of listings. 
# Display them these as you see fit. 