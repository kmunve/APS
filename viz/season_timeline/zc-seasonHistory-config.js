zingchart.MODULESDIR = "https://cdn.zingchart.com/modules/";
zingchart.THEME = "classic";
ZC.LICENSE = ["569d52cefae586f634c54f86dc99e6a9", "ee6b7db5b51705a13dc2339db3edaf6d"];


var time_axis = {
    "min-value": 1420232400000,
    "step": "day",
    "transform": {
        "type": "date",
        "all": "%D<br>%d %M %y"
    }
};

var time_axis_2 = {
    "min-value": 1420232400000,
    "step": "day",
    "transform": {
        "type": "date",
        "all": "%D<br>%d %M %y"
    }
};


var season_plotarea = {
    marginLeft: 150,
    marginRight: 150,
    marginTop: 20,
    marginBottom: 50
};


// Heat map showing the danger level
var DLchart = {
    "type": "heatmap",
    backgroundColor: "white",
    x: 0,  //position from left of chart edge
    width: "100%",
    "scale-x": time_axis,

    plotarea: season_plotarea,

    "plot": {
        "aspect": "none",
        "border-radius": "15px",
        "rules": [
            {
                "rule": "%v == 0",
                "background-color": "silver",
                //"alpha": 0
            },
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
        "wrap-text": true,
        "width": "250px",
        "text": "%data-ttText"
    },

    "scale-y": {
        "mirrored": true,
        "labels": ["Faregrad"]
    }
};


// Heat map showing the avalanche problems
var APchart1 = {
    "type": "heatmap",
    backgroundColor: "white",
    x: 0,  //position from left of chart edge
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
                "alpha": 0.5
            },
            {
                "rule": "%v == 3",
                "alpha": 0.1
            },
            {
                "rule": "%v == 0",
                "background-color": "white"
            },
            {
                "rule": "%v == null",
                "background-color": "white"
            }
        ]
    },


    "scale-x": time_axis,

    "scale-y": {
        "mirrored": true
    },



    "series": []
};

var APchart2 = {
    "type": "heatmap",
    backgroundColor: "white",
    x: 0,  //position from left of chart edge
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
                "alpha": 0.5
            },
            {
                "rule": "%v == 3",
                "alpha": 0.1
            },
            {
                "rule": "%v == 0",
                "background-color": "white"
            },
            {
                "rule": "%v == null",
                "background-color": "white"
            }
        ]
    },

    "scale-x": time_axis,

    "scale-y": {
        "mirrored": true
    },



    "series": []
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
    "values": "0:2000:200",
    "label": {
        text: "Null-isoterm (moh)"
    }
};

// Bar and line plots showing the regional meteorological conditions
var METchart = {

    "type": "mixed", // 1. Specify your mixed chart type.
    backgroundColor: "white",
    x: 0,  //position from left of chart edge

    width: "100%",
    "scale-x": time_axis_2,

    plotarea: season_plotarea,

    "plot": {
        "tooltip": {
            "text": "%t"
        }
    },

    "utc": true,
    "timezone": +1,
    "crosshair-x": {
        "plot-label": {
            "multiple": true
        },
        "scale-label": {
            "text": "%v",
            "transform": {
                "type": "date",
                "all": "%D,<br>%M %d, %Y"
            }
        }
    },

    "scale-y": precip_axis,

    "scale-y-2": temperature_axis,



    "series": [ // 2. Specify the chart type for each series object.
        {
            "type": "bar",
            "scales": "scale-x, scale-y",
            "stacked": true,
            "values": [],
            "background-color": "#9eb2c7",
            //"text": "Nedbør i hele regionen",
            //"tooltip": {
            //    "text": "%v mm"
            //},
            "bar-width": "100%",
            "guide-label": { //for crosshair plot labels
                "visible": false,
                "decimals": 2
            }
        },
        {
            "type": "bar",
            "scales": "scale-x, scale-y",
            stacked: true,
            "values": [],
            "background-color": "#b41216",
            //"text": "Nedbør i mest utsatt område",
            //"tooltip": {
            //    "text": "%data-ApsPrecipitationMostExposedArea mm"
            //},
            "bar-width": "100%",
            "guide-label": { //for crosshair plot labels
                "visible": false,
                "decimals": 2
            }
        },
        {
            "type": "line",
            "scales": "scale-x, scale-y-2",
            "values": [],
            "aspect": "spline",
            //"text": "Temperatur",
            //"tooltip": {
            //    "text": "%v°C"
            //},
            "guide-label": { //for crosshair plot labels
                "text": "Temperatur: %v°C<br>" +
                        "Nedbør i hele regionen: %data-ApsPrecipitation mm<br>" +
                        "Nedbør i mest utsatt område: %data-ApsPrecipitationMostExposedArea mm",
                "decimals": 2
            },
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
        },
        {
            "type": "range",
            "values": [],
            "aspect": "spline",
            "scales": "scale-x, scale-y-2",
            "backgroundColor": "#D7E9F9",
            "lineWidth": 0,
            "marker": {
                "visible": false
            },
            "tooltip": {
                "visible": false
            },
            "guideLabel": {
                "visible": false
            }
        }

    ]
};

var ZeroPointchart = {

    "type": "mixed", // 1. Specify your mixed chart type.
    backgroundColor: "white",
    x: 0,  //position from left of chart edge

    width: "100%",
    "scale-x": time_axis,

    plotarea: season_plotarea,

    "plot": {
        "tooltip": {
            "text": "%t"
        }
    },

    "utc": true,
    "timezone": +1,


    "scale-y": elevation_axis,
    "crosshair-x": {
        "plot-label": {
            "multiple": true
        },
        "scale-label": {
            "text": "%v",
            "transform": {
                "type": "date",
                "all": "%D,<br>%M %d, %Y"
            }
        }
    },

    "series": [ // 2. Specify the chart type for each series object.
        {
            "type": "area",
            "scales": "scale-x, scale-y",
            "values": [0, 0, 200, 550, 670, 310, 69],
            "aspect": "spline",
            "contour-on-top": false,
            "text": "Nullgradersgrense",
            "background-color": "#83b480",
            "line-color": "#83b480",
            "marker": {
                visible: false
            },
            //"tooltip": {
            //    "text": "%v moh"
            //},
            "guide-label": { //for crosshair plot labels
                "text": "%v moh",
                "decimals": 2
            },
        }
    ]
};

var renderSeason = {
    id: 'GraphSet',
    data: {
        gui: { contextMenu: {} },
        history: {},
        "layout": "vertical",
        graphset: [DLchart, APchart1, APchart2, METchart, ZeroPointchart]
    },
    width: "90%"
};


// Graph size settings
DLchart.y =  0;
DLchart.height = 100;

APchart1.y = DLchart.y + DLchart.height;
APchart1.height = 240;

APchart2.y =  APchart1.y + APchart1.height;
APchart2.height = 300;

METchart.y = APchart2.y + APchart2.height;
METchart.height = 300;

ZeroPointchart.y = METchart.y + METchart.height;
ZeroPointchart.height = 200;

renderSeason.height = ZeroPointchart.y + ZeroPointchart.height + 100;

