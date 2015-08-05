import scraping as sc
import stock as st
import pandas as pd
import numpy as np

code = sc.listShares[1]
test = st.Stock(code)
##print(test.name)
##print(test.code)
##print(test.industry)
##print(test.keyNum)
##print(test.Financials)
##test.addKeyNums()
##print(test.keyNum)

for industry in sc.listSectors:
    idx = [i for i,x in enumerate(sc.listSectorsExtd) if x == industry]
    result = pd.DataFrame()
    for elem in sc.listShares[min(idx):(max(idx)+1)]:
        sto = st.Stock(elem)
        print(sto.code)
        sto.addKeyNums()
        if len(result) == 0 :
            result = pd.DataFrame(sto.keyNum.values,columns=[sto.code])
        else:
            result[sto.code] = sto.keyNum.values
        result.index = sto.keyNum.index

    result.to_csv(industry+".csv")
