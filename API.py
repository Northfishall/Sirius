import tushare as ts
import pandas as pd
import numpy as np
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
    data.to_csv(path_or_buf=Path, sep = ',',na_rep = '',float_format=None, columns=None, header=True, index=None,
                 index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"',
                 line_terminator='\n', chunksize=None, tupleize_cols=None, date_format=None, doublequote=True,
                 escapechar=None, decimal='.')


def readFile(Path):
    df = pd.read_csv(filepath_or_buffer=Path,sep=',')
    return df


def getVolumeType(data):
    return data[['volume','type']]


def getThreeType(data):
    result = {'buy':0,'mid':0,'sale':0}
    # print(type(data))
    for index ,row in data.iterrows():
        # print(row)
        # print(type(row))
        if row['type'] == "买盘":
            result['buy']+=int(row['volume'])
        elif row['type'] == "卖盘":
            result['sale'] += int (row['volume'])
        else:
            result['mid']+=int(row['volume'])
    return result

def Test():
    #data = ts.get_concept_classified()
    data = ts.get_latest_news()
    print(data)

#print(getMainDeal('000333','2020-03-20',500,1))