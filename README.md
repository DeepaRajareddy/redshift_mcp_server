# Redshift MCP Server

A Model Context Protocol (MCP) server that enables AI agents to interact with Amazon Redshift using natural language.

## Features

- **SQL Tools**: Execute queries, list tables, describe schemas, get sample data.
- **Resources**: Connection status, table list.
- **Sample Data**: Pre-configured users, products, and orders tables.
- **Architecture**: See [DESIGN.md](DESIGN.md) for system diagrams.

---

## 🚀 Quick Start

For detailed instructions on **Windows, macOS, and Linux**, please refer to the [SETUP.md](SETUP.md) guide.

### Basic Steps (Local Testing):

1. **Start Postgres**: `docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=password postgres`
2. **Install Deps**: `pip install mcp redshift-connector pandas python-dotenv psycopg2-binary sqlalchemy`
3. **Seed Data**: `python seed_redshift.py`
4. **Test**: `python test_redshift_local.py`

---

## 🔧 MCP Client Configuration

Add this to your MCP client configuration (e.g., Antigravity, Claude Code, or VS Code).

```json
"redshift-mcp": {
  "command": "py",
  "args": ["redshift_mcp_server.py"],
  "cwd": "c:/Users/santo/OneDrive/Desktop/workspace/redis connection",
  "env": {
    "REDSHIFT_HOST": "localhost",
    "REDSHIFT_PORT": "5432",
    "REDSHIFT_DATABASE": "postgres",
    "REDSHIFT_USER": "postgres",
    "REDSHIFT_PASSWORD": "password"
  }
}
```

---

## ☁️ AWS Deployment

See [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for deployment options.
