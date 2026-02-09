from openai import OpenAI
from sql_agents.config import config
from sql_agents.utils.database import DatabaseManager

class SQLOptimizerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.db_manager = DatabaseManager()

    def optimize_query(self, query):
        """Analyzes a SQL query and suggests optimizations."""
        schema = self.db_manager.get_schema_summary()
        
        # Get execution plan if possible (SQLite specific)
        try:
            explain_results, _ = self.db_manager.execute_query(f"EXPLAIN QUERY PLAN {query}")
            execution_plan = "\n".join([str(row) for row in explain_results])
        except Exception as e:
            execution_plan = f"Could not retrieve execution plan: {str(e)}"

        prompt = f"""
You are an expert SQL database administrator and query optimizer.
Given the following database schema:
{schema}

And the following SQL query:
```sql
{query}
```

And its execution plan (if available):
{execution_plan}

Please analyze the query for performance issues and suggest optimizations.
Provide the optimized SQL query (if applicable) and a detailed explanation of why it is better.
If the query is already optimal, explain why.

Format your response as:
**Analysis:** [Your analysis]
**Optimized Query:**
```sql
[Optimized SQL]
```
**Explanation:** [Reasoning]
"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful SQL optimization expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content.strip()

    def run(self, query):
        print(f"Optimizing SQL: {query}")
        optimization_report = self.optimize_query(query)
        return optimization_report
