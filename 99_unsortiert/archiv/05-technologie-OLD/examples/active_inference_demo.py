"""
Active Inference: Minimal Working Example
Reference: Friston 2010, DOI:10.1016/j.neuroimage.2008.02.054
"""


class ActiveInferenceAgent:
    """Agent minimiert Überraschung durch Vorhersage.

    Implements Free Energy Principle:
    Agents minimize prediction error by updating internal models.
    """

    def __init__(self, learning_rate: float = 0.1):
        self.lr = learning_rate
        self.prediction = 0.5  # Prior belief

    def observe(self, observation: float) -> float:
        """Bayesian Update der Vorhersage.

        Args:
            observation: Sensory input (0-1 scale)

        Returns:
            Absolute prediction error
        """
        prediction_error = observation - self.prediction
        self.prediction += self.lr * prediction_error
        return abs(prediction_error)


# Example Usage
if __name__ == "__main__":
    agent = ActiveInferenceAgent()
    observations = [0.8, 0.7, 0.9, 0.85]

    print("Iteration | Observation | Prediction | Error")
    print("-" * 50)
    for i, obs in enumerate(observations):
        error = agent.observe(obs)
        print(f"{i+1:9} | {obs:11.2f} | {agent.prediction:10.2f} | {error:5.2f}")
