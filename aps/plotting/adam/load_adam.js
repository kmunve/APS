/**
 * Created by kmu on 01.11.2016.
 */

var adam = {
    "ADAM": {

        "SensitivityToTriggers": {
            "Unreactive": {
                "natural_trigger": "No avalanches",
                "human_trigger": "No avalanches"
            },
            "Stubborn": {
                "natural_trigger": "Few",
                "human_trigger": "Difficult to trigger"
            },
            "Reactive": {
                "natural_trigger": "Several",
                "human_trigger": "Easy to trigger"
            },
            "Touchy": {
                "natural_trigger": "Numerous",
                "human_trigger": " Triggering almost certain"
            }
        },

        "SpatialDistribution": "Isolated"
    }
};


function load() {
    var adam_def = JSON.parse(adam);
    alert(adam_def.ADAM.SensitivityToTriggers.Unreactive.natural_trigger);
    alert(adam_def.ADAM.SpatialDistribution);
}