"""Preserved Boltzmann Wealth tutorial model from the official Mesa docs."""

import mesa


class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, model):
        super().__init__(model)
        self.wealth = 1

    def exchange(self):
        """Give one unit to a randomly selected agent when possible."""
        if self.wealth > 0:
            other_agent = self.random.choice(self.model.agents)
            if other_agent is not None:
                other_agent.wealth += 1
                self.wealth -= 1


class MoneyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, n=10):
        super().__init__()
        self.num_agents = n
        MoneyAgent.create_agents(model=self, n=n)

    def step(self):
        """Advance one model step by activating agents in random order."""
        self.agents.shuffle_do("exchange")
