// Build Cumulative Data
var cumlutiveData =[];

function GetCumlutiveData(){
    var url='/data/cumulative_data_last.json';
        $.ajax({
        url: url,
        success: function(data) {
        // console.log(data);
         cumlutiveData = data;
         RenderTimestamp(data);
        },
        async:false
      });
     return cumlutiveData;
}

function RenderCumlutiveData(){
   
    var data = GetCumlutiveData();
     //console.log(data);
     $('#cumulative').html('');
     $.each(data, function( index, value ) {
            RenderCumlutive(value, index);
     });
}

function RenderCumlutive(data, index){

// Make HTML
    var target=$("#cumulative");
   
    var fdata = {} 

    Object.keys(data).forEach(function(key) {
        if (data[key]) {
            fdata[key] = addCommas(data[key])
        } else {
            fdata[key] = '&infin;'
        }
    })


    var html = `
                <div class="table_data_row" data-index="${index}">
                    <div class="table_data_crypto">${data.fpart}</div>
                    <div class="table_data_large">&#x24;${fdata.marketcap}</div>
                    <div class="table_data_large">${fdata.available_supply}</div>
                    <div class="table_data_large">${fdata.max_supply}</div>
                    <div class="table_data_large">${data.as_percent_long}:${data.as_percent_short}</div>
                    <div class="table_data_large data_long">&#x24;${fdata.total_longs_usd}</div>
                    <div class="table_data_large data_short">&#x24;${fdata.total_shorts_usd}</div>
                </div>`

    target.append(html);


    // Colour Code higher long/short value
  
    var val3 = data.total_longs_usd;
    var val4 = data.total_shorts_usd;
    

      if(val3 > val4) {
          $(`.table_data_row[data-index=${index}] .data_long`).addClass('green'); 
          $(`.table_data_row[data-index=${index}] .data_short`).addClass('red');
      } else {
          $(`.table_data_row[data-index=${index}] .data_long`).addClass('red'); 
          $(`.table_data_row[data-index=${index}] .data_short`).addClass('green');
      }
}


RenderCumlutiveData()




// Build Margin Data
var marginData =[];

function GetMarginData(){
    var url='/data/margin_data_last.json';
        $.ajax({
        url: url,
        success: function(data) {
        // console.log(data);
         marginData = data;
         RenderTimestamp(data);
        },
        async:false
      });
     return marginData;
}

function RenderMarginData(){
    $('#timestamp').html('Updating, please wait...');

    var data = GetMarginData();
     //console.log(data);
     $('#poster').html('');
     $.each(data, function( index, value ) {
            RenderMargin(value, index);
     });
}

function RenderMargin(data, index){

// Make HTML
    var target=$("#poster");
   
   // Format data to have commas
    var fdata = {} 
    Object.keys(data).forEach(function(key) {
        fdata[key] = addCommas(data[key])
    })

    // Add currency symbols
    function formatWithSymbol(key) {
        var symbolMap = {
            'EUR': '€',
            'USD': '$'
        }

        if (symbolMap[data.lpart]) {
            return `${symbolMap[data.lpart]}${fdata[key]}`
        }

        return `${fdata[key]} ${data.lpart}`

    }


    // Build HTML
    var html = `<div class="ticker_container" data-index="${index}">
                    <div class="ticker_header">${data.fpart}/${data.lpart}</div>
                      <div class="ticker_data">
                        <div class="ticker_data_left">
                          <div class="long_short_ratio">
                              <div class="data_label">Long/Short Ratio</div>
                              <div class="data">${data.overall_ls_ratio}</div>
                          </div>
                          <div class="percent_long_short">
                            <div class="data_label">% of supply long:short</div>
                            <div class="data">${data.as_percent_long}:${data.as_percent_short}</div>
                          </div>
                          <div class="long_daily_charge">
                            <div class="data_label">Long Daily Charge</div>
                            <div class="data">${formatWithSymbol('long_funding_charge')}</div>
                          </div>
                          <div class="short_daily_charge">
                            <div class="data_label">Short Daily Charge</div>
                            <div class="data">${data.short_funding_charge} ${data.fpart}</div>
                          </div>
                        </div>
                        <div class="ticker_data_right">
                          <div class="total_long">
                            <div class="data_label">Total Long</div>
                            <div class="data data_long">${fdata.total_longs} (${formatWithSymbol('total_longs_usd')})</div>
                          </div>
                          <div class="funded_longs">
                            <div class="data_label">Funded Longs</div>
                            <div class="data data_long">${formatWithSymbol('long_funding')}</div>
                          </div>
                          <div class="total_short">
                            <div class="data_label">Total Short</div>
                            <div class="data data_short">${fdata.total_shorts} (${formatWithSymbol('total_shorts_usd')})</div>
                          </div>
                          <div class="funded_shorts">
                            <div class="data_label">Funded Shorts</div>
                            <div class="data data_short">${fdata.short_funding} ${data.fpart}</div>
                          </div>
                        </div>
                </div>`

    target.append(html);

    // Colour Code higher long/short value
  
    var val1 = data.total_longs_usd;
    var val2 = data.total_shorts_usd;
    
      if(val1 > val2) {
         console.log("long");
          $(`.ticker_container[data-index=${index}] .data_long`).addClass('green'); 
          $(`.ticker_container[data-index=${index}] .data_short`).addClass('red');
      } else {
        console.log("short");
          $(`.ticker_container[data-index=${index}] .data_long`).addClass('red'); 
          $(`.ticker_container[data-index=${index}] .data_short`).addClass('green');
      }

}

// Show last timestamp
function RenderTimestamp(data)
{
   $('#timestamp').html(data[0].timestamp.split('.')[0]);
}

RenderMarginData()





function addCommas(nStr)
{
    nStr += '';
    x = nStr.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
}