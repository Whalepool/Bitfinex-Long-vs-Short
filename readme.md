# Bitfinex Long Vs Short script by @whalepoolbtc - https://whalepool.io   

Tired of the mis information out there regarding people's analysis and understanding of the bitfinex long/short data - I create this script so people can better get an understanding of the numbers and what they mean.  
  
It's not pretty, but it works.  
  
## Todo (someone else not me !)
If anyones feeling keen and enthusiastic, they could... 
- ~~Put the tickers you want to fetch the data for into a dict/list, maybe build the list from an api query~~
- ~~Put in api requests into a function to handle/wait upon api limit errors~~
- ~~Query the coinmarketcap api, `https://api.coinmarketcap.com/v1/ticker/?limit=0` and add another column of data for total supply/circulating supply and the % of the tickers long/short delta relative to the total circulating supply~~
- ~~Plot some visualisations of the L/S data~~ 
- ~~Fix the combination pairs, where by ETHUSD+ETHBTC can be added up together~~ 
- ~~Build currency values automatically from inputted ticker pairs~~
- ~~Allow input of ticker pairs from command line arguments~~
- ~~Output dump of data to csv/json file ~~
- ~~Save the data hourly to csv~~ 
- Time and date chart
- Legend to help label charts
- If we have a small number of tickers, sleep timer can be quicker, if more tickers, sleep time delay longer
- Add flag to change logging level output 
- Imgur auto upload plotted data for easy sharing 
  
For more info join [@whalepoolbtc](https://t.me/whalepoolbtc) on telegram   

## Example console output 
Easy copy/paste snippets
Easy table for quick comparisson 

![Example output](https://i.imgur.com/B6Q9r97.png)

## Example data visualisaiton output 
![Example output](https://i.imgur.com/xXUYtip.png)

