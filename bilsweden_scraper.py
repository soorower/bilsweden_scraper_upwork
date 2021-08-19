import pandas as pd                                   
from bs4 import BeautifulSoup as bs              
import requests 
import datetime


def range_scrape():
#     st = '07-2021'
#     en = '07-2021'
    st = input('Starting Month-Year(like, 01-2018): ')
    en = input('End Month-Year(like, 07-2021): ')
    st1 = st.split('-')[0].replace('01','Jan').replace('02','Feb').replace('03','Mar').replace('04','Apr').replace('05','May').replace('06','Jun').replace('07','Jul').replace('08','Aug').replace('09','Sep').replace('10','Oct').replace('11','Nov').replace('12','Dec') + st[2:]
    en1 = en.split('-')[0].replace('01','Jan').replace('02','Feb').replace('03','Mar').replace('04','Apr').replace('05','May').replace('06','Jun').replace('07','Jul').replace('08','Aug').replace('09','Sep').replace('10','Oct').replace('11','Nov').replace('12','Dec') + en[2:]
    
    start = datetime.datetime.strptime(st, "%m-%Y")
    end = datetime.datetime.strptime(en, "%m-%Y")

    date_generated = [start + datetime.timedelta(days=xn) for xn in range(0, (end-start).days)]
    my_dates = []
    my_dates2 = []
    for date in date_generated:
        my_dates.append('20'+ str(date.strftime("%y-%m")))
    my_dates.append(en[-4:]+en[2:3]+en[:2])

    for i in my_dates:
        if i in my_dates2:
            pass
        else:
            my_dates2.append(i)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Safari/537.36'
    }
    r = requests.get("https://bil.branschdata.se/BSnewRegs/",headers = headers)
    soup = bs(r.content, 'html.parser')
    viewstate = soup.find('input',attrs = {'id':'__VIEWSTATE'})['value']
    viewstate_gen = soup.find('input',attrs = {'id':'__VIEWSTATEGENERATOR'})['value']
    event_validator = soup.find('input',attrs = {'id':'__EVENTVALIDATION'})['value']
    ctl00_BodyContent_ChartData = soup.find('input',attrs = {'id':'BodyContent_ChartData'})['value']

    lists = []
    for i in my_dates2:
        mon = i[5:].replace('01','Jan').replace('02','Feb').replace('03','Mar').replace('04','Apr').replace('05','May').replace('06','Jun').replace('07','Jul').replace('08','Aug').replace('09','Sep').replace('10','Oct').replace('11','Nov').replace('12','Dec')
        year =i[:4]
        print(f'Scraping {mon}-{year}')
        
        ctl00_BodyContent_DropDownListPeriodFrom =  i
        ctl00_BodyContent_DropDownListPeriodTo = i
        ctl00_BodyContent_DropDownListFoslag = '1'
        ctl00_BodyContent_DropDownListType ='9'
        ctl00_BodyContent_DropDownListMake = '%'
        ctl00_BodyContent_DropDownListLaan = '%'
        ctl00_BodyContent_ExportToExcelButton = 'Export till Excel'
        ctl00_BodyContent_RadioButtonListView = '0'
        ctl00_BodyContent_ChartHeading1 = 'Personbilar, juli 2021 - totalt antal för perioden: 16778'
        ctl00_BodyContent_ChartHeading2 = 'Marknadsandelar Personbilar, januari 2018'

        login_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR':viewstate_gen,
            '__EVENTVALIDATION':event_validator,
            'ctl00$BodyContent$DropDownListPeriodFrom': ctl00_BodyContent_DropDownListPeriodFrom,
            'ctl00$BodyContent$DropDownListPeriodTo': ctl00_BodyContent_DropDownListPeriodTo,
            'ctl00$BodyContent$DropDownListFoslag': ctl00_BodyContent_DropDownListFoslag,
            'ctl00$BodyContent$DropDownListType': ctl00_BodyContent_DropDownListType,
            'ctl00$BodyContent$DropDownListMake': ctl00_BodyContent_DropDownListMake,
            'ctl00$BodyContent$DropDownListLaan':ctl00_BodyContent_DropDownListLaan,
            'ctl00$BodyContent$ExportToExcelButton': ctl00_BodyContent_ExportToExcelButton,
            'ctl00$BodyContent$RadioButtonListView':ctl00_BodyContent_RadioButtonListView,
            'ctl00$BodyContent$ChartHeading1':ctl00_BodyContent_ChartHeading1,
            'ctl00$BodyContent$ChartHeading2':ctl00_BodyContent_ChartHeading2,
            'ctl00$BodyContent$ChartData':ctl00_BodyContent_ChartData

        }
        url = 'https://bil.branschdata.se/BSnewRegs/'
        r = requests.post(url, data = login_data, headers = headers)
        soup = bs(r.content,'html.parser')
        df = pd.read_excel(r.content)
        df.columns = ["Rank","Antal","Marknadsandel","Modell"]
        antal = df["Antal"].tolist()[3:]
        model = df['Modell'].tolist()[3:]
        
        data = {}
        antal2 = []
        model2 = []
        for an,mo in zip(antal,model):
            if mo in model2:
                pass
            else:
                antal2.append(an)
                model2.append(mo)

        for an,mo in zip(antal2[:-3],model2[:-3]):
            mod = mo.split(' ')
            make = mod[0]
            model = ''
            for m in mod[1:]:
                model = model + ' ' + m
                
            data = {
                'YEAR': year,
                'MONTH': mon,
                'MAKE': make,
                'MODEL': model.strip(),
                'COUNT': an
            }
            lists.append(data)

    df = pd.DataFrame(lists)
    df.to_csv(f'{st1} to {en1}_car-stat.csv',encoding='utf-8',index=False)
    print('\n')
    print(f'Look for a csv named: {st1} to {en1}_car-stat.csv')
    
    
    
#-------------------------------------------------------------------------------------------------------------------------
def specific():
    idate = input('Enter Month-Year(09-2020): ')
    i = idate.split('-')[1] + '-' + idate.split('-')[0]
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Safari/537.36'
    }
    r = requests.get("https://bil.branschdata.se/BSnewRegs/",headers = headers)
    soup = bs(r.content, 'html.parser')
    viewstate = soup.find('input',attrs = {'id':'__VIEWSTATE'})['value']
    viewstate_gen = soup.find('input',attrs = {'id':'__VIEWSTATEGENERATOR'})['value']
    event_validator = soup.find('input',attrs = {'id':'__EVENTVALIDATION'})['value']
    ctl00_BodyContent_ChartData = soup.find('input',attrs = {'id':'BodyContent_ChartData'})['value']
    
    lists = []
    st1 = idate.split('-')[0].replace('01','Jan').replace('02','Feb').replace('03','Mar').replace('04','Apr').replace('05','May').replace('06','Jun').replace('07','Jul').replace('08','Aug').replace('09','Sep').replace('10','Oct').replace('11','Nov').replace('12','Dec') + idate[2:]
    mon = idate.split('-')[0].replace('01','Jan').replace('02','Feb').replace('03','Mar').replace('04','Apr').replace('05','May').replace('06','Jun').replace('07','Jul').replace('08','Aug').replace('09','Sep').replace('10','Oct').replace('11','Nov').replace('12','Dec')
    year = idate.split('-')[1]
    
    
    ctl00_BodyContent_DropDownListPeriodFrom =  i
    ctl00_BodyContent_DropDownListPeriodTo = i
    ctl00_BodyContent_DropDownListFoslag = '1'
    ctl00_BodyContent_DropDownListType ='9'
    ctl00_BodyContent_DropDownListMake = '%'
    ctl00_BodyContent_DropDownListLaan = '%'
    ctl00_BodyContent_ExportToExcelButton = 'Export till Excel'
    ctl00_BodyContent_RadioButtonListView = '0'
    ctl00_BodyContent_ChartHeading1 = 'Personbilar, juli 2021 - totalt antal för perioden: 16778'
    ctl00_BodyContent_ChartHeading2 = 'Marknadsandelar Personbilar, januari 2018'

    login_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR':viewstate_gen,
        '__EVENTVALIDATION':event_validator,
        'ctl00$BodyContent$DropDownListPeriodFrom': ctl00_BodyContent_DropDownListPeriodFrom,
        'ctl00$BodyContent$DropDownListPeriodTo': ctl00_BodyContent_DropDownListPeriodTo,
        'ctl00$BodyContent$DropDownListFoslag': ctl00_BodyContent_DropDownListFoslag,
        'ctl00$BodyContent$DropDownListType': ctl00_BodyContent_DropDownListType,
        'ctl00$BodyContent$DropDownListMake': ctl00_BodyContent_DropDownListMake,
        'ctl00$BodyContent$DropDownListLaan':ctl00_BodyContent_DropDownListLaan,
        'ctl00$BodyContent$ExportToExcelButton': ctl00_BodyContent_ExportToExcelButton,
        'ctl00$BodyContent$RadioButtonListView':ctl00_BodyContent_RadioButtonListView,
        'ctl00$BodyContent$ChartHeading1':ctl00_BodyContent_ChartHeading1,
        'ctl00$BodyContent$ChartHeading2':ctl00_BodyContent_ChartHeading2,
        'ctl00$BodyContent$ChartData':ctl00_BodyContent_ChartData

    }
    url = 'https://bil.branschdata.se/BSnewRegs/'
    r = requests.post(url, data = login_data, headers = headers)
    soup = bs(r.content,'html.parser')
    df = pd.read_excel(r.content)


    df.columns = ["Rank","Antal","Marknadsandel","Modell"]

    antal = df["Antal"].tolist()[3:]
    model = df['Modell'].tolist()[3:]


    data = {}

    antal2 = []
    model2 = []
    for an,mo in zip(antal,model):
        if mo in model2:
            pass
        else:
            antal2.append(an)
            model2.append(mo)

    for an,mo in zip(antal2[:-3],model2[:-3]):
        mod = mo.split(' ')
        make = mod[0]
        model = ''
        for m in mod[1:]:
            model = model + ' ' + m

        data = {
            'YEAR': year,
            'MONTH': mon,
            'MAKE': make,
            'MODEL': model.strip(),
            'COUNT': an
        }
        lists.append(data)

    df = pd.DataFrame(lists)
    df.to_csv(f'{st1}_car-stat.csv',encoding='utf-8',index=False)
    print('\n')
    print(f'Look for a csv named: {st1}_car-stat.csv')
    
    
    
    
def main():
    print('1. Scrape Multiple Months Using Range(01-2018 to 07-2021)')
    print('2. Single month(like, 02-2021)')
    print('3. Exit')
    check = int(input('Enter Choice: '))
    if check ==1:
        range_scrape()
    elif check ==2:
        specific()
    else:
        exit()
main()