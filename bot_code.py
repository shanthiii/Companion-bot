import asyncio
import discord
import os
#The OS module in Python provides functions for interacting with the operating system
import requests
#The requests module allows you to send HTTP requests using Python.
#The HTTP request returns a Response Object with all the response data
import json
#JSON stands for JavaScript Object Notation. JSON is a lightweight format for storing and transporting data. JSON is often used when data is sent from a server to a web page.
from PyDictionary import PyDictionary
from youtube_search import YoutubeSearch
#python3 -m pip install googlesearch-python
from googlesearch import search



client = discord.Client() #This client is our connection to Discord.
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+"--"+json_data[0]['a']
  return(quote)

def youtube_link(terms):
  res = YoutubeSearch(terms, max_results=5).to_dict()
  return res
def google_link(terms):
  res=search(terms, num_results=5)
  return res
def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/jokes/general/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['setup']+"\n"+json_data[0]['punchline']
  return(quote)
def joke():
  response = requests.get("https://official-joke-api.appspot.com/jokes/programming/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['setup']+"\n"+json_data[0]['punchline']
  return(quote)

def cont(sitee):
  response = requests.get('https://kontests.net/api/v1/all')
  #for i in response:
  res = []
  #print(response)
  json_data = json.loads(response.text)
  u = (len(json_data))
  for x in range(u):
    y = (json_data[x]['site'])
    if sitee == y:
      res.append(json_data[x])
  #print(res, len(res))
  return res

@client.event
async def on_ready():
 print('We have logged in as {0.user}'.format(client))
#We then use the Client.event() decorator to register an event. This library has many events. Since this library is asynchronous, we do things in a “callback” style manner.
#A callback is essentially a function that is called when something happens. In our case, the on_ready() event is called when the bot has finished logging in and setting things up and the on_message() event is called when the bot has received a message.
@client.event
async def on_message(message):
  if message.author==client.user:
    return
  if message.content.startswith('$Hello'):
    await message.channel.send('Hello!')
  if message.content.startswith('$inspire me'):
    quote=get_quote()
    await message.channel.send(quote)
  if message.content.startswith('$joke'):
    joke=get_joke()
    await message.channel.send(joke)
  if message.content.startswith('$jokegeek'):
    geek=joke()
    await message.channel.send(geek)
  if message.content.startswith('$mean'):
    mean = message.content.split("$mean ",1)[1]
    dictionary = PyDictionary()
    word = dictionary.meaning(mean)
    await message.channel.send(word)
    word1= dictionary.synonym(mean)
    await message.channel.send(word1)
    word2= dictionary.antonym(mean)
    await message.channel.send(word2)
  if message.content.startswith('$gsearch'):
    x = message.content.split('$gsearch' ,1)[1]
    results = google_link(x)
    for i in results:
      await message.channel.send(i)
  if message.content.startswith('$questions'):
    x = message.content.split('$questions' ,1)[1]
    results = google_link("practice questions on" + x)
    for i in results:
      await message.channel.send(i)
  if message.content.startswith('$search'):
    x = message.content.split('$search' ,1)[1]
    results = youtube_link(x)
    for i in range(0,len(results)):
      y = results[i]['url_suffix']
      await message.channel.send(str(i+1) + ' https://www.youtube.com' + y)

  if message.content.startswith('$remind '):
    """start with $remind and 
    then 3/2 letter word 
    like sec, min, hr followed by time with a number
    syntax: !sleep sec 5
    then followed by the reminder keyword/task"""
    result = ""
    tim = message.content.split(" ")
    if(tim[1] == 'sec'):
      x = int(tim[2])
    elif tim[1] == 'min':
      x = 60*int(tim[2])
    elif tim[1] == 'hr':
      x = 3600*int(tim[2])
    
    #know = message.content.split(tim[1] , 1)[2]
    #print(know)
    await asyncio.sleep(int(x))
    for i in tim[3:]:
      #print(i)
      result = result + " " + i 
      #re = "\033" +  " a_string " + "\033"
    await message.channel.send( "REMINDER: " + result)
  
  if message.content.startswith('$contests '):
    site_name = message.content.split('$contests ', 1)[1]
    con = cont(site_name)
    #j = 0
    for i in con:    
      #await(i[0])
      for j in i:
        await message.channel.send(j + " : " + i[j])
      #await message.channel.send(i[0] + ":" + i['url'])
      #await message.channel.send(`\n`)
      # quo = "\n"
      await message.channel.send("----------------------")
     #await message.channel.send(i)


client.run(os.getenv('TOKEN'))
