# Bitfinex Long Vs Short script by @whalepoolbtc - https://whalepool.io   

Tired of the mis information out there regarding people's analysis and understanding of the bitfinex long/short data - I create this script so people can better get an understanding of the numbers and what they mean.  
  
It's not pretty, but it works.  
  
## Todo 
If anyones feeling keen and enthusiastic, they could... 
- Put the tickers you want to fetch the data for into a dict/list, maybe build the list from an api query
- Put in api requests into a function to handle/wait upon api limit errors
- Query the coinmarketcap api, `https://api.coinmarketcap.com/v1/ticker/?limit=0` and add another column of data for total supply/circulating supply and the % of the tickers long/short delta relative to the total circulating supply
  
For more info join [@whalepoolbtc](https://t.me/whalepoolbtc) on telegram   

## Example output 

![Example output](https://i.imgur.com/KnNavot.png)

