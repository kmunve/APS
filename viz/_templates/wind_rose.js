/**
 * Created by kmu on 02.05.2017.
 */
var no_transport = [5.430555555555556, 0.31222222222222223, 0.12694444444444444, 0.15972222222222224, 0.03805555555555555, 0.7244444444444444, 6.1402777777777775, 25.324999999999996];
var snowfall = [8.426944444444445, 0.036944444444444446, 0.0, 0.0, 0.0, 0.014444444444444444, 0.9191666666666667, 51.24583333333334];
var dry_snow = [0.07888888888888888, 0.0002777777777777778, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9722222222222222];
var wet_snow = [0.0005555555555555556, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.010277777777777778];
var all_snow = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];


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
      "text": "Vindhastighet"
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
    "values": no_transport, //[2.856666666666667, 7.839583333333334, 9.354999999999999, 15.171666666666667, 3.120416666666667, 25.271250000000002, 9.501666666666667, 2.327916666666667], // 0-5.5> m/s calm - gentle snowfall
    "background-color": "#969696",
    "text": "Ingen transport",
    "legend-marker": {
      "background-color": "#969696",
    }
  }, {
    "values": snowfall, //[0.0, 1.7325, 1.8641666666666667, 5.78375, 1.30125, 8.038333333333334, 2.1087499999999997, 0.0], // 5.5-13.8> m/s moderate to strong snowfall
    "background-color": "#fafa32",
    "text": "Ved snøfall",
    "legend-marker": {
      "background-color": "#fafa32",
    }
  }, {
    "values": dry_snow, //[0.0, 0.0, 0.0, 0.02375, 0.0, 0.0004166666666666667, 0.050416666666666665, 0.0], // 13.9-20.7> m/s dry_snow
    "background-color": "#64a0ff",
    "text": "Kun tørr snø",
    "legend-marker": {
      "background-color": "#64a0ff",
    }
  }, {
    "values": wet_snow, //[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], // 20.7-32.6> m/s strong dry_snow / wet_snow
    "background-color": "#ff6400",
    "text": "Også våt snø",
    "legend-marker": {
      "background-color": "#ff6400",
    }
  }, {
    "values": all_snow, //[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], // >32.6 m/s all_snow
    "background-color": "#0a0a0a",
    "text": "Hvis ikke skare/avblåst",
    "legend-marker": {
      "background-color": "#0a0a0a",
    }
  }]
};

zingchart.render({
  id: 'myChart',
  data: myConfig,
  height: '100%',
  width: '100%'
});