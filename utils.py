import requests
import web3
import time
import functools

# Constants
ether = int(10**18)
gwei = int(10**9)

w3 = web3.Web3(web3.Web3.IPCProvider(request_kwargs={'timeout': 60}))

# Import a contract using its address, retrieving the abi from etherscan
def import_contract(address):
    abi = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address='+address).json()['result']
    return w3.eth.contract(address=address, abi=abi)


# Some useful decorators ---
def synced(func):
    """
    Wrapper for functions requiring a connected and synced web3 instance
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        assert (w3.isConnected() and not w3.eth.syncing), "No web3 connection or node not synced."
        print(f'Node is connected and synced.')
        func_called = func(*args, **kwargs)
        return func_called
    return wrapper


# Calls a function on every new block
def every_block(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        old_block = 0
        while True:
            new_block = w3.eth.blockNumber
            if new_block != old_block:
                print(f'Block: {new_block}... ', end='')
                func(*args, **kwargs)
                old_block = new_block
    return wrapper


def restart_on_failure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f'Unhandled exception {e}')
                print('Restarting in 60s...')
                time.sleep(60)
                func(*args, **kwargs)

    return wrapper
