# Multi-Platform Setup Guide: Redshift MCP Server

This guide provides instructions for setting up the Redshift MCP server on Windows, macOS, and Linux.

---

## 📋 Prerequisites (All Platforms)

- **Python 3.10+**: Required to run the MCP server.
- **Docker Desktop**: Recommended for running a local Postgres instance for testing.

---

## 🪟 Windows Setup

### 1. Install Dependencies
```powershell
py -m pip install mcp redshift-connector pandas python-dotenv psycopg2-binary sqlalchemy
```

### 2. Start Local Postgres (for testing)
```powershell
docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=password postgres
```

### 3. Configure .env
Create a `.env` file:
```env
REDSHIFT_HOST=localhost
REDSHIFT_PORT=5432
REDSHIFT_DATABASE=postgres
REDSHIFT_USER=postgres
REDSHIFT_PASSWORD=password
```

### 4. Seed Data & Test
```powershell
py seed_redshift.py
py test_redshift_local.py
```

---

## 🔧 MCP Client Configuration

### 1. Antigravity
Add this to your Antigravity MCP settings:
```json
{
  "mcpServers": {
    "redshift-org": {
      "command": "py",
      "args": ["redshift_mcp_server.py"],
      "cwd": "C:/Users/santo/OneDrive/Desktop/workspace/redis connection",
      "env": {
        "REDSHIFT_HOST": "localhost",
        "REDSHIFT_PORT": "5432",
        "REDSHIFT_DATABASE": "postgres",
        "REDSHIFT_USER": "postgres",
        "REDSHIFT_PASSWORD": "password"
      }
    }
  }
}
```

---

## ☁️ Connecting to Amazon Redshift

To connect to your actual Redshift cluster, update your `.env` or MCP environment variables:
```env
REDSHIFT_HOST=your-cluster.abc123xyz.us-east-1.redshift.amazonaws.com
REDSHIFT_PORT=5439
REDSHIFT_DATABASE=dev
REDSHIFT_USER=awsuser
REDSHIFT_PASSWORD=your-password
```
