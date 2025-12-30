"""
Redis MCP Server
A Model Context Protocol server that enables AI agents to interact with Redis databases.
"""

import os
import json
from typing import Any
from dotenv import load_dotenv
import redis
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("redis-mcp-server")

# Redis connection configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Create Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True
)


def get_connection_status() -> dict:
    """Get Redis connection status."""
    try:
        redis_client.ping()
        return {
            "status": "connected",
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": REDIS_DB
        }
    except redis.ConnectionError as e:
        return {
            "status": "disconnected",
            "error": str(e)
        }


# ============== MCP TOOLS ==============

@mcp.tool()
def redis_get(key: str) -> str:
    """
    Get the value of a key from Redis.
    
    Args:
        key: The Redis key to retrieve
    
    Returns:
        The value stored at the key, or a message if key doesn't exist
    """
    try:
        value = redis_client.get(key)
        if value is None:
            return f"Key '{key}' does not exist"
        return value
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def redis_set(key: str, value: str, expire_seconds: int = None) -> str:
    """
    Set a key-value pair in Redis.
    
    Args:
        key: The Redis key to set
        value: The value to store
        expire_seconds: Optional expiration time in seconds
    
    Returns:
        Confirmation message
    """
    try:
        if expire_seconds:
            redis_client.setex(key, expire_seconds, value)
        else:
            redis_client.set(key, value)
        return f"Successfully set key '{key}'"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def redis_delete(key: str) -> str:
    """
    Delete a key from Redis.
    
    Args:
        key: The Redis key to delete
    
    Returns:
        Confirmation message
    """
    try:
        deleted = redis_client.delete(key)
        if deleted:
            return f"Successfully deleted key '{key}'"
        return f"Key '{key}' does not exist"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def redis_hgetall(key: str) -> str:
    """
    Get all fields and values of a hash stored at key.
    
    Args:
        key: The Redis hash key
    
    Returns:
        JSON string of all hash fields and values
    """
    try:
        data = redis_client.hgetall(key)
        if not data:
            return f"Hash '{key}' does not exist or is empty"
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def redis_hset(key: str, field: str, value: str) -> str:
    """
    Set a field in a hash stored at key.
    
    Args:
        key: The Redis hash key
        field: The field name within the hash
        value: The value to set
    
    Returns:
        Confirmation message
    """
    try:
        redis_client.hset(key, field, value)
        return f"Successfully set field '{field}' in hash '{key}'"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def redis_keys(pattern: str = "*") -> str:
    """
    List all keys matching a pattern.
    
    Args:
        pattern: Pattern to match keys (default: "*" for all keys)
    
    Returns:
        JSON array of matching keys
    """
    try:
        keys = redis_client.keys(pattern)
        return json.dumps(keys, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def redis_list_tables() -> str:
    """
    List all available sample tables (users, products, orders).
    
    Returns:
        Information about available sample data tables
    """
    tables = {
        "users": {
            "description": "User accounts with name, email, role",
            "key_pattern": "user:*",
            "sample_key": "user:1"
        },
        "products": {
            "description": "Product catalog with name, price, category, stock",
            "key_pattern": "product:*",
            "sample_key": "product:1"
        },
        "orders": {
            "description": "Customer orders linking users and products",
            "key_pattern": "order:*",
            "sample_key": "order:1"
        }
    }
    return json.dumps(tables, indent=2)


@mcp.tool()
def redis_query_table(table_name: str) -> str:
    """
    Query all entries from a sample table.
    
    Args:
        table_name: Name of the table (users, products, or orders)
    
    Returns:
        JSON array of all entries in the table
    """
    table_patterns = {
        "users": "user:*",
        "products": "product:*",
        "orders": "order:*"
    }
    
    if table_name not in table_patterns:
        return f"Unknown table '{table_name}'. Available tables: users, products, orders"
    
    try:
        pattern = table_patterns[table_name]
        keys = redis_client.keys(pattern)
        
        if not keys:
            return f"No entries found in table '{table_name}'. Run seed_data.py to populate sample data."
        
        results = []
        for key in sorted(keys):
            data = redis_client.hgetall(key)
            data["_key"] = key
            results.append(data)
        
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def redis_connection_status() -> str:
    """
    Check the Redis connection status.
    
    Returns:
        Connection status information
    """
    return json.dumps(get_connection_status(), indent=2)


# ============== MCP RESOURCES ==============

@mcp.resource("redis://tables")
def get_tables_resource() -> str:
    """List of available sample data tables."""
    return redis_list_tables()


@mcp.resource("redis://status")
def get_status_resource() -> str:
    """Current Redis connection status."""
    return redis_connection_status()


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
