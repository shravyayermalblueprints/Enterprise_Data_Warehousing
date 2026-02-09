import argparse
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Advanced SQL Agents CLI")
    parser.add_argument("agent", choices=["text_to_sql", "optimizer", "explainer", "documenter", "analyst"], help="The agent to run")
    parser.add_argument("--query", help="The SQL query or natural language question")
    parser.add_argument("--schema", help="Path to schema file (for documenter/text_to_sql)")
    
    args = parser.parse_args()
    
    console.print(Panel(f"Running Agent: [bold]{args.agent}[/bold]", title="SQL Agents"))

    if args.agent == "text_to_sql":
        if not args.query:
            console.print("[red]Error: --query argument is required for text_to_sql agent.[/red]")
            return
        
        from sql_agents.agents.text_to_sql import TextToSQLAgent
        agent = TextToSQLAgent()
        results, columns, sql = agent.run(args.query)
        
        console.print(Panel(f"[bold]Generated SQL:[/bold]\n{sql}", title="Result"))
        if isinstance(results, str) and results.startswith("Error"):
             console.print(f"[red]{results}[/red]")
        else:
             console.print(f"[green]Query executed successfully. Rows returned: {len(results)}[/green]")
             for row in results:
                 console.print(row)

    elif args.agent == "optimizer":
        if not args.query:
            console.print("[red]Error: --query argument is required for optimizer agent.[/red]")
            return
            
        from sql_agents.agents.optimizer import SQLOptimizerAgent
        agent = SQLOptimizerAgent()
        report = agent.run(args.query)
        
        console.print(Panel(report, title="Optimization Report"))

    elif args.agent == "explainer":
        if not args.query:
            console.print("[red]Error: --query argument is required for explainer agent.[/red]")
            return
            
        from sql_agents.agents.explainer import SQLExplainerAgent
        agent = SQLExplainerAgent()
        explanation = agent.run(args.query)
        
        console.print(Panel(explanation, title="Query Explanation"))

    elif args.documenter == "documenter" or args.agent == "documenter":
        from sql_agents.agents.documenter import DatabaseDocumenterAgent
        agent = DatabaseDocumenterAgent()
        doc = agent.run()
        
        console.print(Panel(doc, title="Database Documentation"))

    elif args.agent == "analyst":
        if not args.query:
            console.print("[red]Error: --query argument is required for analyst agent.[/red]")
            return
            
        from sql_agents.agents.analyst import DataAnalystAgent
        agent = DataAnalystAgent()
        analysis = agent.run(args.query)
        
        console.print(Panel(analysis, title="Data Analysis"))

if __name__ == "__main__":
    main()
