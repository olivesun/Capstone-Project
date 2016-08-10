// Morris.js Charts sample data for SB Admin template

$(function() {

    // Area Chart
    // Morris.Area({
    //     element: 'morris-area-chart',
    //     data: [{
    //         period: '2010 Q1',
    //         iphone: 2666,
    //         ipad: null,
    //         itouch: 2647
    //     }, {
    //         period: '2010 Q2',
    //         iphone: 2778,
    //         ipad: 2294,
    //         itouch: 2441
    //     }, {
    //         period: '2010 Q3',
    //         iphone: 4912,
    //         ipad: 1969,
    //         itouch: 2501
    //     }, {
    //         period: '2010 Q4',
    //         iphone: 3767,
    //         ipad: 3597,
    //         itouch: 5689
    //     }, {
    //         period: '2011 Q1',
    //         iphone: 6810,
    //         ipad: 1914,
    //         itouch: 2293
    //     }, {
    //         period: '2011 Q2',
    //         iphone: 5670,
    //         ipad: 4293,
    //         itouch: 1881
    //     }, {
    //         period: '2011 Q3',
    //         iphone: 4820,
    //         ipad: 3795,
    //         itouch: 1588
    //     }, {
    //         period: '2011 Q4',
    //         iphone: 15073,
    //         ipad: 5967,
    //         itouch: 5175
    //     }, {
    //         period: '2012 Q1',
    //         iphone: 10687,
    //         ipad: 4460,
    //         itouch: 2028
    //     }, {
    //         period: '2012 Q2',
    //         iphone: 8432,
    //         ipad: 5713,
    //         itouch: 1791
    //     }],
    //     xkey: 'period',
    //     ykeys: ['iphone', 'ipad', 'itouch'],
    //     labels: ['iPhone', 'iPad', 'iPod Touch'],
    //     pointSize: 2,
    //     hideHover: 'auto',
    //     resize: true
    // });

    // Donut Chart
    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Non Customers",
            value: 9990
        }, {
            label: "Customers",
            value: 8
        }, {
            label: "Reviewers",
            value: 2
        }],
        resize: true
    });



    // Bar Chart
    Morris.Bar({
        element: 'morris-bar-chart',
        data: [
          {x: 'Impression', y: 5, z: 100, a: 500},
          {x: 'CPC', y: 3.27, z: 65, a: 327},
          {x: '5+ Users', y: 1.73, z: 35, a: 173},
          {x: '10+ Users', y: 0.93, z: 19, a: 93}
        ],
        xkey: 'x',
        ykeys: ['y', 'z', 'a'],
        labels: ['$/click', '$/customer', '$/reviewer'],
        xLabelAngle: 45,
        stacked: true
    });
    // Line Chart
    var day_data = [
      {"elapsed": "Basic", "value": 1,"value2":0},
      {"elapsed": "5+", "value": 2.90, "value2":8.30},
      {"elapsed": "6+", "value": 3.36, "value2":6.61},
      {"elapsed": "7+", "value": 3.87, "value2":5.44},
      {"elapsed": "8+", "value": 4.36, "value2":4.67},
      {"elapsed": "9+", "value": 4.76, "value2":4.06},
      {"elapsed": "10+", "value": 5.37, "value2":3.62},
    ];
    Morris.Line({
      element: 'morris-line-chart',
      data: day_data,
      xkey: 'elapsed',
      ykeys: ['value', 'value2'],
      labels: ['times of baseline', '% identified'],
      parseTime: false
    });
});
