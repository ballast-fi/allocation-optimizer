import utils
import web3Feeds
import models


def checkCost(bestAllocation):
    """Get the gas cost (in USD equivalent) for executing a given allocation

    Args:
        bestAllocation (dict): [description]

    Returns:
        int: The cost in USD equivalent of ether
    """
    gas_price = web3Feeds.getGasPrice()
    eth_price = web3Feeds.getEthprice()
    gas_cost = web3Feeds.rebalance(bestAllocation, estimate=True)
    return gas_cost * gas_price * eth_price


def checkYieldDelta(potentialYield):
    """Get the expected gain (in USD per unit time) of a given allocation over the current allocation

    Args:
        potentialYield (int): The yield of the proposed strategy

    Returns:
        int: The expected gain (in USD per unit time)
    """
    poolBalance = web3Feeds.getBallastPoolBalance()
    poolYield = web3Feeds.getBallastPoolYield()
    return poolBalance * (potentialYield - poolYield)


def getBestAllocation():
    """ Get the best allocation right now.

    Returns:
        dict: The allocation

    Note: any models (simple or complex) are abstracted behind this function. It just returns an allocation.

    """
    return models.getBestAllocation()


def execute(allocation):
    """Execute a given allocation

    Args:
        allocation (dict): The allocation to execute
    """
    print("New allocation recommended:")
    print(allocation)
    # rebalance(allocation)


@utils.every_block
def checkForRebalance(horizon):
    """Constantly loop to check if the best allocation is better than the current allocation for the specified horizon

    Args:
        horizon (int): The time horizon over which to check for profitable allocations
    """
    bestAllocation, bestYield = getBestAllocation()
    print(bestAllocation, bestYield)
    
    # Profit over given time horizon must be greater than cost to execute allocation
    if (horizon * checkYieldDelta(bestYield)) - checkCost(bestAllocation) > 0:
        web3Feeds.execute(bestAllocation)
        

#@utils.restart_on_failure
@utils.synced
def main():
    """Main function. Require synced web3 connection. Restart on unhandled errors

    """
    # The horizon over which a new allocation must be profitable to execute
    horizon = 10_000
    # TO DO: Thread this process to manage multiple pools in parallel
    checkForRebalance(horizon)


if __name__ == "__main__":
    main_strategy_address = ""
    main()