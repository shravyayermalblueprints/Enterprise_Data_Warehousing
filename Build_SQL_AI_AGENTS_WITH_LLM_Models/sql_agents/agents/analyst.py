from openai import OpenAI
from sql_agents.config import config
from sql_agents.utils.database import DatabaseManager
import json

class DataAnalystAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.db_manager = DatabaseManager()

    def analyze_data(self, query, data, columns):
        """Analyzes the data returned by a query."""
        
        # Convert data to a string format (limit complexity for LLM)
        # In a real app, we might use pandas and only send summary stats if data is large
        data_str = str(data[:20]) # Limit to first 20 rows for analysis to avoid token limits
        if len(data) > 20:
            data_str += f"\n... (and {len(data) - 20} more rows)"

        prompt = f"""
You are an expert data analyst.
Given the following SQL query:
```sql
{query}
```

And the following data results (columns: {columns}):
{data_str}

Please analyze this data.
Provide:
1.  **Summary of Findings**: What does the data show? (Trends, outliers, patterns)
2.  **Key Insights**: Business or technical insights derived from the data.
3.  **Visualization Suggestions**: What type of charts/graphs would best represent this data?

Format the output in Markdown.
"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful data analysis expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content.strip()

    def run(self, query):
        print(f"Executing and Analyzing: {query}")
        data, columns = self.db_manager.execute_query(query)
        
        if isinstance(data, str) and data.startswith("Error"):
            return f"Could not analyze data due to execution error: {data}"
            
        analysis = self.analyze_data(query, data, columns)
        return analysis
