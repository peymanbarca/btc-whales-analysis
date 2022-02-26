import requests
import json
from matplotlib import  pyplot as plt
from datetime import datetime


num = 1
url = "https://www.lookintobitcoin.com/django_plotly_dash/app/min_{}_count/_dash-update-component".format(num)

payload= str("{\"output\":\"chart.figure\",\"changedPropIds\":[\"url.pathname\"],\"inputs\":[{\"id\":\"url\",\"property\":\"pathname\",\"value\":\"/charts/wallets-greater-than-xxx-btc/\"}]}").replace("xxx",str(num))
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

res = json.loads(response.text)

dates = list(res['response']['props']['figure']['data'][1]['x'])
nums = list(res['response']['props']['figure']['data'][1]['y'])
price = list(res['response']['props']['figure']['data'][0]['y'])


today = datetime.today().strftime('%Y-%m-%d')

print(len(dates),len(nums))
print('Today : ',today)

today_str = str(today) + "T00:00:00"


days_back = 90

index = dates.index(today_str)
dates_picked = dates [index+1-days_back:index]
nums_picked = nums[index-days_back:index]
price_picked = price[index-days_back:index]

print(len(dates_picked),dates_picked)
print(len(nums_picked),nums_picked)
print(len(price_picked),price_picked)

fig = plt.figure()
ax = fig.add_subplot(211)
ax.plot(dates_picked, nums_picked)
plt.xlabel('DATE')
plt.xticks(rotation=45)
plt.ylabel('Addresses')
plt.title('{} # BTC Addresses'.format(num))


ax2 = fig.add_subplot(212)
ax2.plot(dates_picked, price_picked,'y')
plt.xlabel('DATE')
plt.ylabel('BTC Price')
plt.xticks(rotation=45)


def mouse_event(event):
    print('x: {} and y: {}'.format(event.xdata, event.ydata))



cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
plt.show()
