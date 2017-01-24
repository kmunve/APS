/**
 * Created by kmu on 24.01.2017.
 */

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

var season_plotarea = {
        marginLeft: 100,
        marginRight: 150
    };

var danger_level = [1, 2, 2, 3, 3, 4, 3];

// Heat map showing the danger level
var DLchart = {
    "type": "heatmap",
    backgroundColor: "white",
    x: 0,  //position from left of chart edge
    y: "0%",  //position top of chart
    height: "20%",
    width: "100%",

    plotarea: season_plotarea,

    "plot": {
        "aspect": "none",
        "border-radius": "15px",
        "rules": [
            {
                "rule": "%v == 1",
                "background-color": "#75B100"
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
        "mirrored": true,
        "labels": ["Faregrad"]
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

// Heat map showing the avalanche problems
var APchart = {
    "type": "heatmap",
    backgroundColor: "white",
    x: 0,  //position from left of chart edge
    y: "20%",  //position top of chart
    height: "30%",
    width: "100%",

    plotarea: season_plotarea,

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


///////////////
// MET CHART //
///////////////


var precip_axis = {
    "values": "0.0:60:5", //Min/Max/Step
    "label": {
        text: "Nedbør (mm)"
    }
};

var temperature_axis = {
    "values": "-20:10:5",
    "label": {
        text: "Temperatur (C)"
    }
};

var elevation_axis = {
    "values": "0:2000:300",
    "label": {
        text: "Høyde over havet (m)"
    }
};

// Bar and line plots showing the regional meteorological conditions
var METchart = {

    "type": "mixed", // 1. Specify your mixed chart type.
    backgroundColor: "white",
    x: 0,  //position from left of chart edge
    y: "50%",  //position top of chart
    height: "50%",
    width: "100%",

    plotarea: season_plotarea,

    "plot": {
        "tooltip": {
            "text": "%t"
        }
    },

    "utc": true,
    "timezone": +1,

    "scale-x": time_axis,

    "scale-y": precip_axis,

    "scale-y-2": temperature_axis,

    "scale-y-3": elevation_axis,


    "series": [ // 2. Specify the chart type for each series object.
        {
            "type": "area",
            "scales": "scale-x, scale-y-3",
            "values": [0, 0, 200, 550, 670, 310, 69],
            "aspect": "spline",
            "contour-on-top": false,
            "text": "Nullgradersgrense",
            "background-color": "#83b480",
            "line-color": "#83b480",
            "marker": {
                visible: false
            }
        },
        {
            "type": "bar",
            "scales": "scale-x, scale-y",

            "values": [34, 70, 4, 0, 0, 5, 6],
            "background-color": "#b41216",
            "text": "regn",
            "tooltip": {
                "text": "%v mm %t"
            },
            "bar-width": "50%"
        },
        {
            "type": "bar",
            "scales": "scale-x, scale-y",

            "values": [15, 30, 20, 75, 33, 5, 7],
            "background-color": "#9eb2c7",
            "text": "snø",
            "tooltip": {
                "text": "%v mm %t"
            },
            "bar-width": "50%"
        },
        {
            "type": "line",
            "scales": "scale-x, scale-y-2",
            "values": [-5, -9, -3, 1, 7, 5, -4],
            "aspect": "spline",
            "text": "Temperatur",
            "marker": {
                "rules": [
                    {
                        "rule": "%v >= 0",
                        "background-color": "#e82818"
                    },
                    {
                        "rule": "%v < 0",
                        "background-color": "#0a2b90"
                    }
                ],

                "size": 6, /* in pixels */
                "border-color": "none", /* hexadecimal or RBG value */
                "border-width": 0 /* in pixels */
            },
            "rules": [
                {
                    "rule": "%v >= 0",
                    "line-color": "#e82818"
                },
                {
                    "rule": "%v < 0",
                    "line-color": "#0a2b90"
                }
            ]
        }
    ]
};


var plotConfig = { //root object
    gui: {
        contextMenu: {
            // handles options when the user right-clicks on the chart
        }
    },
    history: {},
    "layout": "vertical",
    graphset: [DLchart, APchart, METchart]
};


var renderSeason = {
    id: 'GraphSet',
    data: plotConfig,
    height: 1000,
    width: "90%"
};

//zingchart.render(renderSeason);