var gaugeOptions1 = {

  chart: {
    type: 'solidgauge',
    backgroundColor: '#9e9e9e',
    height: '55%'
  },

 // renderto: "container-testi",
  title: null,

  pane: {
    center: ['50%', '70%'],
    size: '110%',
    startAngle: -90,
    endAngle: 90,
    background: {
      backgroundColor: '#424242',
      innerRadius: '60%',
      outerRadius: '100%',
      shape: 'arc'
    }
  },

  tooltip: {
    enabled: false
  },

  // the value axis
  yAxis: {
    stops: [
      [0.5, '#DF5353'], // red
      [0.8, '#FFFF00'], // yellow
      [0.9, '#55BF3B'] // green
    ],
    lineWidth: 0,
    minorTickInterval: null,
    tickAmount: 2,
    title: {
      y: -70
    },
    labels: {
      y: 16
    }
  },

  plotOptions: {
    solidgauge: {
      dataLabels: {
        y: 5,
        borderWidth: 0,
        useHTML: true
      }
    }
  }
};

var gaugeOptions2 = {

    chart: {
      type: 'solidgauge',
      backgroundColor: '#9e9e9e',
      height: '55%'
    },
  
   // renderto: "container-testi",
    title: null,
  
    pane: {
      center: ['50%', '70%'],
      size: '110%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: '#424242',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },
  

    tooltip: {
      enabled: false
    },
  
    // the value axis
    yAxis: {
      stops: [
        [0.167, '#55BF3B'], // green
        [0.167,'#FFFF00'], // yellow
        [0.7, '#DF5353'] // red
      ],
      lineWidth: 0,
      minorTickInterval: null,
      tickAmount: 2,
      title: {
        y: -70
      },
      labels: {
        y: 16
      }
    },
  
    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    }
  };
  
  // The speed gauge
  var chartMittari2 = Highcharts.chart('container-mittari2', Highcharts.merge(gaugeOptions2, {
    yAxis: {
      min: 0,
      max: 30,
      title: {
        text: 'Keskimääräinen myöhästyminen',
        style: {
          color: '#2E2E2E',
          font: '14px Sans-serif'
        }
      }
    },
  
    credits: {
      enabled: false
    },
  
    series: [{
      name: 'Myöhästyminen keskimäärin',
      data: kpi_2,
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:25px;color:' +
          ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
             '<span style="font-size:12px;color:silver">min</span></div>'
      },
      tooltip: {
        valueSuffix: ' %'
      }
    }]
  
  }));
  
  // Junat myöhässä %
  var chartMittari1 = Highcharts.chart('container-mittari1', Highcharts.merge(gaugeOptions1, {
    yAxis: {
      min: 0,
      max: 100,
      title: {
        text: 'Junista ajoissa',
        style: {
          color: '#2E2E2E',
          font: '14px Sans-serif'
        }
      }
    },
  
    series: [{
      name: 'Ajoissa',
      data: kpi_1,
      dataLabels: {
        format: '<div style="text-align:center"><span style="font-size:25px;color:' +
          ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.0f}</span><br/>' +
             '<span style="font-size:12px;color:silver"> % </span></div>'
      },
    }]
  
  }));
  


