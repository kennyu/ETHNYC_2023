## Move contracts from EVM compatible chains
Service that helps migrate projects from an EVM based chain to other EVM compatible chain

## How to run
# Set the variables in the `env.sh` file
```
export SOURCE_URL=""            # RPC url of the chain
export SOURCE_ABI_API_KEY=""    # API key from a blockchain-scan website
export SOURCE_ABI_URL=""        # URL from a blockchain-scan website
export SOURCE_CONTRACT_ADDR=""  # Contract Address
export PRIVATE_KEY=""           # Private key you are using to deploy onto testnets
export ADDRESS=""               # Wallet address you are using to deploy onto
export ETH_GOERLI_URL=""        # RPC Url of the ethereum testnet
export GNOSIS_TESTNET_URL=""    # RPC Url of the gnosis testnet
```
# Run the commands
```
mv env.sh set_env.sh && source set_env.sh
pip install
python app.py
```
