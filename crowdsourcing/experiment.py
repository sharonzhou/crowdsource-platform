import numpy as np


class ExperimentConfig(object):
    TYPE_UNIFORM = 'uniform'
    TYPE_WEIGHTED = 'weighted'
    TYPES = [TYPE_UNIFORM, TYPE_WEIGHTED]

    def __init__(self, config):
        if type(config) != dict:
            raise TypeError("Config must be a dictionary")
        if 'type' not in config or config['type'] not in self.TYPES:
            raise ValueError("Invalid or missing `type`")
        if 'choices' not in config and len(config['choices']) == 0:
            raise ValueError("Choices not provided")

        self.type = config['type']
        self.raw_choices = config['choices']
        if 'conditions' in config:
            self.conditions = config['conditions']
        else:
            self.conditions = []
        self.choices = []
        self.weights = []

    def assign(self):
        self._parse_choices()
        result = {
            'selected': None
        }
        if self.type == self.TYPE_UNIFORM:
            result['selected'] = str(self.uniform())
        else:
            result['selected'] = str(self.weighted())
        return result

    def _parse_choices(self):
        for d in self.raw_choices:
            self.choices.append(d['value'])
            if 'weight' in d:
                self.weights.append(d['weight'])

    def uniform(self):
        return np.random.choice(self.choices)

    def weighted(self):
        return np.random.choice(self.choices, p=self.weights)
