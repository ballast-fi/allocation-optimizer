import web3
import utils

w3 = web3.Web3(web3.Web3.IPCProvider(request_kwargs={'timeout': 60}))
main_strategy_address = ""

# requires strategy manager to be verified on etherscan. Otherwise just do strategyManager = w3.eth.contract(address, abi)
strategyManager = utils.import_contract(main_strategy_address)


# Gets the current Ballast pool balance 
def getBallastPoolBalance():
    return strategyManager.functions.investedUnderlyingBalance()


# Gets the current Ballast pool yield 
def getBallastPoolYield():
    return strategyManager.functions.getAPR()


# Call the strategyManager contract to rebalance. Optionally just estimate gas, without execution.
def rebalance(allocation, estimate=False):
    # TO DO : Convert allocation into data format that strategyManager expects
    data = '0x'
    if estimate:
        return strategyManager.functions.rebalance(data).estimateGas()
    else:
        strategyManager.functions.rebalance(data).transact()


# Gets yields from platforms we support. Currently Aave and Compound
# DEV: Does Ballast contract have endpoint for this or do we need to import Aave and Compound contracts themselves? 
def getPlatformYields():
    # TO DO
    return {"compound": 0, "aave": 0}

# Get the current gas price
# TO DO : This probably needs to be EIP-1559-ified
def getGasPrice():
    return w3.eth.gasPrice

# Get the current ether price
def getEthprice():
    # TO DO
    # Insert price oracle here.
    # Could be on chain (e.g. uniswap ETH/USDC), or centralized exchange (Kraken API, etc.)
    # Probably a hybrid price with safeguards is best (e.g. 5 feeds, discard high and low, and take mean value)
    pass