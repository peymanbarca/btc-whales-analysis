from bs4 import BeautifulSoup
import requests
import pandas as pd


totalSum = 0
totalSell = 0
totalBuy = 0
totalBuyers = 0
totalSellers = 0

for pageNum in range(1,100):
    url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-{}.html'.format(pageNum)
    html = (requests.request(method='get',url=url)).text
    bs = BeautifulSoup(html)

    table = bs.find_all("table",{"class": "table table-striped abtb"})[0]
    caption = table.find(lambda tag: tag.name=='caption')


    rows = table.findAll(lambda tag: tag.name=='tr')



    table = bs.find_all("table",{"class": "table table-striped bb"})[0]

    rows2 = table.findAll(lambda tag: tag.name=='tr')

    rows += rows2


    print(caption,len(rows),'\n','\n\n')


    data =[]

    for item in rows:
        if item!=None:
            try:
                id = (str(item.find_all(lambda tag: tag.name=='td')[0]).split('>')[1]).replace("</td","")
                balances = (str(item.find("td",{"class" : "hidden-phone"})).split('">'))
                change=""
                balance=""
                address = ((str(item.find_all('a', href=True)[0]))[1:-1]).replace("a href=","").split('">')[0]
                if len(balances)>2:
                    balance = (balances[1]).split("<span")[0]
                    change = (str(item.find("span",{"class" : "text-success"})).split(">")[1]).replace("</span","")
                else:
                    balance = (balances[1]).replace("</td>","")
                    change=""
                lastIn = (str(item.find_all('td',{'class':'utc hidden-tablet'})[1]).split('hidden-tablet">')[1]).split(" UTC")[0]
                lastOut = (str(item.find_all('td', {'class': 'utc hidden-tablet'})[3]).split('hidden-tablet">')[1]).split(" UTC")[0]
                if lastOut=='</td>':
                    lastOut=''
                data.append([id,balance,change,address,lastIn, lastOut])
                #print(id, "    ", len(balances) , "   ", balance, "   ", change, "   ", address )

            except:
                try:
                    id = None
                    balances = (str(item.find("td", {"class": "hidden-phone"})).split('">'))
                    change = ""
                    balance = ""
                    address = ((str(item.find_all('a', href=True))[1:-1]).replace("a href=","").split('">')[0]).replace("<","")
                    if len(balances) > 2:
                        balance = (balances[1]).split("<span")[0]
                        change = ((str(item.find("span", {"class": "text-error"}))).split(">")[1]).replace("</span","")
                    lastIn = \
                    (str(item.find_all('td', {'class': 'utc hidden-tablet'})[1]).split('hidden-tablet">')[1]).split(
                        " UTC")[0]
                    lastOut = \
                    (str(item.find_all('td', {'class': 'utc hidden-tablet'})[3]).split('hidden-tablet">')[1]).split(" UTC")[0]
                    if lastOut == '</td>':
                        lastOut = ''
                    data.append([id,balance,change,address,lastIn, lastOut])
                except:
                    pass

    DF = pd.DataFrame(data=data,columns=['rowNumber','Current Balance','Recent Change','Address','Last-in', 'Last-Out'])


    counter = 0
    sum = 0
    buy = 0
    sell = 0


    cnt_seller = 0
    cnt_buyer = 0
    for index,row in DF.iterrows():
        if row['Recent Change']!='':
            change = row['Recent Change']

            if str(change).__contains__("+"):
                ch = float(change.replace("+","").replace(" BTC",""))
                sum += ch
                buy += ch
            elif str(change).__contains__("-"):
                ch = float(change.replace("-", "").replace(" BTC", ""))
                sum -= ch
                sell += ch
            counter+=1

        if str(row['Last-Out']).__contains__('2022-01') or str(row['Last-Out']).__contains__('2021-12'):
            cnt_seller+=1
        if str(row['Last-in']).__contains__('2022-01') or str(row['Last-in']).__contains__('2021-12'):
            cnt_buyer += 1

    totalSell += sell
    totalBuy += buy
    totalSum += sum
    totalBuyers += cnt_buyer
    totalSellers += cnt_seller
    print(url)
    print('\n\n Page Num ', pageNum , ' Total Changed Recently :  ', 'Num : ' , counter, ' SUM : ' , "+" if sum>0 else "-" , sum , " BTC", ' Total Buy ', buy, " BTC", ' \033[1m Total Sell ', sell, " BTC")
    print('Cnt Seller : ', cnt_seller, 'Cnt Buyer : ', cnt_buyer)
    print('\033[0m ----------------------')

print('Total Sum : ', totalSum, 'Total Buy : ' , totalBuy, 'Total Sell', totalSell)
print('Total Number of Buyers : ', totalBuyers, 'Total Number of Sellers : ', totalSellers)
