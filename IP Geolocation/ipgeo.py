"""
@Author: Stavros Gkounis
@alias: wh1t3kn16ht
@Project: IP Geolocation
@Description: This script takes and parse the json object which is return by the RESTful API provided by the website https://tools.keycdn.com/geo, which contains useful information such as ISP, location etc.
@Version: v1.0
"""


import requests

def signature():
  print(" ___________   _____            _                 _   _")
  print("|_   _| ___ \ |  __ \          | |               | | (_)")
  print("  | | | |_/ / | |  \/ ___  ___ | | ___   ___ __ _| |_ _  ___  _ __")
  print("  | | |  __/  | | __ / _ \/ _ \| |/ _ \ / __/ _` | __| |/ _ \| '_ \ ")
  print(" _| |_| |     | |_\ \  __/ (_) | | (_) | (_| (_| | |_| | (_) | | | |")
  print(" \___/\_|      \____/\___|\___/|_|\___/ \___\__,_|\__|_|\___/|_| |_|")
  print("              written by Stavros Gkounis (wh1t3kn16ht)")


def takeJsonDataForIPAddress(ip_address):
  url = 'https://tools.keycdn.com/geo.json?host=' + ip_address # RESTfull API
  rqst = requests.get(url)
  return rqst.json()

def parseJson(json):
  geolocation_data = json['data']['geo']
  for key in geolocation_data:
    print("  [*] " + key.upper() + ": {}".format(geolocation_data[key]))

if(__name__ == "__main__"):
  signature()
  print('\n')
  ip = input("Give the public IP address: ")
  parseJson(takeJsonDataForIPAddress(ip))
