"""
Redshift MCP Server
A Model Context Protocol server that enables AI agents to interact with Amazon Redshift.
"""

import os
import json
import logging
from typing import Any, List, Dict, Optional
from dotenv import load_dotenv
import redshift_connector
import pandas as pd
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("redshift-mcp-server")

# Initialize FastMCP server
mcp = FastMCP("redshift-mcp-server")

# Redshift connection configuration
REDSHIFT_HOST = os.getenv("REDSHIFT_HOST", "localhost")
REDSHIFT_PORT = int(os.getenv("REDSHIFT_PORT", 5439))
REDSHIFT_DATABASE = os.getenv("REDSHIFT_DATABASE", "dev")
REDSHIFT_USER = os.getenv("REDSHIFT_USER", "awsuser")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD", "")

def get_connection():
    """Create a connection to Redshift or local Postgres."""
    try:
        # If host is localhost and port is 5432, assume local Postgres for testing
        if REDSHIFT_HOST == "localhost" and REDSHIFT_PORT == 5432:
            import psycopg2
            return psycopg2.connect(
                host=REDSHIFT_HOST,
                port=REDSHIFT_PORT,
                database=REDSHIFT_DATABASE,
                user=REDSHIFT_USER,
                password=REDSHIFT_PASSWORD
            )
        else:
            return redshift_connector.connect(
                host=REDSHIFT_HOST,
                port=REDSHIFT_PORT,
                database=REDSHIFT_DATABASE,
                user=REDSHIFT_USER,
                password=REDSHIFT_PASSWORD
            )
    except Exception as e:
        logger.error(f"Connection error: {e}")
        raise

# ============== MCP TOOLS ==============

@mcp.tool()
def redshift_query(sql: str) -> str:
    """
    Execute a SQL query on Redshift and return results as JSON.
    
    Args:
        sql: The SQL query to execute
    
    Returns:
        JSON string of the query results or error message
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(sql, conn)
            return df.to_json(orient="records", indent=2)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@mcp.tool()
def redshift_list_tables(schema: str = "public") -> str:
    """
    List all tables in a specific schema.
    
    Args:
        schema: The schema name (default: "public")
    
    Returns:
        JSON list of table names
    """
    sql = f"""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = '{schema}'
    AND table_type = 'BASE TABLE'
    """
    return redshift_query(sql)

@mcp.tool()
def redshift_describe_table(table_name: str, schema: str = "public") -> str:
    """
    Get the column definitions for a table.
    
    Args:
        table_name: Name of the table
        schema: Schema name (default: "public")
    
    Returns:
        JSON description of columns
    """
    sql = f"""
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_schema = '{schema}'
    AND table_name = '{table_name}'
    ORDER BY ordinal_position
    """
    return redshift_query(sql)

@mcp.tool()
def redshift_get_sample_data(table_name: str, limit: int = 5, schema: str = "public") -> str:
    """
    Get sample rows from a table.
    
    Args:
        table_name: Name of the table
        limit: Number of rows to return (default: 5)
        schema: Schema name (default: "public")
    
    Returns:
        JSON sample data
    """
    sql = f"SELECT * FROM {schema}.{table_name} LIMIT {limit}"
    return redshift_query(sql)

@mcp.tool()
def redshift_connection_status() -> str:
    """
    Check the Redshift connection status.
    
    Returns:
        Connection status information
    """
    try:
        with get_connection() as conn:
            return json.dumps({
                "status": "connected",
                "host": REDSHIFT_HOST,
                "port": REDSHIFT_PORT,
                "database": REDSHIFT_DATABASE
            }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "disconnected",
            "error": str(e)
        }, indent=2)

# ============== MCP RESOURCES ==============

@mcp.resource("redshift://tables")
def get_tables_resource() -> str:
    """List of available tables in the public schema."""
    return redshift_list_tables()

@mcp.resource("redshift://status")
def get_status_resource() -> str:
    """Current Redshift connection status."""
    return redshift_connection_status()

def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
