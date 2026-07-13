Example configuration for Claude Desktop:

In ~/.config/Claude/claude_desktop_config.json, add the following field to the json configuration:

```
 "mcpServers": {
    "nostromodb": {
      "command": "uv",
      "args": [
        "--directory",
        "{source location}/nostromodb_public/mcp_server",
        "run",
        "nostromodb.py",
        "--db_path",
        "{data location}/{catalog name}.json",
        "--read_only",
        "--use_docker"
      ]
    }
  },
```

If --use-docker is specified, the MCP server will rely on the docker image (see nostromodb.io), otherwise if set to false
it will rely on a local installation (via the .deb package).

