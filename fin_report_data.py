
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date


def get_financial_report(ticker):

    # try:
    urlfinancials = 'https://www.marketwatch.com/investing/stock/'+ticker+'/financials'
    urlbalancesheet = 'https://www.marketwatch.com/investing/stock/'+ticker+'/financials/balance-sheet'

    text_soup_financials = BeautifulSoup(requests.get(urlfinancials).text,"html") #read in
    text_soup_balancesheet = BeautifulSoup(requests.get(urlbalancesheet).text,"html") #read in


    # build lists for Income statement
    titlesfinancials = text_soup_financials.findAll('td', {'class': 'rowTitle'})
    epslist=[]
    netincomelist = []
    longtermdebtlist = [] 
    interestexpenselist = []
    ebitdalist= []

    for title in titlesfinancials:
        if 'EPS (Basic)' in title.text:
            epslist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'Net Income' in title.text:
            netincomelist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'Interest Expense' in title.text:
            interestexpenselist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'EBITDA' in title.text:
            ebitdalist.append ([td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])


    # find the table headers for the Balance sheet
    titlesbalancesheet = text_soup_balancesheet.findAll('td', {'class': 'rowTitle'})
    equitylist=[]
    for title in titlesbalancesheet:
        if 'Total Shareholders\' Equity' in title.text:
            equitylist.append( [td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])
        if 'Long-Term Debt' in title.text:
            longtermdebtlist.append( [td.text for td in title.findNextSiblings(attrs={'class': 'valueCell'}) if td.text])

    #get the data from the income statement lists 
    #use helper function get_element
    eps = get_element(epslist,0)
    epsGrowth = get_element(epslist,1)
    netIncome = get_element(netincomelist,0)
    shareholderEquity = get_element(equitylist,0)
    roa = get_element(equitylist,1)

    longtermDebt = get_element(longtermdebtlist,0)
    interestExpense =  get_element(interestexpenselist,0)
    ebitda = get_element(ebitdalist,0)

    # load all the data into dataframe 
    fin_df= pd.DataFrame({'eps': eps,'eps Growth': epsGrowth,'net Income': netIncome,'shareholder Equity': shareholderEquity,'roa': 
                  roa,'longterm Debt': longtermDebt,'interest Expense': interestExpense,'ebitda': ebitda},index=range(date.today().year-5,date.today().year))
    
    fin_df.reset_index(inplace=True)
    
    return fin_df



def get_element(list,element):
    try:
        return list[element]
    except:
        return '-'




