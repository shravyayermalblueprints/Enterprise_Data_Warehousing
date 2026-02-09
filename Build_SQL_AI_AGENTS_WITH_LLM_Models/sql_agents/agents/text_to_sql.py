from openai import OpenAI
from sql_agents.config import config
from sql_agents.utils.database import DatabaseManager

class TextToSQLAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.db_manager = DatabaseManager()

    def generate_sql(self, question):
        """Generates a SQL query from a natural language question."""
        schema = self.db_manager.get_schema_summary()
        
        prompt = f"""
You are an expert SQL assistant. Your goal is to convert natural language questions into executable SQL queries.
Given the following database schema:

{schema}

Write a SQL query to answer the following question:
"{question}"

Return ONLY the SQL query, without any markdown formatting or explanations.
"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful SQL assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content.strip().replace("```sql", "").replace("```", "")

    def run(self, question):
        print(f"Generating SQL for: {question}")
        sql_query = self.generate_sql(question)
        print(f"Generated SQL: {sql_query}")
        
        input("Press Enter to execute this query...")
        
        results, columns = self.db_manager.execute_query(sql_query)
        return results, columns, sql_query
