"""
Local Test Script for Redshift MCP
"""

import sys
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from redshift_mcp_server import (
    redshift_query,
    redshift_list_tables,
    redshift_describe_table,
    redshift_get_sample_data,
    redshift_connection_status
)

def print_section(title: str):
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)

def run_tests():
    print("\n[TEST] Redshift MCP Server - Local Test Suite\n")
    
    # Test 1: Connection Status
    print_section("1. Connection Status")
    status = redshift_connection_status()
    print(status)
    
    if "disconnected" in status:
        print("\n[ERROR] Cannot connect to Database. Make sure Postgres is running:")
        print("   docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=password postgres")
        return False
    
    # Test 2: List Tables
    print_section("2. List Tables")
    print(redshift_list_tables())
    
    # Test 3: Describe Table
    print_section("3. Describe Users Table")
    print(redshift_describe_table("users"))
    
    # Test 4: Sample Data
    print_section("4. Sample Data from Products")
    print(redshift_get_sample_data("products"))
    
    # Test 5: Custom Query
    print_section("5. Custom SQL Query")
    sql = "SELECT category, COUNT(*) as count FROM products GROUP BY category"
    print(redshift_query(sql))
    
    print("\n[SUCCESS] All tests completed!\n")
    return True

if __name__ == "__main__":
    run_tests()
