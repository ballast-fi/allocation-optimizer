import web3Feeds

def getBestAllocation():
    """Get best proposed allocation from the model 

    Returns:
        dict: The proposed allocation
    """

    # Strategy is currently simple so returns a dict instructing strategy manager to allocation 100% to best platform
    # Also returns the yield to calculate if execution is profitable

    yields = web3Feeds.getPlatformYields()
    bestPlatform =  yields[max(yields, key=yields.get)]
    return {k: 1 if k == bestPlatform else 0 for k in yields.keys()}, yields[bestPlatform]
