/**
 * Created by kmu on 10.01.2017.
 */


/**
 * Created by kmu on 16.12.2016.
 */
zingchart.THEME = "classic";

var ForecastDates = ["01. jan 2017", "02. jan 2017"];

var ForecastRegion = "Hallingdal";

var ElevIntervals = ["0-400", "400-800", "800-1200", "1200-1600", "1600-2000"];

var BoxData = [
    [9.9, 13.5, 21.6000003815, 26.5, 39.2],
    [0.3, 35.2999992371, 37.9500007629, 38.2000007629, 39.2]
];

var plotConfig = {
        "type": "boxplot",
        "background-color": "white",
        "title": {
            "background-color": "none",
            "text": "Nedbør i regionen", // string needs to be constructed using variables ForecastRegion and ForecastDate
            "color": "black",
            "font-weight": "none",
            "font-size": 24,
            "offset-y": "5%"
        },
        "plotarea": {
            "margin-top": "10%",
            "margin-left": "25%",
            "margin-right": "12%"
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
            "labels": ["I hele<br>regionen", "I mest<br>utsatt område"],
            "offset-start": 20,
            "offset-end": 20,
            "line-color": "none",
            "format": "%v",
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
                "text": "Nedbør (mm)",
                "font-size": 14,
                "font-color": "darkgrey"
            },
            "offset-start": 20,
            "offset-end": 20,
            "values": "0:100:5",
            "format": "%v mm",
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
                    "rule": "%i == 0",
                    "background-color": "darkgrey"
                }, {
                    "rule": "%i == 1",
                    "background-color": "red"
                }, {
                    "rule": "%i == 2",
                    "background-color": "#9A8AAD"
                }, {
                    "rule": "%i == 3",
                    "background-color": "#9A8AAD"
                }, {
                    "rule": "%i == 4",
                    "background-color": "#9A8AAD"
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
            "data-box": BoxData
        }]
    }
    ;

var renderObj = {
    id: 'BoxPlot',
    data: plotConfig,
    height: 500,
    width: 700
};

zingchart.render(renderObj);