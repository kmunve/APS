/**
 * Created by kmu on 06.01.2017.
 */


var danger_level = [1, 2, 2, 3, 3, 4, 3]


var plotConfig = {
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

    "scale-y": {
        "min-value": 0,
        "max-value": 5,
        "labels": ["Ikke gitt", "1-Liten", "2-Moderat", "3-Betydelig", "4-Stor", "5-Meget stor"]
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
        {
            "values": danger_level
        }
    ]
}


var renderObj = {
    id: 'BarChart',
    data: plotConfig,
    height: "400",
    width: "100%"
    //defaultsurl: '../aps_chart_theme.txt'
};


var renderSmall = {
    id: 'BarChart',
    data: plotConfig,
    height: "400",
    width: "700"
};

//zingchart.render(renderObj); //comment when plot should be loaded interactively
