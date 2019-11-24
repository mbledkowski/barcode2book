# by github.com/mmble
# using external library - requests | to install use >pip install requests
import os
import re
import sys
import json
import requests

# prints given data in the correct way
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
      print("Author: " + datastring)
    else:
      print("No informations about author/s are available :/")
  elif type == "title":
    if len(data) == 2:
      print("Title: "+data[0]+" - "+data[1])
    else:
      print("Title: "+data[0])
  elif type == "publishing":
    print("Published by "+data[0]+" in "+data[1]+"yr")
  elif type == "others":
    print("Pages: "+str(data[0])+"; Language: "+data[1]+"; Age-rating: "+data[2]+"; Public domain: "+str(data[3]))

try:
  while True:
    # TODO - save the api response to file for some time, if book was checked before read data from that file
    getinput = input('Barcode scanner\n$ ')
    if re.search(r'^\d{13}$', getinput):
      try:
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + getinput)
      except:
        print("There is problem with internet connection.\nPlz try again later.")
        continue
      # check what is the https status
      if response.status_code != 200:
        print("Error: "+str(response.status_code))
      else:
        getjson = response.json()
        # check if there is only one item
        if getjson["totalItems"] != 1:
          if getjson["totalItems"] == 0:
            print("This item do not exist in Google Books database :(")
          else:
            print("Error: there is more than one book.")
        else:
          booksinfoitems = getjson["items"][0]

          if "title" not in booksinfoitems["volumeInfo"]:
            booksinfoitems["volumeInfo"]["title"] = "Title not found :/"

          if "subtitle" in booksinfoitems["volumeInfo"]:
            printdata("title", [booksinfoitems["volumeInfo"]["title"], booksinfoitems["volumeInfo"]["subtitle"]])
          else:
            printdata("title", [booksinfoitems["volumeInfo"]["title"]])

          # check if authors exists
          if "authors" in booksinfoitems["volumeInfo"]:
            printdata("authors", booksinfoitems["volumeInfo"]["authors"])
          else:
            printdata("authors", [])

          # add element with value "-" if do not exist
          if "publisher" not in booksinfoitems["volumeInfo"]:
            booksinfoitems["volumeInfo"]["publisher"] = "-"
          if "publishedDate" not in booksinfoitems["volumeInfo"]:
            booksinfoitems["volumeInfo"]["publisher"] = "-"

          printdata("publishing", [booksinfoitems["volumeInfo"]["publisher"], booksinfoitems["volumeInfo"]["publishedDate"]])


          if "pageCount" not in booksinfoitems["volumeInfo"]:
            booksinfoitems["volumeInfo"]["pageCount"] = "-"
          if "language" not in booksinfoitems["volumeInfo"]:
            booksinfoitems["volumeInfo"]["language"] = "-"
          if "maturityRating" not in booksinfoitems["volumeInfo"]:
            booksinfoitems["volumeInfo"]["maturityRating"] = "-"
          else: #if maturityRating exists remove "_" and make everything lowercase
            if booksinfoitems["volumeInfo"]["maturityRating"] == "NOT_MATURE":
              booksinfoitems["volumeInfo"]["maturityRating"] = "not mature"
            else:
              booksinfoitems["volumeInfo"]["maturityRating"] = booksinfoitems["volumeInfo"]["maturityRating"].lower()
          if "publicDomain" not in booksinfoitems["accessInfo"]:
            booksinfoitems["accessInfo"]["publicDomain"] = "-"

          printdata("others", [booksinfoitems["volumeInfo"]["pageCount"], booksinfoitems["volumeInfo"]["language"], booksinfoitems["volumeInfo"]["maturityRating"], booksinfoitems["accessInfo"]["publicDomain"]])
    elif getinput == 'exit':
      try:
        sys.exit(0)
      except SystemExit:
        os._exit(0)
    else: #if command is given - execute it
      os.system(getinput)
    print()

except KeyboardInterrupt:
  print('\nInterrupted')
  try:
    sys.exit(0)
  except SystemExit:
    os._exit(0)