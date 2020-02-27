import tushare as ts

def Test():
    data = ts.get_concept_classified()
    print(data)

Test()