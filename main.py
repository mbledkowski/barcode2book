# by github.com/mmble
# using external library - requests | to install use >pip install requests
import os
import re
import json
import requests


def printdata(type, data):
  if type == "authors":
    datastring = ""
    for i in range(0, len(data)):
      if i == len(data)-1:
        datastring += data[i]
      else:
        datastring += data[i] + ", "
    if len(data) > 1:
      print("Authors: " + datastring)
    elif len(data) == 1:
      print("Authors: " + datastring)
    else:
      print("No informations about author/s are available :/")
  elif type == "title":
    print("Title: "+data[0]+" - "+data[1])
  elif type == "publishing":
    print("Published by "+data[0]+" in "+data[1])


while True:
  getinput = input()
  if re.search(r'^\d{13}$', getinput):
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + getinput)
    if response.status_code != 200:
      print("Error: "+response.status_code)
    else:
      getjson = response.json()
      if getjson["totalItems"] != 1:
        if getjson["totalItems"] == 0:
          print("This item do not exist in Google Books database :(")
        else:
          print("Error: there is more than one book.")
      else:
        booksinfoitems = getjson["items"][0]
        printdata("title", [booksinfoitems["volumeInfo"]["title"], booksinfoitems["volumeInfo"]["subtitle"]])
        printdata("authors", booksinfoitems["volumeInfo"]["authors"])
        printdata("publishing", [booksinfoitems["volumeInfo"]["title"], booksinfoitems["volumeInfo"]["subtitle"]])
  else:
    os.system(getinput)