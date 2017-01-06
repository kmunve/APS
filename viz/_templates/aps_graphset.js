/**
 * Created by kmu on 06.01.2017.
 */


var time_axis = {
    "min-value": 1420232400000,
        "step": "day",
        "transform": {
            "type": "date",
            "all": "%D<br>%d %M %y"
        }
};


var danger_level = [1, 2, 2, 3, 3, 4, 3];


var DLchart = {
    "type": "bar",

    "plot": {
        //"aspect": "vertical",
        //"border-radius": "15px",
        "rules": [
            {
                "rule": "%v == 1",
                "background-color": "#75B100",
            },
            {
                "rule": "%v == 2",
                "background-color": "#FFCC33"
            },
            {
                "rule": "%v == 3",
                "background-color": "#E46900"
            },
            {
                "rule": "%v == 4",
                "background-color": "#D21523"
            },
            {
                "rule": "%v == 5",
                "background-color": "#000000"
            }
        ]
    },

    "tooltip": {
        "placement": "node:top",
        "text": "%vt"
    },

    "scale-x": time_axis,

    "scale-y": {
        "min-value": 0,
        "max-value": 5,
        "labels": ["Ikke gitt", "1-Liten", "2-Moderat", "3-Betydelig", "4-Stor", "5-Meget stor"]
    },


    "series": [
        {
            "values": danger_level
        }
    ]
};


var windslabs = [0, 1, 1, 2, 2, 0, 0];
var stormslabs = [1, 0, 0, 1, 1, 0, 0];
var pwl = [0, 0, 0, 0, 3, 1, 1];

var APchart = {
    "type": "heatmap",

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

    "scale-x": time_axis,

    "scale-y": {
        "mirrored": true,
        "labels": ["Fokksnø", "Nysnø", "VSL"]
    },



    "tooltip": {
      "text": "Skredproblemer"
    },

    "series": [
        {"values": windslabs},
        {"values": stormslabs},
        {"values": pwl}
    ]
};

var plotConfig =     { //root object
      gui:{
        contextMenu:{
            // handles options when the user right-clicks on the chart
        }
      },
      history:{

      },
      graphset:[DLchart, APchart]
    };



zingchart.render({
    id: 'GraphSet',
    data: plotConfig,
    height: 500,
    width: 725
});