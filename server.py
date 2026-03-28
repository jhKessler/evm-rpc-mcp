#!/usr/bin/env python3
"""MCP server providing read-only access to an EVM node via JSON-RPC."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from mcp.server.fastmcp import FastMCP

RPC_URL: str = ""

mcp = FastMCP("evm-rpc")


def rpc_call(method: str, params: list | None = None) -> str:
    """Make a JSON-RPC call to the EVM node."""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params or [],
        "id": 1,
    }).encode()
    req = urllib.request.Request(
        RPC_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
    except urllib.error.URLError as e:
        return json.dumps({"error": str(e)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

    if "error" in result:
        return json.dumps(result["error"], indent=2)
    return json.dumps(result.get("result"), indent=2)


@mcp.tool()
def eth_block_number() -> str:
    """Get the latest block number."""
    return rpc_call("eth_blockNumber")


@mcp.tool()
def eth_get_block(block: str = "latest", full_transactions: bool = False) -> str:
    """Get a block by number (hex like '0x1' or 'latest'/'earliest'/'pending') or by hash (0x-prefixed 32-byte hash).

    Args:
        block: Block number (hex), tag (latest/earliest/pending), or block hash.
        full_transactions: If true, return full transaction objects instead of just hashes.
    """
    if block.startswith("0x") and len(block) == 66:
        return rpc_call("eth_getBlockByHash", [block, full_transactions])
    return rpc_call("eth_getBlockByNumber", [block, full_transactions])


@mcp.tool()
def eth_get_transaction(tx_hash: str) -> str:
    """Get a transaction by its hash.

    Args:
        tx_hash: The 0x-prefixed transaction hash.
    """
    return rpc_call("eth_getTransactionByHash", [tx_hash])


@mcp.tool()
def eth_get_transaction_receipt(tx_hash: str) -> str:
    """Get the receipt of a transaction by its hash.

    Args:
        tx_hash: The 0x-prefixed transaction hash.
    """
    return rpc_call("eth_getTransactionReceipt", [tx_hash])


@mcp.tool()
def eth_get_logs(
    from_block: str = "latest",
    to_block: str = "latest",
    address: str | None = None,
    topics: str | None = None,
) -> str:
    """Get logs matching a filter.

    Args:
        from_block: Start block (hex number or tag like 'latest').
        to_block: End block (hex number or tag like 'latest').
        address: Contract address to filter by (optional). Can be a single address or comma-separated list.
        topics: JSON array of topic filters, e.g. '["0xddf2..."]'. Each element can be a hex string or null. (optional)
    """
    filter_obj: dict = {
        "fromBlock": from_block,
        "toBlock": to_block,
    }
    if address:
        if "," in address:
            filter_obj["address"] = [a.strip() for a in address.split(",")]
        else:
            filter_obj["address"] = address
    if topics:
        filter_obj["topics"] = json.loads(topics)
    return rpc_call("eth_getLogs", [filter_obj])


@mcp.tool()
def eth_get_balance(address: str, block: str = "latest") -> str:
    """Get the balance of an address in wei (hex).

    Args:
        address: The 0x-prefixed address.
        block: Block number (hex) or tag (latest/earliest/pending).
    """
    return rpc_call("eth_getBalance", [address, block])


@mcp.tool()
def eth_get_code(address: str, block: str = "latest") -> str:
    """Get the bytecode at a contract address.

    Args:
        address: The 0x-prefixed contract address.
        block: Block number (hex) or tag (latest/earliest/pending).
    """
    return rpc_call("eth_getCode", [address, block])


@mcp.tool()
def eth_get_storage_at(address: str, position: str, block: str = "latest") -> str:
    """Get the value of a storage slot at a contract address.

    Args:
        address: The 0x-prefixed contract address.
        position: The storage slot position (hex, e.g. '0x0').
        block: Block number (hex) or tag (latest/earliest/pending).
    """
    return rpc_call("eth_getStorageAt", [address, position, block])


@mcp.tool()
def eth_call(to: str, data: str, from_addr: str | None = None, block: str = "latest") -> str:
    """Execute a read-only call against a contract (eth_call). Does not create a transaction.

    Args:
        to: The 0x-prefixed contract address to call.
        data: The 0x-prefixed calldata (encoded function selector + arguments).
        from_addr: Optional sender address for the call context.
        block: Block number (hex) or tag (latest/earliest/pending).
    """
    call_obj: dict = {"to": to, "data": data}
    if from_addr:
        call_obj["from"] = from_addr
    return rpc_call("eth_call", [call_obj, block])


@mcp.tool()
def eth_gas_price() -> str:
    """Get the current gas price in wei (hex)."""
    return rpc_call("eth_gasPrice")


@mcp.tool()
def eth_chain_id() -> str:
    """Get the chain ID."""
    return rpc_call("eth_chainId")


@mcp.tool()
def eth_get_transaction_count(address: str, block: str = "latest") -> str:
    """Get the transaction count (nonce) of an address.

    Args:
        address: The 0x-prefixed address.
        block: Block number (hex) or tag (latest/earliest/pending).
    """
    return rpc_call("eth_getTransactionCount", [address, block])


@mcp.tool()
def net_version() -> str:
    """Get the network version / network ID."""
    return rpc_call("net_version")


def main():
    parser = argparse.ArgumentParser(description="MCP server for EVM JSON-RPC")
    parser.add_argument(
        "--rpc-url",
        default=os.environ.get("EVM_RPC_URL"),
        help="EVM JSON-RPC endpoint URL (or set EVM_RPC_URL env var)",
    )
    args = parser.parse_args()

    if not args.rpc_url:
        print("Error: RPC URL required. Use --rpc-url or set EVM_RPC_URL.", file=sys.stderr)
        sys.exit(1)

    global RPC_URL
    RPC_URL = args.rpc_url
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
