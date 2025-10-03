import click
from planner import Planner

@click.group()
def cli():
    """PlanTask AI CLI"""
    pass

# task commands (add, show, delete )
@cli.command()
@click.argument("title")
@click.option("--duration", default=60, help="Task duration in minutes")
@click.option("--priority", default="medium", type=click.Choice(["low", "medium", "high"]))
@click.option("--deadline", default=None, help="Deadline (YYYY-MM-DD)")
def add(title, duration, priority, deadline):
    """Add a new task"""
    planner = Planner()
    planner.add_task(title, duration, priority, deadline)
    planner.close()

@cli.command()
def show():
    """Show all tasks"""
    planner = Planner()
    planner.show_tasks()
    planner.close()

@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Delete a task"""
    planner = Planner()
    planner.delete_task(task_id)
    planner.close()

@cli.command()
def reschedule():
    """Reschedule overdue tasks"""
    planner = Planner()
    planner.reschedule_tasks()
    planner.close()

# reflection commands (reflect, reflection)
@cli.command()
@click.argument("reflection")
def reflect(reflection):
    """Add today’s reflection"""
    planner = Planner()
    planner.add_reflection(reflection)
    planner.close()

@cli.command()
@click.option("--date", default=None, help="Date (YYYY-MM-DD)")
def reflection(date):
    """Show reflection for a date (default: today)"""
    planner = Planner()
    planner.show_reflection(date)
    planner.close()

if __name__ == "__main__":
    cli()
