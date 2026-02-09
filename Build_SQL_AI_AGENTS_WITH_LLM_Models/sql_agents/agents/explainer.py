from openai import OpenAI
from sql_agents.config import config
from sql_agents.utils.database import DatabaseManager

class SQLExplainerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.db_manager = DatabaseManager()

    def explain_query(self, query):
        """Generates a plain English explanation for a SQL query."""
        schema = self.db_manager.get_schema_summary()
        
        prompt = f"""
You are an expert SQL educator and technical writer.
Given the following database schema:
{schema}

And the following SQL query:
```sql
{query}
```

Please explain what this query does in plain English. 
Break down the explanation into:
1.  **Objective**: A one-sentence summary of what the query retrieves.
2.  **Logic**: A step-by-step breakdown of the operations (joins, filters, aggregations).
3.  **Key Takeaways**: Any important notes about the data being queried.

Keep the explanation clear and concise, suitable for a non-technical stakeholder.
"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful SQL explanation expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content.strip()

    def run(self, query):
        print(f"Explaining SQL: {query}")
        explanation = self.explain_query(query)
        return explanation
