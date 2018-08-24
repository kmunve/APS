import numpy as np
import matplotlib.pyplot as plt
import json

with open('training_score.json') as json_data:
    score = json.load(json_data)
    print(score)

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

ts = get_score_range(position, size, distribution, trigger, probability, dangerlevel)
print(ts.max())
plt.plot(ts)
plt.show()
