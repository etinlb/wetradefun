"""
Module that currently holds all of the search functions 
"""

import urllib2 #open urls
import xml.etree.ElementTree as ET #parse xml

#api_key is needed for access to the GB database
api_key = '?api_key=308d89c435a454c3943316fb25c73ceba1f8bf72'
searchStart = 'http://api.giantbomb.com/search/' + api_key 
specificGame = 'http://api.giantbomb.com/game/' 


def getList(searchQuery, *params):
  """ Returns a nested dictionary based on the string passed in as searchQuery
  currently the outer dictionary uses the game name as a key and the inner uses
  the param associated with it as a key.

  params is a varible arugment of strings that are used to filter the resutls.
  what can be used as a param
  'name' : the name of the game
  'original_release_date' : when the game came out
  'aliases' : what else the games are know as
  'deck' : a short discription of the game
  'id' : the  games id
  'platform' : not implemented yet
  'image' : for now it returns multiple image urls.

  example
    x = getList('halo', 'name', 'id')
    x.keys() #prints out all the keys
    y = x['Halo 4'] #gets the nested halo 4 dict
    y['id'] #gets the id of Halo 4
    x['Halo 4']['id'] #access inner dictionary id value

  """
  #makes the params entered in the proper filter format
  filters = buildFilterStr(params)
  searchString = searchStart + '&resources=game&query='+ searchQuery + filters + '&limit=10'

  #queries the video game database
  file = urllib2.urlopen(searchString)
  #make the dictionary
  gameList = parseFields(file, params)

  return gameList

def getGameDetsById(gameId, *params):
  """ returns a dict with the details on a specific game
  gameId is the id of the game you want details on
  params is a varible arugment of strings that are used to filter the resutls.
  what can be used as a param
  
  'name' : the name of the game
  'original_release_date' : when the game came out
  'aliases' : what else the games are know as
  'deck' : a short discription of the game
  'id' : the  games id
  'platform' : not implemented yet
  'image' : for now it returns multiple image urls.
  example
    x = getGameDetsById(2600)
    x['name'] #returns the game's name
    x['image'] #return a urls of the main image 
  """
  filters = buildFilterStr(params)
  searchString = specificGame + gameId +'/' + api_key + filters

  file = urllib2.urlopen(searchString)  
  game = parseFieldsSpecific(file)
  return game

def parseFields(file, params):
  """ parses the xml file for search query and returns a nested dict 
  It uses the name of the game as the outter dict key. If no 'name' tag is found
  it uses the games id as a key.

  """

  data = file.read()
  root = ET.fromstring(data)
  if checkXml(root) != 1:
    return None # check if the xml is good
  resNode = root.find('results') # get the node with the game data
  
  
  mainDict = {}
  innerDict = {}
  grandKey = ''
  #Loop over the game nodes 
  for gameNode in resNode:
    
    #get the specified parameters and add them to the inner dict
    for y in params:
      if y == 'name': # for names = key
        grandKey = gameNode.find(y).text

      else: # for any non-name = value pair
        if y == 'platform':
          searchPlatform = specificGame + gameNode.find('id').text + '/' + api_key + '&field_list=platforms'
          # print searchPlatform
          file = urllib2.urlopen(searchPlatform)
          data2 = file.read()
          root2 = ET.fromstring(data2)
          if checkXml(root2) != 1:
            return None # check if the xml is good
          resNode2 = root2.find('results') # get the node with the game data
          resNodeDeep = resNode2.find('platforms')

          allplatforms = ""
          for moreNodes in resNodeDeep:
            resNodeDeeper = resNodeDeep.find('platform')
            allplatforms += moreNodes.find('name').text + ", "
          innerDict[y] = allplatforms

          
        elif y == 'image':
          resNodeImage = gameNode.find('image')
          innerDict[y] = resNodeImage.find('icon_url').text
        
        else:

          # print gameNode.find(y).text
          innerDict[gameNode.find(y).tag] = gameNode.find(y).text

    #no name node was found
    if  grandKey == '':
      mainDict[innerDict['id']] = innerDict
    else:

      mainDict[grandKey] = innerDict
    innerDict = {}  
  return mainDict  

def parseFieldsSpecific(file):
  """ Parses the xml sheet for one 
  returns a dict with each node's tag as a key.
  If the xml sheet is bad or empty, it returns none

  """
  data = file.read()
  root = ET.fromstring(data)
  if checkXml(root) != 1: # check if the xml is good
    return None
  resNode = root.find('results')
  gameDict = {}
  for child in resNode:
    gameDict[child.tag] = child.text
  return gameDict  

def checkXml(dataRoot):
  """checks the meta data of the xml sheet
  returns -1 if there was a problem with the query
  returns 0 if there was no search results found
  returns 1 if the xml sheet is fine
  """
  if dataRoot.find('status_code').text != '1':
    #error_message = dataRoot.find('error').text
    return -1
  elif dataRoot.find('number_of_page_results').text == '0':
    return 0
  else: 
    return 1

def buildFilterStr(params):
  """converts the parmas passed in to the syntax of the GB database query
  """
  filters = '&field_list='
  for x in params:
    filters += x + ','

  return filters  




