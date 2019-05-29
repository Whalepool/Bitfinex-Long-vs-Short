// THEME
Highcharts.flatdark = {
  "colors": ["#dc4460", "#569a5e", "#9b59b6", "#e74c3c", "#0f131f", "#3498db", "#1abc9c", "#f39c12", "#d35400"],
  "chart": {
    "backgroundColor": "#0f131f"
  },
  "xAxis": {
    "gridLineDashStyle": "solid",
    "gridLineWidth": 1,
    "gridLineColor": "#1b2237",
    "lineColor": "#1b2237",
    "minorGridLineColor": "#BDC3C7",
    "tickColor": "#1b2237",
    "tickWidth": 1,
    "title": {
      "style": {
        "color": "#FFFFFF"
      }
    }
  },
  "yAxis": {
    "gridLineDashStyle": "solid",
    "gridLineColor": "#1b2237",
    "lineColor": "#BDC3C7",
    "minorGridLineColor": "#BDC3C7",
    "tickColor": "#1b2237",
    "tickWidth": 1,
    "title": {
      "style": {
        "color": "#FFFFFF"
      },
    }
  },
  "legendBackgroundColor": "rgba(0, 0, 0, 0.5)",
  "background2": "#505053",
  "dataLabelsColor": "#B0B0B3",
  "textColor": "#34495e",
  "contrastTextColor": "#F0F0F3",
  "maskColor": "rgba(255,255,255,0.3)",
  "title": {
    "style": {
      "color": "#FFFFFF"
    }
  },
  "title": {
    "style": {
      "color": "#fff",
      "font-family": "'Montserrat'",
      "font-size": "16px",
      "font-weight": "bold"
    },
  },
  "subtitle": {
    "style": {
      "color": "#666666"
    }
  },
  "legend": {
    "itemStyle": {
      "color": "#C0C0C0"
    },
    "itemHoverStyle": {
      "color": "#C0C0C0"
    },
    "itemHiddenStyle": {
      "color": "#444444"
    }
  }
}

Highcharts.setOptions(Highcharts.flatdark)


// HELPERS

// Add commas to values
function addCommas(nStr) {
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


/**
 * treemapHelper
 * Renders treemap chart with common defaults
 */
function treemapHelper({ el, series, title }) {
  Highcharts.chart(el, {
    series: [{
      type: 'treemap',
      layoutAlgorithm: 'squarified',
      data: series
    }],
    title: {
      text: title
    },
    credits: {
      enabled: false
    },
  })
}

/**
 * barHelper
 * Renders bar chart with common defaults
 */
function barHelper({ el, series, title, categories, yAxisFormatter, seriesFormatter }) {
  let baseConfig = {
    chart: {
      type: 'bar'
    },
    title: {
      text: title
    },
    legend: {
      enabled: false
    },
    tooltip: {
      enabled: false
    },
    credits: {
      enabled: false
    },
    xAxis: {
      categories: categories,
      reversed: true,
      labels: {
        style: {
          color: '#fff',
          font: '11px Trebuchet MS, Verdana, sans-serif'
        }
      },
    },
    yAxis: {
      title: {
        text: null
      },

      labels: {
        formatter: yAxisFormatter,
        style: {
          color: '#fff',
          font: '11px Trebuchet MS, Verdana, sans-serif'
        },
      }
    },

    plotOptions: {
      series: {
        stacking: 'normal',
        enableMouseTracking: false,
        borderWidth: 0,
        pointPadding: 0.1,
        groupPadding: 0,
        pointWidth: 10,
        dataLabels: {
          enabled: false
        }
      }
    },

    series: series
  }

  if (seriesFormatter) {
    baseConfig.plotOptions.series.dataLabels = {
      enabled: true,
      crop: false,
      overflow: 'none',
      inside: false,
      style: {
        textOutline: 0,
      },
      formatter: seriesFormatter
    }
  }

  Highcharts.chart(el, baseConfig)
}