from lxml import html
import pandas as pd
import requests
from lxml import etree
import math
import csv
##pd.set_option('max_columns', 50)

listShares = list()
listCodes = list()
listSectors = list()
listSectorsExtd = list()
with open('D:\Programmation\Python\Scrapping\listCompanies.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        listShares.append(row)
        listCodes.append(row[0])
        listSectorsExtd.append(row[2])
        if row[2] not in listSectors:
            listSectors.append(row[2])

webSitePath = 'http://shares.telegraph.co.uk/fundamentals/?epic='

def printXml(element):
    print(etree.tostring(element, pretty_print=True))

def getKeyNum(element):
    listName = list()
    listValue = list()
    for elem in element:
        listName.append(elem[0].text)
        listName.append(elem[2].text)
        listValue.append(elem[1].text.replace(",",""))
        listValue.append(elem[3].text.replace(",",""))
    result = pd.DataFrame(listValue,index = listName)
    return result

def getFinancials(element):
    listName = list()
    listValue = list()
    for elem in element:
        listName.append(elem[0].text)
        listName.append(elem[2].text)
        listValue.append(elem[1].text.replace(",",""))
        listValue.append(elem[3].text.replace(",",""))
    result = pd.DataFrame(listValue,index = listName)
    return result

def get_all_text( node, liste = list() ):
        if len(node) ==  0:
            if node.text is None or len(node.text.strip(' \n\t')) == 0:
                return
            liste.append(node.text.strip(' \n\t').replace(",",""))
            return
        else:
            for child_node in node:
                if len(node.text.strip(' \n\t').replace(",","")) > 0:
                    liste.append(node.text.strip(' \n\t').replace(",",""))
                get_all_text( child_node , liste)
            return liste

def createDataframe(liste, ncol=6):
    numIter = int(math.floor(len(liste) / ncol))
    for i in range(numIter):
        if i == 0:
            res = pd.DataFrame(liste[ncol*i:ncol*(i+1)])
            res = res.T
        else:
            newRes = pd.DataFrame(liste[ncol*i:ncol*(i+1)])
            newRes = newRes.T
            res = res.append(newRes,ignore_index=True)
    return res

def getKeyNumFromCode(code):
    page = requests.get(webSitePath + code)
    tree = html.fromstring(page.text)
    table = tree.xpath('//div[@id="TPContainer"]')
    tableXml = html.fromstring(etree.tostring(table[0]))
    keyNum = tableXml[9]
    keyNum = getKeyNum(keyNum)
    return keyNum

def getFinancialsFromCode(code):
    page = requests.get(webSitePath + code)
    tree = html.fromstring(page.text)
    table = tree.xpath('//div[@id="TPContainer"]')
    tableXml = html.fromstring(etree.tostring(table[0]))
    Financials = tableXml[21]
    Financials = get_all_text(Financials)
    Financials = createDataframe(Financials)
    return Financials

## SAB, NICL, CGG
##
##page = requests.get('http://shares.telegraph.co.uk/fundamentals/?epic=RBS')
##tree = html.fromstring(page.text)
##table = tree.xpath('//div[@id="TPContainer"]')
##tableXml = html.fromstring(etree.tostring(table[0]))
##keyNum = tableXml[9]
##Financials = tableXml[21]
##keyNum = getKeyNum(keyNum)
##Financials = get_all_text(Financials)
##Financials = createDataframe(Financials)

##print keyNum
##print Financials.to_string()

