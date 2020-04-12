import numpy as np
import pandas as pd
import API

PATH_Save = './'
csv = ".csv"
code = '000158'
date = '2020-03-27'
vol = 500
pause = 1

file_path = PATH_Save + code + csv
print(file_path)
# main_deal = API.getMainDeal(code,date=date,vol=vol,pause=pause)
# API.saveFile(file_path,main_deal)
main_deal = API.readFile(file_path)
# print(main_deal)
# print(main_deal.columns)
# volumeType = API.getVolumeType(main_deal)
# print(volumeType)
# result = API.getThreeType(volumeType)
# print(result)
# dates = API.getDateList(7)
# print(dates)
# API.getNdayResult("000158",5,500,1)
# result = API.getMainDeal("000158","2020-04-06",500,1)
# print("get")
# print(type(result))
