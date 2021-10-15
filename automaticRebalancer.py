import utils
import web3Feeds

# Get the gas cost (in USD equivalent) for executing a given allocation
def checkCost(bestAllocation):
    gas_price = web3Feeds.getGasPrice()
    eth_price = web3Feeds.getEthprice()
    gas_cost = web3Feeds.rebalance(bestAllocation, estimate=True)
    return gas_cost * gas_price * eth_price


# Get the expected gain (in USD per unit time) of a given allocation over the current allocation
def checkYieldDelta(potentialYield):
    poolBalance = web3Feeds.getCurrentPoolBalance()
    poolYield = web3Feeds.getCurrentPoolYield()
    return poolBalance * (potentialYield - poolYield)


# Get the best allocation right now.
# Note: any models (simple or complex) are abstracted behind this function. It just returns an allocation.
def getBestAllocation():
    yields = web3Feeds.getPlatformYields()
    # Strategy is currently simple so returns a dict instructing strategy manager to allocation 100% to best platform
    # Also returns the yield to calculate if execution is profitable
    bestPlatform =  yields[max(yields, key=yields.get)]
    return {k: 1 if k == bestPlatform else 0 for k in yields.keys()}, yields[bestPlatform]
    

# Execute the strategy
def execute(allocation):
    print("New allocation recommended:")
    print(allocation)
    # rebalance(allocation)


# Constantly loop to check if the best allocation is better than the current allocation for the specified horizon
@utils.every_block
def checkForRebalance(horizon):
    bestAllocation, bestYield = getBestAllocation()
    # Profit over given time horizon must be greater than cost to execute allocation
    if (horizon * checkYieldDelta(bestYield)) - checkCost(bestAllocation) > 0:
        web3Feeds.execute(bestAllocation)
        

# Main function. Require synced web3 connection. Restart on unhandled errors
@utils.restart_on_failure
@utils.synced
def main():
    # The horizon over which a new allocation must be profitable to execute
    horizon = 10_000
    # TO DO: Thread this process to manage multiple pools in parallel
    checkForRebalance(horizon)


if __name__ == "__main__":
    main_strategy_address = ""
    main()
