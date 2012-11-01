#http://api.giantbomb.com/characters/?api_key=308d89c435a454c3943316fb25c73ceba1f8bf72&gender=M&sort=birth_date&format=xml
#I have no idea what this will be doing but something along the lines of requesting
#a list from giantbomb then parsing the xml. This is mainly for educational 
#purposes but I hope it preforms welll enough so we can use.

#so to request the database, pass in api key(it was long so I put it in it's own
#varible) and then append filtes to it. The filters have a format of 
#&filter=what_field_you_want_filtered_by
#list of usefull filters
#field_list
#limit, the maximum amount of games 
#list of useful feilds
#aliases = other names that the name goes by
#descritpion = a discription of the game WARNING VERY LARGE
#id = unique id to game, may want to mimic it in our database for ease
#image = main image of the game
#resource, only available in search, specify what we want, will always be games
#or game
#query = what you want to search for. THere is a litmitation in that this need to be 
#as close as possible to real a game, doesn't work well with partial names

#example url to search the games "resource" for anything called halo and display only
#the name of the query
#http://api.giantbomb.com/search/?api_key=308d89c435a454c3943316fb25c73ceba1f8bf72\
#&resources=game&field_list=name&format=xml&limit=10&query=halo
import urllib2
#import pdb
#from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET


api_key = '?api_key=308d89c435a454c3943316fb25c73ceba1f8bf72'
searchStart = 'http://api.giantbomb.com/search/' + api_key
specificGame = 'http://api.giantbomb.com/game/' 

def getList(searchQuery, *params):
  filters = buildFilterStr(params) #'&field_list='
  # for x in params:
  #   filters += x + ','
  searchString = searchStart + '&query='+ searchQuery +'&resources=game' +filters+'limit=10'
  file = urllib2.urlopen(searchString)
  gameList = parseFields(file, params)
  return gameList

# def parseXml(file, fields):
#   data = file.read()
#   root = ET.fromstring(data)
#   x = root.find('results')
#   gameList = parseFields(x, fields);
#   print gameList


def parseFields(file, fields):
  data = file.read()
  root = ET.fromstring(data)
  resNode = root.find('results')
  mainDict = {}
  innerDict = {}
  for gameNode in resNode:
    for y in fields:
      if gameNode.find(y).tag == 'name':
        grandKey = gameNode.find(y).text
      else:
        key = gameNode.find(y).tag;
        text = gameNode.find(y).text# + ' '
        innerDict[key] = text
    mainDict[grandKey] = innerDict
    innerDict = {}  
  return mainDict  

def parseFieldsSpec(file, fields):
  data = file.read()
  print data
  root = ET.fromstring(data)
  resNode = root.find('results')
  print resNode
  for child in resNode:
    print child.tag



# def getGameDetsByName(name, *params):

def buildFilterStr(params):
  filters = '&field_list='
  for x in params:
    filters += x + ','
  return filters  


#   searchString = api_key_specific +'&name=' + name 
#   file = urllib2.urlopen(searchString)

#   return node.text

def getGameDetsById(gameId, *params):
  filters = buildFilterStr(params)
  searchString = specificGame + gameId +'/' + api_key + filters
  file = urllib2.urlopen(searchString)  
  game = parseFieldsSpec(file, params)
  return game




  # x = root.find('game')
  # print x.atrib
  # print x.tag
  # file.close
  #dom = parseString(data)

  # xmlData = ''
  # for node in dom.getElementsByTagName('game'):
  #   print node.getAttribute('name')
  # x = ET.Element('results')  
  # xmlData = ''
  # for x in xrange(0,10):
  #   xmlData += dom.getElementsByTagName('name')[x].firstChild.data + '\n'
  # print xmlData
  
