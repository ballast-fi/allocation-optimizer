import requests
import web3
import time
import functools
import secrets


# Constants
ether = int(10**18)
gwei = int(10**9)

alchemy_kovan_endpoint = f"https://eth-kovan.alchemyapi.io/v2/{secrets.alchemy_kovan_api_key}"

w3 = web3.Web3(web3.Web3.HTTPProvider(alchemy_kovan_endpoint, request_kwargs={'timeout': 60}))

def import_contract(address):
    """Import a contract using its address, retrieving the abi from etherscan

    Args:
        address (string): The address of the contract

    Returns:
        Contract: The contract object
    """
    abi = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address='+address).json()['result']
    return w3.eth.contract(address=address, abi=abi)



def synced(func):
    """Wrapper for functions requiring a connected and synced web3 instance
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        assert (w3.isConnected() and not w3.eth.syncing), "No web3 connection or node not synced."
        print(f'Node is connected and synced.')
        func_called = func(*args, **kwargs)
        return func_called
    return wrapper


def every_block(func):
    """Wrapper for invoking a function on every new block

    """
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
    """Wrapper for restarting a function if it encounters an unhandled exception

    """
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
