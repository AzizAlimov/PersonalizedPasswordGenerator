"""
Returns the index of thresholds where thresholds[index] < value < thresholds[index + 1]
"""
def threshold_index(value, thresholds) -> int:
    for i in range(len(thresholds)):
        if value <= thresholds[i]:
            return i - 1


"""
Updates the probability thresholds using the current self.probabilities matrix. self.thresholds is
a cumulative matrix of probabilities
"""
def get_thresholds(probabilities: list) -> list:
    thresholds = [[0] for _ in probabilities]
    for i in range(len(thresholds)):
        for probability in probabilities[i]:
            thresholds[i].append(thresholds[i][-1] + probability)

    return thresholds
