import numpy as np
import matplotlib.pyplot as plt
import json
import os.path


class APSTrainingScore:

    def __init__(self):
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'training_score.json')
        with open(self.filename) as json_data:
            self.score_dict = json.load(json_data)


    def get_score(self, position, size, distribution, trigger, probability, dangerlevel):
        pos = self.score_dict['AvalancheProblemId'][str(int(position))]
        s = self.score_dict['DestructiveSizeExtId'][str(int(size))]
        d = self.score_dict['AvalPropagationId'][str(int(distribution))]
        t = self.score_dict['AvalTriggerSimpleId'][str(int(trigger))]
        p = self.score_dict['AvalProbabilityId'][str(int(probability))]
        dl = self.score_dict['DangerLevel'][str(int(dangerlevel))]

        self.score = pos + (s * d) + (t * p) + dl



def load_config():
    filename = 'training_score.json'
    with open(filename) as json_data:
        score = json.load(json_data)

    distribution = np.array(list(score['AvalPropagationId'].values())) # why is it called "propagation"?
    size = np.array(list(score['DestructiveSizeExtId'].values()))
    trigger = np.array(list(score['AvalTriggerSimpleId'].values()))
    probability = np.array(list(score['AvalProbabilityId'].values()))
    position = np.array(list(score['AvalancheProblemId'].values()))
    dangerlevel = np.array(list(score['DangerLevel'].values()))




def get_score(position, size, distribution, trigger, probability, dangerlevel):
    return position + (size * distribution) + (trigger * probability) + dangerlevel


def get_score_range(position, size, distribution, trigger, probability, dangerlevel):
    score_range = []
    for d in distribution:
        for s in size:
            for t in trigger:
                for p in probability:
                    for pos in position:
                        for dl in dangerlevel:
                            score_range.append(get_score(pos, s, d, t, p, dl))
    return np.array(score_range)


if __name__ == "__main__":
    position, size, distribution, trigger, probability, dangerlevel = load_config()
    ts = get_score_range(position, size, distribution, trigger, probability, dangerlevel)
    print(ts.max())
    plt.plot(ts)
    plt.show()
