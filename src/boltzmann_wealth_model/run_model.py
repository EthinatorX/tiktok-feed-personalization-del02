"""Run the preserved Mesa Boltzmann Wealth source example from the terminal."""

from model import MoneyModel


def main():
    model = MoneyModel(10)
    for _ in range(30):
        model.step()
    wealth = [agent.wealth for agent in model.agents]
    print("Boltzmann Wealth Model — wealth after 30 steps")
    print(wealth)
    print(f"Total wealth: {sum(wealth)}")


if __name__ == "__main__":
    main()
