/**
 * Created by kmu on 16.12.2016.
 */

var Values1 = [
    20,
    40,
    25,
    50,
    15,
    45,
    33,
    34
];

var LineConfig = {
    "type": "line",
    "utc": true,
    "plotarea": {
        "adjust-layout": true
    },
    "scale-x": {
        "label": {
            "text": "Above is an example of a time-series scale"
        },
        "min-value": 1420070400000,
        "step": "day",
        "transform": {
            "type": "date",
            "all": "%m.%d.%y"
        }
    },
    "series": [
        {
            "values": Values1
        },
        {
            "values": [
                5,
                30,
                21,
                18,
                59,
                50,
                28,
                33
            ]
        }
    ]
};


var RenderObj = {
    id: 'LineChart',
    data: LineConfig,
    height: '400',
    width: '100%'
};

zingchart.render(RenderObj);

