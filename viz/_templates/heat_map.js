/**
 * Created by kmu on 06.01.2017.
 */

var windslabs = [0, 1, 1, 2, 2, 0, 0];
var stormslabs = [1, 0, 0, 1, 1, 0, 0];
var pwl = [0, 0, 0, 0, 3, 1, 1];

var plotConfig = {
    "type": "heatmap",
    "text": "Skredproblemer",
    "plot": {
        "aspect": "none",
        "border-radius": "15px",
        "background-color": "darkblue",
        "rules": [
            {
                "rule": "%v == 1",
                "alpha": 1.0
            },
            {
                "rule": "%v == 2",
                "alpha": 0.7
            },
            {
                "rule": "%v == 3",
                "alpha": 0.4
            },
            {
                "rule": "%v == 0",
                "background-color": "white"
            }
        ]
    },

    "scale-y": {
        "mirrored": true,
        "labels": ["Fokksnø", "Nysnø", "VSL"]
    },

    "scale-x": {
        "labels": ["Søn", "Man", "Tir", "Ons", "Tor", "Fre", "Lør"],  //X-Axis Scale Labels
        "line-color": "none",   //Axis Lines
        "guide": {              //Plot Lines
            "visible": true
        },
        "tick": {               //Tick Marks
            "visible": false
        },
        "placement": "opposite" //To change the placement of your axis.
    },

    "series": [
        {"values": windslabs},
        {"values": stormslabs},
        {"values": pwl}
    ]
};

var renderObj = {
    id: 'HeatMap',
    data: plotConfig,
    height: "400",
    width: "100%"
};

zingchart.render(renderObj);

