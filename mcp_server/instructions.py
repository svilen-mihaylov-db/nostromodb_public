"""
Server instructions for NostromoDB.

These instructions are sent to the client during initialization
to provide context about how to use the server's capabilities.
"""

INSTRUCTIONS_BASE = """Execute SQL queries against the NostromoDB databases using the NostromoDB SQL syntax.

## Available Tools

- `execute_query`: Execute SQL queries (NostromoDB SQL dialect)
- `list_tables`: List tables and views in a database
- `list_columns`: List columns of a table or view

## NostromoDB SQL Quick Reference

**Name Qualification**
- Format: 'foo.bar' or fully qualified: 'table::foo.bar'
- Use fully qualified names when joining tables across different databases

**Identifiers and Literals:**
- Use single quotes (`'`) for string literals
- Identifiers can be used to form paths: e.g. 'foo.bar'. If spaces are required inside a path, wrap with quotes and begin with a dot: '.'field with space''

**Flexible Query Structure:**
- `SELECT` without `FROM` for expressions: `SELECT 1 + 1 AS result;`
- `CREATE TABLE <foo>' may be used, but it is not required to create a table. 'INSERT INTO <foo> VALUES ..." may be used to implicitly create table <foo> if it does not already exist (otherwise it will just append the values).  

### Schema Exploration

```sql
-- List tables in a database
PRAGMA show_tables();
OR
SELECT name FROM pragma_show_tables() WHERE name = 'your_table'; 

-- Get column/json path info, with the columns display in array format: e.g. "a.b.c" returned as ["a", "b", "c"]
PRAGMA table_flush('your_table');
<followed by>
PRAGMA approx_columns('your_table');

-- To return the json paths in dotted format (e.g. "a.b.c") apply the following: 
select concat_arr(*, '.') from unpack(pragma_approx_columns('your_table'))

```

### Query Best Practices

- Filter early to reduce data volume before blocking operations
- Avoid unnecessary `ORDER BY` on intermediate results

### Persisting In-Memory Data to File

To save an in-memory database to a persistent file:

```sql
-- List all tables:
PRAGMA show_tables();
-- Export a table to a json file
EXPORT <table> to '/path/to/exported.json';
--Start in persistent mode (with non-empty database path)
-- Import the data from the exported file:
IMPORT FROM '/tmp/export.json' INTO <table>; 
```
"""

def get_instructions(read_only: bool = False,  db_path: str = "") -> str:
    """
    Get server instructions with connection context.

    Args:
        read_only: Whether the server is in read-only mode
        db_path: The database path being used

    Returns:
        Instructions string with context header
    """
    context_lines = []

    # Database info
    if db_path == "":
        context_lines.append("- **Database**: In-memory (data will not persist after session ends)")
    else:
        context_lines.append(f"- **Database**: Local NostromoDB file (`{db_path}`)")

    # Access mode
    if read_only:
        context_lines.append(
            "- **Access mode**: Read-only - CREATE, INSERT, UPDATE, DELETE, and DROP operations are disabled for non-temporary tables. All SQL operations are available for temporary tables."
        )
    else:
        context_lines.append("- **Access mode**: Read-write - all SQL operations are allowed")

    # Available tools
    tools = ["execute_query", "list_tables", "list_columns"]
    context_lines.append(f"- **Available tools**: {', '.join(tools)}")

    # Implications for the agent
    context_lines.append("")
    context_lines.append("### Important Implications")

    if db_path == "":
        context_lines.append("- Data created in this session will be lost when the session ends")
        context_lines.append(
            "- To persist data, use EXPORT (see 'Persisting In-Memory Data to File' below)"
        )

    if read_only:
        context_lines.append(
            "- You can only query existing data in non-temporary tables; any attempt to modify data in non-temporary tables will fail"
        )
        context_lines.append("- Use this mode for safe data exploration and analysis")

    context = "## Server Configuration\n\n" + "\n".join(context_lines) + "\n\n"
    return context + INSTRUCTIONS_BASE
