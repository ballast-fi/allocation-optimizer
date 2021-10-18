import web3
import utils
import secrets

alchemy_kovan_endpoint = f"https://eth-kovan.alchemyapi.io/v2/{secrets.alchemy_kovan_api_key}"

w3 = web3.Web3(web3.Web3.HTTPProvider(alchemy_kovan_endpoint, request_kwargs={'timeout': 60}))

main_strategy_address = "0xe80EfEe1Ab443D9D63ee15e43ef928ef10a2C8da"

# requires strategy manager to be verified on etherscan. Otherwise just do strategyManager = w3.eth.contract(address, abi)
# strategyManager = utils.import_contract(main_strategy_address)
with open("abi/pool.json") as f:
    pool_abi = f.read()

strategyManager = w3.eth.contract(address=main_strategy_address, abi=pool_abi)

 
def getBallastPoolBalance():
    """Gets the current Ballast pool balance

    Returns:
    int: The total pool balance
    """
    return strategyManager.functions.underlyingBalanceInclStrategy().call()


def getBallastPoolYield():
    """Gets the current Ballast pool yield 

    Returns:
        int: The aggregate underlying yield of the current strategy
    """
    return strategyManager.functions.getAPR().call()


def rebalance(allocation, estimate=False):
    """Call the strategyManager contract to rebalance. Optionally just estimate gas, without execution.

    Args:
        allocation (dict): The allocation to implement
        estimate (bool, optional): Whether to just estimate gas cost. Defaults to False.

    Returns:
        int: Gas cost, or None.
    """
    # TO DO : Convert allocation into data format that strategyManager expects
    data = '0x'
    if estimate:
        return strategyManager.functions.rebalance(data).estimateGas()
    else:
        strategyManager.functions.rebalance(data).transact()



def getPlatformYields():
    """Gets yields from platforms we support. Currently Aave and Compound

    Returns:
        dict: The yieds of each of the platorms

    DEV: Does Ballast contract have endpoint for this or do we need to import Aave and Compound contracts themselves? 
    """
    # TO DO
    return {"compound": 1, "aave": 2}

# TO DO : This probably needs to be EIP-1559-ified
def getGasPrice():
    """Get the current gas price

    Returns:
        int: The current gas price
    """
    return w3.eth.gasPrice


def getEthprice():
    """Get the current ether price
    
    """
    # TO DO
    # Insert price oracle here.
    # Could be on chain (e.g. uniswap ETH/USDC), or centralized exchange (Kraken API, etc.)
    # Probably a hybrid price with safeguards is best (e.g. 5 feeds, discard high and low, and take mean value)
    pass