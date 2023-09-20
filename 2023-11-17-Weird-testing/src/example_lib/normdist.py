import random


def sample_mean(dist: "NormalDistribution", sample_size: int) -> float:
    sample = dist.sample(sample_size)
    return sum(sample) / len(sample)


class NormalDistribution:
    def __init__(self, mean: float, variance: float):
        self.mean = mean
        self.variance = variance

    def sample(self, how_many: int) -> list[float]:
        return [random.normalvariate(self.mean, self.variance) for _ in range(how_many)]


    def recenter(self, bump: float) -> "NormalDistribution":
        return NormalDistribution(self.mean + bump, self.variance)
