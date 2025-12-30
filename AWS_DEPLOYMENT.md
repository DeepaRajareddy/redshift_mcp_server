# AWS Deployment Guide: Redshift MCP Server

## Option 1: AWS App Runner (Simplest)

### Steps

1. **Create ECR Repository:**
```bash
aws ecr create-repository --repository-name redshift-mcp-server
```

2. **Build and Push Docker Image:**
```bash
docker build -t redshift-mcp-server .
# ... tag and push to ECR ...
```

3. **Deploy to App Runner:**
   - Use the ECR image.
   - Configure environment variables for Redshift connection.
   - Ensure the App Runner service has network access to your Redshift cluster (VPC connector if needed).

---

## Redshift Security

1. **Security Groups**: Ensure your Redshift cluster allows inbound traffic from the MCP server's IP or security group on port 5439.
2. **IAM Roles**: If using IAM authentication, ensure the server has the `redshift:GetClusterCredentials` permission.
