from web3 import Web3, HTTPProvider
import requests
import os

def deploy_to_evm(url, address, private_key, contract_abi, contract_bytecode):
    w3 = Web3(HTTPProvider(url))
    assert w3.is_connected()
    contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

    my_address = w3.to_checksum_address(address)

    gas_estimate = contract.constructor().estimate_gas()

    transaction = {
        'gas': gas_estimate,
        'nonce': w3.eth.get_transaction_count(my_address),
    }

    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(contract.constructor().build_transaction(transaction), private_key)

    # Send transaction
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for transaction to be mined
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(txn_receipt)
    return txn_receipt['contractAddress']

if __name__ == '__main__':
    SOURCE_ABI_API_KEY = os.environ.get("SOURCE_ABI_API_KEY")

    SOURCE_URL = os.environ.get("SOURCE_URL")
    SOURCE_CONTRACT_ADDR = os.environ.get("SOURCE_CONTRACT_ADDR")
    # Assume we use the $BLOCKCHAIN SCAN websites
    SOURCE_ABI_API_KEY = os.environ.get("SOURCE_ABI_API_KEY")
    SOURCE_ABI_URL = os.environ.get("SOURCE_ABI_URL") + f"?module=contract&action=getabi&address={SOURCE_CONTRACT_ADDR}&apikey={SOURCE_ABI_API_KEY}"

    w3 = Web3(HTTPProvider(SOURCE_URL))
    try:
        BYTECODE = w3.eth.get_code(SOURCE_CONTRACT_ADDR)
        ABI = requests.get(SOURCE_ABI_URL,timeout=10).json()['result']
    except Exception:
        print("Error getting bytecode or ABI")

    # # Deploy to a test net
    URL = os.environ.get("ETH_GOERLI_URL")
    ADDRESS = os.environ.get("ADDRESS")
    PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

    deployed_contract_addr = deploy_to_evm(URL, ADDRESS, PRIVATE_KEY, ABI, BYTECODE)
    print("Sent to Ethereum Testnet Goerli: ", deployed_contract_addr)
    print("Check it out here - ", "https://goerli.etherscan.io/address/" + deployed_contract_addr )

    # Deploy to gnosis test net

    URL = os.environ.get("GNOSIS_TESTNET_URL")
    deployed_contract_addr = deploy_to_evm(URL, ADDRESS, PRIVATE_KEY, ABI, BYTECODE)
    print("Sent to Gnosis Testnet Chiado: ", deployed_contract_addr)
    print("Check it out here - ", "https://gnosis-chiado.blockscout.com/address/" + deployed_contract_addr )
