from openai import OpenAI
from sql_agents.config import config
from sql_agents.utils.database import DatabaseManager

class DatabaseDocumenterAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.db_manager = DatabaseManager()

    def generate_documentation(self):
        """Generates documentation for the database schema."""
        schema = self.db_manager.get_schema_summary()
        
        prompt = f"""
You are an expert technical writer and database architect.
Given the following database schema:
{schema}

Please generate comprehensive technical documentation for this database.
Include:
1.  **Overview**: A high-level description of the database's purpose (infer from table names).
2.  **Table Details**: For each table, describe its purpose, columns, and data types.
3.  **Relationships**: Infer and describe potential relationships between tables.

Format the output in Markdown.
"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful documentation expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content.strip()

    def run(self):
        print("Generating database documentation...")
        documentation = self.generate_documentation()
        return documentation
