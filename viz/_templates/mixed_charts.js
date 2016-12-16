/**
 * Created by kmu on 16.12.2016.
 */
zingchart.THEME = "classic";

var myConfig = {
  "type": "mixed", // 1. Specify your mixed chart type.
  "plot": {
    "tooltip": {
      "text": "%t"
    }
  },
  "series": [ // 2. Specify the chart type for each series object.
    {
      "type": "area",
      "values": [34, 70, 40, 75, 33, 50, 65],
      "aspect": "stepped",
      "contour-on-top": false,
      "text": "Area Chart"
    },
    {
      "type": "bar",
      "values": [49, 30, 21, 15, 59, 51, 69],
      "bar-width": "50%",
      "text": "Bar Chart"
    },
    {
      "type": "line",
      "values": [5, 9, 3, 19, 7, 15, 14],
      "aspect": "spline",
      "text": "Line Chart"
    }
  ]
};

zingchart.render({
  id: 'myChart',
  data: myConfig,
  height: 500,
  width: 725
});

