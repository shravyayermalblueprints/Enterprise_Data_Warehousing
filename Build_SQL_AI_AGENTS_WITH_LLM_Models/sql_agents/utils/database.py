from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from sql_agents.config import config

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(config.DB_CONNECTION_STRING)
        self.inspector = inspect(self.engine)

    def get_schema_summary(self):
        """Returns a summary of the database schema (tables and columns)."""
        schema_summary = ""
        for table_name in self.inspector.get_table_names():
            schema_summary += f"Table: {table_name}\n"
            columns = self.inspector.get_columns(table_name)
            for column in columns:
                schema_summary += f"  - {column['name']} ({column['type']})\n"
            schema_summary += "\n"
        return schema_summary

    def execute_query(self, query):
        """Executes a SQL query and returns the results."""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                if result.returns_rows:
                    return result.fetchall(), result.keys()
                return "Query executed successfully.", []
        except SQLAlchemyError as e:
            return f"Error executing query: {str(e)}", []
