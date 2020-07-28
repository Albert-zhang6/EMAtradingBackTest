import quandl
import pandas as pd
import numpy  as np
import math
import matplotlib.pyplot as plt
import datetime as dt

msft = pd.read_csv("C:/Users/Albert Zhang/Desktop/test/MICROSOFT.csv")
msft.set_index('Date', inplace=True)

startyear = 2020
startmonth = 1
startday = 1

start=dt.datetime(startyear, startmonth, startday)

now=dt.datetime.now()

emaUsed = [3,5,8,10,12,15,30,35,40,45,50,60]
for x in emaUsed:
	ema=x
	msft['Ema_'+str(ema)]=msft.iloc[:,3].ewm(span=ema, adjust=False).mean()

print(msft.tail())


pos = 0
num = 0
percentchange = []

for i in msft.index:
	cmin = min(msft["Ema_3"][i],msft["Ema_5"][i],msft["Ema_8"][i],msft["Ema_10"][i],msft["Ema_12"][i],msft["Ema_15"][i])
	cmax = max(msft["Ema_30"][i],msft["Ema_35"][i],msft["Ema_40"][i],msft["Ema_45"][i],msft["Ema_50"][i],msft["Ema_60"][i])

	close=msft['Close/Last'][i]

	if(cmin>cmax):
		print("Buy Signal")
		if (pos==0):
			bp=close
			pos=1
			print("Buying now at " +str(bp))

	elif(cmin<cmax):
		print("Sell Signal")
		if(pos==1):
			pos=0
			sp=close
			print("Selling now at" +str(sp))
			pc = (sp/bp-1)*100
			percentchange.append(pc)

	if(num==msft['Close/Last'].count()-1 and pos==1):
		pos=0
		sp=close
		print("Selling now at " +str(sp))
		pc = (sp/bp-1)*100
		percentchange.append(pc)
	
	num+=1

print(percentchange)	


gains=0
ng=0
losses=0
nl=0
totalReturn=1

for i in percentchange:
	if(i>0):
		gains+=i
		ng+=1
	else:
		losses+=i
		nl+=1
	totalReturn=totalReturn*((i/100)+1)

totalReturn=round((totalReturn-1)*100,2)

if(ng>0):
	avgGains = gains/ng
	maxR = str(max(percentchange))
else:
	avgGains = 0
	maxR = "unrealized"

if(ng>0):
	avgLoss = losses/nl
	maxL = str(min(percentchange))
	ratio = str(-avgGains/avgLoss)
else:
	avgLoss = 0
	maxL = "unrealized"
	ratio ="inf"



print()
print("Results for Microsoft from"+str(msft.index[0])+", Sample size: "+str(ng+nl)+" trades")
print("EMAs used: "+str(emaUsed))
print("Average Gain: "+ str(avgGains))
print("Average Loss: "+ str(avgLoss))
print("Gain/loss ratio: "+ ratio)
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+ " trades: "+ str(totalReturn)+"%" )
print()



