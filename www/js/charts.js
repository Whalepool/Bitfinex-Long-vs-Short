
load()

/**
 * load
 * Request data from JSON
 */
function load() {
  // Load cumulative data
  $.ajax({
    url: '/data/cumulative_data_last.json',
    success: renderCumulative
  })

  // Load margin data
  $.ajax({
    url: '/data/margin_data_last.json',
    success: renderMargin
  })
}

/**
 * updateTimestamp
 * Updates timestamp
 */
function updateTimestamp(data) {
  $('#timestamp').html(data[0].timestamp.split('.')[0]);
}


/**
 * renderMargin
 * Executed on XHR response, kicks off render fns
 */
function renderMargin(data) {
  updateTimestamp(data)
  renderMarginTables(data)
  renderMarginCharts(data)
}

/**
 * renderCumulative
 * Executed on XHR response, kicks off render fns
 */
function renderCumulative(data) {
  renderCumulativeTables(data)
  renderCumulativeCharts(data)
}


/**
 * renderCumulativeTables
 * Builds ticker table
 */
function renderCumulativeTables(data) {
  var $target = $('#cumulative')
  var fdata = data.map(row => {
    let formattedRow = { raw: row }

    Object.keys(row).forEach(function(key) {
      if (row[key]) {
        formattedRow[key] = addCommas(row[key]) // util.js
      } else {
        formattedRow[key] = '&infin;'
      }
    })

    return formattedRow
  })

  // Loop formatted data, render each row
  fdata.forEach(renderCumulativeRow)

  // Renders an individual row of ticker table
  function renderCumulativeRow(row, index) {
    var html = `
      <div class="table_data_row" data-index="${index}">
          <div class="table_data_crypto">${row.raw.fpart}</div>
          <div class="table_data_large">&#x24;${row.marketcap}</div>
          <div class="table_data_large">${row.available_supply}</div>
          <div class="table_data_large">${row.max_supply}</div>
          <div class="table_data_large">${row.raw.as_percent_long}:${row.raw.as_percent_short}</div>
          <div class="table_data_large data_long">&#x24;${row.total_longs_usd}</div>
          <div class="table_data_large data_short">&#x24;${row.total_shorts_usd}</div>
      </div>`

    $target.append(html) 

    // Colour Code higher long/short value
    var longs = row.raw.total_longs_usd;
    var shorts = row.raw.total_shorts_usd;

    if (longs > shorts) {
      $(`.table_data_row[data-index=${index}] .data_long`).addClass('green')
      $(`.table_data_row[data-index=${index}] .data_short`).addClass('red')
    } else {
      $(`.table_data_row[data-index=${index}] .data_long`).addClass('red')
      $(`.table_data_row[data-index=${index}] .data_short`).addClass('green')
    }
  }
}


/**
 * renderMarginTables
 * Builds margin table
 */
function renderMarginTables(data) {
  var $target = $('#poster')
  var fdata = data.map(row => {
    let formattedRow = { raw: row }
    let symbolKeys = ['long_funding_charge', 'total_longs_usd', 'long_funding', 'total_shorts_usd']
    let symbolMap = {
      'EUR': '€',
      'USD': '$'
    }

    Object.keys(row).forEach(function(key) {
      let formatted = addCommas(row[key]) // util.js

      // Add symbols if needed
      if (symbolKeys.includes(key)) {
        let symbol = symbolMap[row.lpart]

        if (symbol) {
          formatted = `${symbol}${formatted}`
        } else {
          formatted = `${formatted} ${row.lpart}`
        }
      }

      formattedRow[key] = formatted
    })

    return formattedRow
  })

  // Loop formatted data, render each row
  fdata.forEach(renderMarginBox)

  // Renders an individual row of ticker table
  function renderMarginBox(row, index) {
    var html = `
      <div class="ticker_container" data-index="${index}">
        <div class="ticker_header">${row.raw.fpart}/${row.raw.lpart}</div>
        <div class="ticker_data">
          <div class="ticker_data_left">
            <div class="long_short_ratio">
              <div class="data_label">Long/Short Ratio</div>
              <div class="data">${row.raw.overall_ls_ratio}</div>
            </div>
            <div class="percent_long_short">
              <div class="data_label">% of supply long:short</div>
              <div class="data">${row.raw.as_percent_long}:${row.raw.as_percent_short}</div>
            </div>
            <div class="long_daily_charge">
              <div class="data_label">Long Daily Charge</div>
              <div class="data">${row.long_funding_charge}</div>
            </div>
            <div class="short_daily_charge">
              <div class="data_label">Short Daily Charge</div>
              <div class="data">${row.raw.short_funding_charge} ${row.raw.fpart}</div>
            </div>
          </div>
          <div class="ticker_data_right">
            <div class="total_long">
              <div class="data_label">Total Long</div>
              <div class="data data_long">${row.total_longs} (${row.total_longs_usd})</div>
            </div>
            <div class="funded_longs">
              <div class="data_label">Funded Longs</div>
              <div class="data data_long">${row.long_funding}</div>
            </div>
            <div class="total_short">
              <div class="data_label">Total Short</div>
              <div class="data data_short">${row.total_shorts} (${row.total_shorts_usd})</div>
            </div>
            <div class="funded_shorts">
              <div class="data_label">Funded Shorts</div>
              <div class="data data_short">${row.short_funding} ${row.raw.fpart}</div>
            </div>
          </div>
        </div>
      </div>`

    $target.append(html) 

    // Colour Code higher long/short value
    var longs = row.raw.total_longs_usd
    var shorts = row.raw.total_shorts_usd

    if (longs > shorts) {
      $(`.ticker_container[data-index=${index}] .data_long`).addClass('green')
      $(`.ticker_container[data-index=${index}] .data_short`).addClass('red')
    } else {
      $(`.ticker_container[data-index=${index}] .data_long`).addClass('red')
      $(`.ticker_container[data-index=${index}] .data_short`).addClass('green')
    }
  }
}


/**
 * renderCumulativeCharts
 * Builds cumulative charts
 */
function renderCumulativeCharts(data) {
  let categories = data.map(item => item.fpart);
  
  // Market cap
  function treemap() {
    treemapHelper({
      el: 'treemap',
      title: 'Market Cap Sizes',
      series: data.map(v => {
        return {
          name: v.fpart,
          value: v.marketcap
        }
      })
    })
  }

  // USD valuation of margin positions
  function usdMargin() {
    let series = (function() {
      let positions = {
        'Short': [],
        'Long': []
      }

      data.forEach(v => {
        positions.Long.push(v.total_longs_usd)
        positions.Short.push(-v.total_shorts_usd)
      })

      positions = Object.keys(positions).map(key => {
        return {
          name: key,
          data: positions[key]
        }
      })

      return positions
    })()

    barHelper({
      el: 'container',
      title: 'USD valuation of margin positions',
      series: series,
      categories: categories,
      yAxisFormatter: function() {
        return Math.abs(this.value) / 1000000
      },
      seriesFormatter: function() {
        return '$' + Highcharts.numberFormat(Math.abs(this.y) / 1000000, 0) + 'm'
      }
    })
  }

  // Circulating supply that is margin L/S
  function circulating() {
    let series = (function() {
      let positions = {
        'Short': [],
        'Long': []
      }

      data.forEach(v => {
        positions.Long.push(v.as_percent_long)
        positions.Short.push(-v.as_percent_short)
      })

      positions = Object.keys(positions).map(key => {
        return {
          name: key,
          data: positions[key]
        }
      })

      return positions
    })()

    barHelper({
      el: 'container2',
      title: '% of Circulating supply that is margin L/S',
      series: series,
      categories: categories,
      yAxisFormatter: function() {
        return this.value + '%'
      }
    })
  }


  treemap()
  usdMargin()
  circulating()
}

/**
 * renderMarginCharts
 * Builds margin charts
 */
function renderMarginCharts(data) {
  // Individual ticket breakdown of circulating supply L/S
  function ticker() {
    let categories = data.map(item => item.ticker)
    let series = (function() {
      let positions = {
        'Short': [],
        'Long': []
      }

      data.forEach(v => {
        positions.Long.push(v.as_percent_long)
        positions.Short.push(-v.as_percent_short)
      })

      positions = Object.keys(positions).map(key => {
        return {
          name: key,
          data: positions[key]
        }
      })

      return positions
    })()

    barHelper({
      el: 'container3',
      title: 'Individual ticker breakdown % of Circulating supply L/S',
      series: series,
      categories: categories,
      yAxisFormatter: function() {
        return this.value + '%'
      }
    })
  }
  
  ticker()
}