/**
 * Created by kmu on 16.12.2016.
 */

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
            "values": [
                20,
                40,
                25,
                50,
                15,
                45,
                33,
                34
            ]
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

zingchart.render({
    id: 'LineChart',
    data: LineConfig,
    height: '100%',
    width: '100%'
});

