/**
 * Created by kmu on 16.05.2017.
 */
var calm = [5.430555555555556, 0.31222222222222223, 0.12694444444444444, 0.15972222222222224, 0.03805555555555555, 0.7244444444444444, 6.1402777777777775, 25.324999999999996];
var breeze = [8.426944444444445, 0.036944444444444446, 0.0, 0.0, 0.0, 0.014444444444444444, 0.9191666666666667, 51.24583333333334];
var fresh_breeze = [];
var strong_breeze = [];
var high_wind = [];
var gale = [0.07888888888888888, 0.0002777777777777778, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9722222222222222];
var strong_gale = [];
var storm = [0.0005555555555555556, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.010277777777777778];
var hurricane = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];


var myConfig = {
  "type": "radar",

  "legend": {
    //"x": "0px",
    //"y": "50px",
    //"width": "125px",
    "padding": "10px 12px",
    "background-color": "#f8f8f8",
    "shadow": false,
    "item": {
      "font-family": "Arial",
      "font-size": "12px",
      "font-weight": "normal"
    },

    "header": {
      "text": "Vindstyrke"
    },
    /*
            "footer":{
              "text":"Footer"
            },
            */
    //"max-items":3,
    //"overflow":"page",
    "minimize": true,
    /*
      "highlight-plot":true,
      "minimize":true,
      "draggable":true
    */
  },

  "plot": {
    "aspect": "rose",
    "stacked": true
  },
  "scale-v": { //in percent
    "values": "0:100:25",
    "format": "%v %"
  },

  "scale-k": {
    "values": "0:315:45",
    "labels": ["N", "NØ", "Ø", "SØ", "S", "SV", "V", "NV"],
    "format": "%v",
    "aspect": "circle", //To set the chart shape to circular.
    "guide": {
      "line-style": "solid",
      "background-color": "#f8f8f8"
    }
  },

  "series": [{
    "values": calm, // stille
    "background-color": "#CCFFFF",
    "text": "stille / svak vind",
    "legend-marker": {
      "background-color": "#CCFFFF",
    }
  }, {
    "values": breeze, //bris
    "background-color": "#99FF99",
    "text": "bris",
    "legend-marker": {
      "background-color": "#99FF99",
    }
  }, {
    "values": fresh_breeze, // frisk bris
    "background-color": "#99FF00",
    "text": "frisk bris",
    "legend-marker": {
      "background-color": "#99FF00",
    }
  }, {
    "values": strong_breeze, //liten kuling
    "background-color": "#CCFF00",
    "text": "liten kuling",
    "legend-marker": {
      "background-color": "#CCFF00",
    }
  }, {
    "values": high_wind, // stiv kuling
    "background-color": "#FFFF00",
    "text": "stiv kuling",
    "legend-marker": {
      "background-color": "#FFFF00",
    }
  }, {
    "values": gale, //sterk kuling
    "background-color": "#FFCC00",
    "text": "sterk kuling",
    "legend-marker": {
      "background-color": "#FFCC00",
    }
  }, {
    "values": strong_gale, // liten storm
    "background-color": "#FFFF00",
    "text": "liten storm",
    "legend-marker": {
      "background-color": "#FFFF00",
    }
  }, {
    "values": storm, // storm
    "background-color": "#FF6600",
    "text": "storm",
    "legend-marker": {
      "background-color": "#FF6600",
    }
  }, {
    "values": hurricane, // orkan
    "background-color": "#FF3300",
    "text": "orkan",
    "legend-marker": {
      "background-color": "#FF3300",
    }
  }]
};

zingchart.render({
  id: 'myChart',
  data: myConfig,
  height: '100%',
  width: '100%'
});