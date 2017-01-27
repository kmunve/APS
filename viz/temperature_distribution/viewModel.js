angular.module('APS', ['zingchart-angularjs'])
    .controller('DistributionByDateController', ['$scope', '$filter', '$http', function ($self, $filter, $http) {

        $self.init = function (model) {
            $self.regions = model.Regions;
            $self.fromDate = new Date(model.FromDate);
            $self.toDate = new Date(model.ToDate);
        }

        $self.selectedRegion = null;

        $self.submitForm = function () {
            var formattedFromDate = $filter('date')($self.fromDate, "yyyy-MM-dd");

            var url = "http://tst-h-int-api01/APSServices/TimeSeriesReader.svc/DistributionByDate/met_obs_v2.0/17/24/" + $self.selectedRegion + "/" + formattedFromDate + "/" + formattedFromDate;

            zingchart.THEME = "classic";
            zingchart.MODULESDIR = "https://cdn.zingchart.com/modules/";


            var tempBoxChartConfig = {

                "type": "hmixed",
                "background-color": "white",
                "title": {
                    "background-color": "none",
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


                "series": [

                    {
                        "type": "hboxplot",

                        "tooltip": {
                            "paddingBottom": 5,
                            "background-color": "darkgrey",
                            "border-color": "lightgrey",
                            "border-radius": 10,
                            "text": "<span style=\"font-style:italic;\">Median temperatur i<br> h�ydeinterval: %kl</span>:<br><br><b style=\"font-size:18px;\">%data-median C</b><br><br>Maksimum: <b>%data-max</b><br>�vre kvartil: <b>%data-upper-quartile</b><br>Nedre kvartil: <b>%data-lower-quartile</b><br>Minimum: <b>%data-min</b>"
                        },
                        "scale-x": {
                            "label": {
                                "text": "H�ydeintervall",
                                "font-size": 14,
                                "font-color": "darkgrey"
                            },
                            "offset-start": 20,
                            "offset-end": 20,
                            "line-color": "none",
                            "labels": [],
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
                            "values": "-20:20:2",
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
                                "background-color": "lightblue",
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
                    },

                    {
                        "type": "bar",
                        "values": [5, 3, -10, 1, 9],
                        "bar-width": "50%",
                        "text": "Bar Chart"

                    }]
            };


            $.ajax({
                method: 'GET',
                dataType: 'json',
                crossDomain: true,
                url: url
            })
                .done(function (data, status) {
                    if (status === 'error' || !data) {
                        alert("Kune ikke hente data for generering av plot");
                        return;
                    }


                    var region = data.TimeLine[0].Regions[0].RegionName;

                    tempBoxChartConfig.title.text = "Temperaturfordeling for " + region + " (" + $filter('date')($self.fromDate, "d. MMM. yyyy") + ")";


                    var elevations = [];
                    var arealprecentage = [];
                    var tempElevData = [];
                    var min = 999;
                    var max = -999;
                    angular.forEach(data.TimeLine[0].Regions[0].ElevationData, function (element) {
                        elevations.push(element.ElevationBottom + "-" + element.ElevationTop + "(" + element.ArealPercentage + "%)");
                        arealprecentage.push(element.ArealPercentage);
                        if (element.Minimum < min) min = element.Minimum;
                        if (element.Maximum > max) max = element.Maximum;
                        tempElevData.push([
                            Math.round(element.Minimum * 100) / 100,
                            Math.round(element.FirstQuartile * 100) / 100,
                            Math.round(element.Median * 100) / 100,
                            Math.round(element.ThirdQuartile * 100) / 100,
                            Math.round(element.Maximum * 100) / 100
                        ]);
                    });

                    var roundedMin = (Math.floor(min / 10)) * 10;
                    var roundedMax = (Math.ceil(max / 10)) * 10;

                    var arealPerc = roundedMin + (roundedMax + Math.abs(roundedMin)) * (arealprecentage / 100)

                    var containsPrognosis = data.TimeLine[0].ContainsPrognosis;
                    var exclusivelyPrognosis = data.TimeLine[0].ExclusivelyPrognosis;

                    tempBoxChartConfig["scale-y"].values = roundedMin + ":" + roundedMax + ":" + "2";
                    tempBoxChartConfig["scale-x"].labels = elevations;
                    tempBoxChartConfig.series = [{"data-box": tempElevData}];


                    var renderObj = {
                        id: 'TempElevChart',
                        data: tempBoxChartConfig,
                        height: 500,
                        width: 700
                    };

                    zingchart.render(renderObj);

                });

        };

    }]);

