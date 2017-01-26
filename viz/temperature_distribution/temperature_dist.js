/**
 * Created by kmu on 16.12.2016.
 */
zingchart.THEME = "classic";

var ForecastDate = "26 jan. 2017";

var ForecastRegion = "Salten";

var ElevIntervals = ["0-400", "400-800", "800-1200", "1200-1600", "1600-2000"];
var ElevPercentages = [56, 27, 14, 3, 0];
var TempElevData = [
    [-1.1, 1.95866668, 4.25, 6.635083, 8.7],
    [-1.6, 0.5003333, 3.2, 5.99133348, 8.2],
    [-3.7, -1.2955, 1.8, 4.7205, 7.8],
    [-6.1, -2.97675, -0.075, 1.81216669, 4.4],
    [-7.8, -3.97466683, -1.7, -0.05416667, 1.3]
];
var TempRange = "-10:10:5" // Min:Max:Step
var FreezingLevel = 1350;

var TempChart = {
        "type": "hboxplot",
        "background-color": "white",
        x: 0,  //position from left of chart edge
        y: 0,  //position top of chart
        height: "100%",
        width: "70%",

        "title": {
            "background-color": "none",
            //"text": "Temperaturfordeling for  Hallingdal (6 des. 2016)", // string needs to be constructed using variables ForecastRegion and ForecastDate
            "color": "black",
            "font-weight": "none",
            "font-size": 24,
            "offset-y": "5%"
        },
        "plotarea": {
            "margin-top": "10%",
            "margin-left": "25%",
            "margin-right": "1%"
        },
        "plot": {
            "bar-width": 50,
            "hover-state": {
                "visible": false
            }
        },
        "tooltip": {
            "paddingBottom": 5,
            "background-color": "darkgrey",
            "border-color": "lightgrey",
            "border-radius": 10,
            "text": "<span style=\"font-style:italic;\">Median temperatur i<br> høydeinterval: %kl</span>:<br><br><b style=\"font-size:18px;\">%data-median C</b><br><br>Maksimum: <b>%data-max</b><br>Øvre kvartil: <b>%data-upper-quartile</b><br>Nedre kvartil: <b>%data-lower-quartile</b><br>Minimum: <b>%data-min</b>"
        },
        "scale-x": {
            "label": {
                "text": "Høydeintervall",
                "font-size": 14,
                "font-color": "darkgrey"
            },
            "offset-start": 0,
            "offset-end": 0,
            "line-color": "none",
            "labels": ElevIntervals,
            "format": "%v<br>moh",
            "tick": {
                "visible": false
            },
            "item": {
                "font-size": 14
            },
            "guide": {
                "visible": false
            }
        },
        "scale-y": {
            "label": {
                "text": "Temperatur (Celsius)",
                "font-size": 14,
                "font-color": "darkgrey"
            },
            "offset-start": 20,
            "offset-end": 20,
            "values": TempRange,
            "ref-value": 0,
            "ref-line": {
                "visible": true,
                "line-color": "darkgrey",
                "line-width": 2,
                "line-style": "solid"
            },
            "format": "%v C",
            "line-color": "darkgrey",
            "tick": {
                "line-color": "darkgrey"
            },
            "item": {
                "font-size": 14
            },
            "guide": {
                "visible": true
            }
        },
        "options": {
            "box": {
                "border-color": "black",
                "border-width": 1,
                "background-color": "lightgrey",
                "rules": [{
                    "rule": "%data-median >= 0",
                    "background-color": "red"
                }, {
                    "rule": "%data-median < 0",
                    "background-color": "lightblue"
                }]
            }
            ,
            "line-median-level": {
                "line-color": "black",
                "line-width": 2
            }
            ,
            "line-min-level": {
                "line-color": "black",
                "line-width": 1
            }
            ,
            "line-min-connector": {
                "line-color": "black",
                "line-width": 1
            }
            ,
            "line-max-level": {
                "line-color": "black",
                "line-width": 1
            }
            ,
            "line-max-connector": {
                "line-color": "black",
                "line-width": 1
            }
        }
        ,
        "series": [{
            "data-box": TempElevData
        }]
    }
    ;

var PercChart = {
    type: "hbar",
    backgroundColor: "white",
    x: "70%",  //position from left of chart edge
    y: 0,  //position top of chart
    height: "100%",
    width: "30%",

    /*"plotarea": {
     "adjust-layout": true /!* For automatic margin adjustment. *!/
     },*/
    "plot": {
        //"aspect": "stepped"

    },

    "scale-x": {
        "offset-start": 0,
        "offset-end": 0,
        "line-color": "none",
        "tick": {
            "visible": false
        },
        "guide": {
            "visible": false
        },
        "item": {
            "visible": false
        },

    },
    "scale-y": {
        "label": {
            "text": "Areal i høydesonen",
            "font-size": 14,
            "font-color": "darkgrey"
        },
        "offset-start": 0,
        "offset-end": 0,
        "format": "%v %",
        "line-color": "darkgrey",
        "tick": {
            "line-color": "darkgrey"
        },
        "item": {
            "font-size": 14
        },
        "guide": {
            "visible": true
        }
    },
    "series": [
        {
            "values": ElevPercentages,
            "background-color": "darkgrey",
            "line-color": "none",
            "alpha": 0.5,
            "bar-width": "100%",
            "bars-space-left": 0,
            "bars-space-right": 0
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
    "layout": "horizontal",
    graphset: [TempChart, PercChart]
};

var renderObj = {
    id: 'TempElevChart',
    data: plotConfig,
    height: 500,
    width: 700
};

//zingchart.render(renderObj);