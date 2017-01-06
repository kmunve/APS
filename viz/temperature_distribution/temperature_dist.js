/**
 * Created by kmu on 16.12.2016.
 */
zingchart.THEME = "classic";
var myConfig = {
        "type": "hboxplot",
        "background-color": "white",
        "title": {
            "background-color": "none",
            "text": "Temperaturfordeling for Hallingdal (6 des. 2016)",
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
            "label": {
                "text": "Høydeintervall",
                "font-size": 14,
                "font-color": "darkgrey"
            },
            "offset-start": 20,
            "offset-end": 20,
            "line-color": "none",
            "labels": ["0-400", "400-800", "800-1200", "1200-1600", "1600-2000"],
            "format": "%v moh",
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
            "values": "-10:2:2",
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
                    "rule": "%i == 0",
                    "background-color": "#9A8AAD"
                }, {
                    "rule": "%i == 1",
                    "background-color": "#9A8AAD"
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
            "data-box": [
                [-0.500, -0.233, 0.000, 0.233, 0.400],
                [-2.200, -1.733, -1.200, -0.666, -0.200],
                [-4.699, -3.958, -3.150, -2.341, -1.500],
                [-7.199, -6.383, -5.500, -4.616, -3.799],
                [-8.199, -7.683, -7.199, -6.716, -6.300]
            ]
        }]
    }
    ;

zingchart.render({
    id: 'myChart',
    data: myConfig,
    height: 500,
    width: 725
});