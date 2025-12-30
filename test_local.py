"""
Local Test Script
Tests the Redis MCP server functionality without needing an MCP client.
"""

import sys
import json

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from redis_mcp_server import (
    redis_get,
    redis_set,
    redis_delete,
    redis_hgetall,
    redis_hset,
    redis_keys,
    redis_list_tables,
    redis_query_table,
    redis_connection_status,
    get_connection_status
)


def print_section(title: str):
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)


def run_tests():
    print("\n[TEST] Redis MCP Server - Local Test Suite\n")
    
    # Test 1: Connection Status
    print_section("1. Connection Status")
    status = redis_connection_status()
    print(status)
    
    if "disconnected" in status:
        print("\n[ERROR] Cannot connect to Redis. Make sure Redis is running:")
        print("   docker run -d -p 6379:6379 redis:latest")
        return False
    
    # Test 2: Basic SET/GET
    print_section("2. Basic SET/GET Operations")
    print(f"SET: {redis_set('test:hello', 'world')}")
    print(f"GET: {redis_get('test:hello')}")
    print(f"DELETE: {redis_delete('test:hello')}")
    print(f"GET (after delete): {redis_get('test:hello')}")
    
    # Test 3: Hash Operations
    print_section("3. Hash Operations")
    print(f"HSET: {redis_hset('test:user', 'name', 'Test User')}")
    print(f"HSET: {redis_hset('test:user', 'email', 'test@example.com')}")
    print(f"HGETALL: {redis_hgetall('test:user')}")
    redis_delete('test:user')
    
    # Test 4: Keys Pattern
    print_section("4. List Keys")
    print(f"All keys matching 'user:*':")
    print(redis_keys('user:*'))
    
    # Test 5: List Tables
    print_section("5. Available Tables")
    print(redis_list_tables())
    
    # Test 6: Query Tables
    print_section("6. Query Users Table")
    users = redis_query_table('users')
    print(users)
    
    print_section("7. Query Products Table")
    products = redis_query_table('products')
    print(products)
    
    print_section("8. Query Orders Table")
    orders = redis_query_table('orders')
    print(orders)
    
    print("\n[SUCCESS] All tests completed!\n")
    return True


if __name__ == "__main__":
    run_tests()
