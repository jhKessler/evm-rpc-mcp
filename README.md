# evm-rpc-mcp

An MCP server that gives AI assistants read-only access to any EVM-compatible blockchain (Ethereum, Polygon, Arbitrum, Base, etc.) via JSON-RPC.

## Features

- `eth_block_number` — get the latest block number
- `eth_get_block` — get a block by number, tag, or hash
- `eth_get_transaction` — get a transaction by hash
- `eth_get_transaction_receipt` — get a transaction receipt
- `eth_get_logs` — query event logs with filters
- `eth_get_balance` — get an address balance
- `eth_get_code` — get contract bytecode
- `eth_get_storage_at` — read a contract storage slot
- `eth_call` — execute a read-only contract call
- `eth_gas_price` — get the current gas price
- `eth_chain_id` — get the chain ID
- `eth_get_transaction_count` — get an address nonce
- `net_version` — get the network ID

## Installation

```bash
pip install evm-rpc-mcp
```

Or run directly with `uvx`:

```bash
uvx evm-rpc-mcp --rpc-url https://eth.llamarpc.com
```

## Usage

Pass your RPC endpoint URL via the `--rpc-url` flag or the `EVM_RPC_URL` environment variable:

```bash
evm-rpc-mcp --rpc-url https://eth.llamarpc.com
```

```bash
EVM_RPC_URL=https://eth.llamarpc.com evm-rpc-mcp
```

### Claude Code

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "evm-rpc": {
      "type": "stdio",
      "command": "uvx",
      "args": ["evm-rpc-mcp", "--rpc-url", "https://eth.llamarpc.com"]
    }
  }
}
```

Or if you installed it with pip:

```json
{
  "mcpServers": {
    "evm-rpc": {
      "type": "stdio",
      "command": "evm-rpc-mcp",
      "args": ["--rpc-url", "https://eth.llamarpc.com"]
    }
  }
}
```

### Claude Desktop

Add this to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "evm-rpc": {
      "command": "uvx",
      "args": ["evm-rpc-mcp", "--rpc-url", "https://eth.llamarpc.com"]
    }
  }
}
```

Replace `https://eth.llamarpc.com` with your preferred RPC endpoint for any EVM chain.

## License

MIT
