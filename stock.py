import scraping as sc
import pandas as pd
import numpy as np

class Stock(object):
    def __init__(self,sto):
        self.code = sto[0]
        self.name = sto[1]
        self.industry = sto[2]
        self.keyNum = sc.getKeyNumFromCode(self.code)
        self.keyNum = self.keyNum.convert_objects(convert_numeric=True)
        Financials = sc.getFinancialsFromCode(self.code)
        self.reporting = Financials.iloc[1,1:]
        Financials2 = pd.DataFrame(np.asarray(Financials.iloc[2:,1:]))
        Financials2 = Financials2.convert_objects(convert_numeric=True)
        Financials2.index = Financials.iloc[2:,0]
        Financials2.columns = Financials.iloc[0,1:]
        self.Financials = Financials2

    def addKeyNums(self):
        means = self.Financials.mean(1)
        PE5 =  self.keyNum.iloc[2,0] / means[-1]
        toAdd = pd.DataFrame([PE5],index=["PE5"])
        self.keyNum = self.keyNum.append(toAdd)
        return
        
        
