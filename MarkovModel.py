import random
import Helpers

'''
Class that creates a markov model using a adjacency matrix implementation containing transition probabilities.
Index 0 corresponds to the "initial" state
'''
class MarkovModel:
    step_size: float = 0.1
    probabilities: list
    thresholds: list
    categories: list
    num_choices: int = 1

    def __init__(self, categories):
        n = len(categories)
        self.probabilities = [([0.0] + [1/n for _ in categories]) for _ in range(len(categories) + 1)]
        self.thresholds = [[0.0] for i in range(len(self.probabilities) + 1)]
        self.categories = ["initial"] + categories
        self.update_thresholds()

    '''
    Updates the probability thresholds using the current self.probabilities matrix. self.thresholds is
    a cumulative matrix of probabilities
    '''
    def update_thresholds(self) -> None:
        self.thresholds = [[0] for _ in self.probabilities]
        for i in range(len(self.thresholds)):
            for probability in self.probabilities[i]:
                self.thresholds[i].append(self.thresholds[i][-1] + probability)

    '''
    Samples from a markov chain randomly, n describes the number of steps and the size of the return array
    '''
    def sample(self, n=3) -> list:
        curr_index = 0
        states = ["" for _ in range(n)]
        for i in range(n):
            rng_value = random.uniform(0, 1)
            curr_index = Helpers.threshold_index(rng_value, self.thresholds[curr_index])
            states[i] = self.categories[curr_index]

        return states

    def update_probabilities(self, choices: list) -> None:
        curr_state = "initial"
        for choice in choices:
            curr_index = self.categories.index(curr_state)
            going_index = self.categories.index(choice)
            probabilities = self.probabilities[curr_index]
            dec_step_size = self.step_size / (self.num_choices * (len(probabilities) - 1))

            updated_probabilities = [0 if (i == going_index or i == 0) else max(probabilities[going_index] - dec_step_size, 0.04)
                                     for i in range(len(probabilities))]
            updated_probabilities[going_index] = 1 - sum(updated_probabilities)
            self.probabilities[curr_index] = updated_probabilities

            curr_state = choice
        self.num_choices += 1
        self.thresholds = Helpers.get_thresholds(self.probabilities)
