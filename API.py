import tushare as ts
import pandas as pd
import numpy as np
import os
import time
import datetime
#ts.set_token('')
'''
获取某个股票的在date中过的成交手为vol以上的大单信息
'''
def getMainDeal(code,date,vol,pause):
    result = ts.get_sina_dd(code,date=date,vol=vol,pause=pause)
    return result



'''
path_or_buf 保存的文件路径
sep : 输出文件的字段分隔符，默认为 “,”
na_rep : 用于替换空数据的字符串，默认为''
float_format : 设置浮点数的格式（几位小数点）
columns : 要写的列
header : 是否保存列名，默认为 True ，保存
index : 是否保存索引，默认为 True ，保存
index_label : 索引的列标签名
'''
def saveFile(Path,data):
    data.to_csv(path_or_buf=Path, sep = ',',na_rep = 'NA',float_format=None, columns=None, header=True, index=None,
                 index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"',
                 line_terminator='\n',  decimal='.')

'''
读取csv文件
'''
def readFile(Path):
    df = pd.read_csv(filepath_or_buffer=Path,sep=',')
    return df

'''
对Pandasform 文件提取两列 
volume 和 type
'''
def getVolumeType(data):
    return data[['volume','type']]


'''
对输入数据中的
买盘、卖盘、中性盘进行统计
返回字典
'''
def getThreeType(data):
    result = {'buy':0,'mid':0,'sale':0}
    # print(type(data))
    for index ,row in data.iterrows():
        if row['type'] == "买盘":
            result['buy']+=int(row['volume'])
        elif row['type'] == "卖盘":
            result['sale'] += int (row['volume'])
        else:
            result['mid']+=int(row['volume'])
    return result

'''
输入天数Days
返回当天开始的Days天的日期 
数据格式为"2020-04-11"
'''
def getDateList(Days):
    if Days < 0:
        return "error input"
    limit = Days
    i = 0
    dateList = []
    while (i<limit):
        date = datetime.date.today() - datetime.timedelta(days = i)
        if date.weekday() == 6 or date.weekday() == 5:
            i+=1
            limit+=1
            continue
        dateList.append(date)
        i+=1
    return dateList


'''
根据查找前N天的数据
并且保存
'''
def getNdayResult(code,N,vol,pause):
    if N < 0:
        return "error input"
    dateList = getDateList(N)
    for date in dateList:
        filePath = "./" + str(code)+"_"
        filePath += str(date) + ".csv"
        result = getMainDeal(code,date,vol,pause)
        if result is None:
            continue
        saveFile(filePath,result)
        time.sleep(10)

'''
获取今天的数据
'''
def getToday():
    filePath = "./data/today.csv"
    saveFile(filePath,ts.get_today_all())


'''
提取当日涨幅在x以上的code
'''
def getCodeOverX(x):
    data = readFile("./data/today.csv")
    data['code'] = data['code'].astype('str')
    # print(type(data['code']))
    data['code'] = data['code'].str.rjust(6,fillchar="0")
    data = data[data['changepercent']>x]
    saveFile("./data/top.csv",data)
    print(data['code'].shape[0])
    # print(data['code'])



'''
查找机构盘
逻辑为 连续多波中单
'''
def SearchAgenc():
    data = readFile('./data/top.csv')
    code_list = []
    for code in data['code']:
        code = str(code).rjust(6,"0")
        code_list.append(code)
    date = getDateList(2)[1]
    for code in code_list:
        print("code is :"+str(code))
        result = getMainDeal(str(code),date,90,1)
        if result is None:
            continue
        path = "./data/MainDeal"+str(code)+".csv"
        print("result is :",result)
        print("Type:",type(result))
        saveFile(path,result)
        result_sell = result[result['type']=="卖盘"]
        result_buy = result[result['type']=="买盘"]
        result_med = result[result['type']=="中性盘"]
        # for row in result_sell:

def Search_local():
    for root, dirs, files in os.walk(r'./data/MainDeal/'):
        for file in files:
            path = os.path.join(root,file)
            data = readFile(path)
            # print(data)
            data['time'] = pd.to_datetime(data['time'])
            print(data['time'][0])
            print((data['time'][0]-data['time'][1]).seconds)
            result = pd.DataFrame(columns=['code','name','time','price','volume','preprice','type'])
            data_temp = data.copy()
            #axis = 1 表示按行 axis = 0 表示按列
            data_temp['next_time'] = data_temp.groupby('code')['time'].apply(lambda i:i.shift(1))
            data_temp['diff'] = data_temp.apply(lambda x:(x['next_time'] - x['time']).seconds , axis = 1)
            print(data_temp)
            # data_temp['diff'] = pd.to_datetime(data_temp['diff'])
            # data_temp['diff'] = data_temp['diff'].seconds

            # print(data_temp)

            # for index in range(data.shape[0]-1):
            #     diff_time = (data['time'][index]-data['time'][index+1]).seconds
            #     if diff_time<70:
            #         if data[index]['volume']>10000 and data[index]['volume']<30000 and \
            #                 data[index+1]['volume']>10000 and data[index+1]['volume']<30000:
            #             flag = 1


            return







#getToday()
# getCodeOverX(9.5)
# SearchAgenc()
Search_local()