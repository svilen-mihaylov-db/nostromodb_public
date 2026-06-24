from typing import Any
from mcp.server.fastmcp import FastMCP

import json
import logging
import click
import subprocess

from instructions import get_instructions


logger = logging.getLogger("mcp_server_nostromodb")
logging.basicConfig(level=logging.INFO, format="[nostromodb] %(levelname)s - %(message)s")

def invoke_nostromodb():
    result = subprocess.run(["nostromodb", "--db_path", "--c"], capture_output=True, text=True)

    # Access the results
    print("STDOUT:", result.stdout)  # Outputs: Hello World
    print("Return Code:", result.returncode)  # Outputs: 0 (success)
    pass

@click.command()
@click.option(
    "--db_path",
    default="",
    help="(Default: '') Path to local NostromoDB database file. Empty if the database is temporary."
)
@click.option(
    "--read_only",
    is_flag=True,
    help="Enable write access to the database. Note: In-memory databases are always writable.",
)
def main(db_path: str, read_only: bool):
    instructions = get_instructions(read_only=read_only, db_path=db_path)

    # Initialize and run the server
    mcp = FastMCP(name="mcp-server-nostromodb", instructions=instructions)

    common_options = ["nostromodb", "--json_output"]
    if db_path:
        common_options.extend(["--db_path", db_path])
    if read_only:
        common_options.append("--read_only")
    print("Started sever with options: ", common_options)

    @mcp.tool()
    def execute_query_tool(sql: str) -> str:
        """
           Execute a SQL query on the NostromoDB database.

           Args:
               sql: SQL query to execute (NostromoDB SQL dialect)

           Returns:
               JSON string with query results

           """

        options = common_options.copy()
        options.extend(["--c", sql])
        print("Running sql query with", options)

        result = subprocess.run(options, capture_output=True, text=True, check=True)
        return result.stdout

    @mcp.tool()
    def list_tables_tool() -> str:
        """
            List all tables in the current database with their comments.
        """

        options = common_options.copy()
        options.extend(["--c", "pragma show_tables()"])
        print("Listing tables with", options)

        result = subprocess.run(options, capture_output=True, text=True, check=True)
        return result.stdout

    @mcp.tool()
    def list_columns_tool(table: str) -> str:
        """
        List all columns of a table or view with their types and comments.
        """

        options = common_options.copy()
        options.extend(["--c", f"select concat_arr(*, '.') from unpack(pragma_approx_columns('{table}'))"])
        print("Listing columns with", options)

        result = subprocess.run(options, capture_output=True, text=True, check=True)
        return result.stdout

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()