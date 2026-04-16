# app/core/scheduler.py

from app.agent.planner import generate_tasks_from_goal
from app.task.service import create_tasks_from_plan

def daily_goal_planning():

    goal = "Build a production-ready AI agent system"

    plan = generate_tasks_from_goal(goal)

    create_tasks_from_plan(plan)

    print("✅ Daily tasks generated")