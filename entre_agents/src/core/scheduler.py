"""
Simple scheduler for autonomous agent operations.

Enables agents to run tasks on schedules (e.g., morning briefing at 8am).
Lightweight implementation - just what we need now.
"""

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, time
import threading
import time as time_module


@dataclass
class ScheduledTask:
    """
    Represents a scheduled task.
    """
    id: str
    agent_name: str
    task_name: str
    schedule_time: time  # Time of day to run (e.g., 08:00)
    task_function: Callable
    enabled: bool = True
    last_run: Optional[datetime] = None


class SimpleScheduler:
    """
    Simple daily scheduler for agent tasks.

    Runs tasks at specified times each day.
    """

    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.check_interval = 60  # Check every 60 seconds

    def schedule_daily(
        self,
        agent_name: str,
        task_name: str,
        schedule_time: time,
        task_function: Callable
    ) -> str:
        """
        Schedule a task to run daily at a specific time.

        Args:
            agent_name: Name of the agent
            task_name: Name of the task
            schedule_time: Time of day to run (datetime.time object)
            task_function: Function to execute

        Returns:
            Task ID
        """
        task_id = f"{agent_name}_{task_name}"

        task = ScheduledTask(
            id=task_id,
            agent_name=agent_name,
            task_name=task_name,
            schedule_time=schedule_time,
            task_function=task_function,
            enabled=True
        )

        self.tasks[task_id] = task
        print(f"✓ Scheduled: {agent_name} - {task_name} at {schedule_time.strftime('%H:%M')}")

        return task_id

    def unschedule(self, task_id: str):
        """Remove a scheduled task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            print(f"✓ Unscheduled: {task_id}")

    def enable_task(self, task_id: str):
        """Enable a task."""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True

    def disable_task(self, task_id: str):
        """Disable a task without removing it."""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False

    def _should_run_task(self, task: ScheduledTask) -> bool:
        """
        Determine if a task should run now.
        """
        if not task.enabled:
            return False

        now = datetime.now()
        current_time = now.time()

        # Check if we're past the scheduled time
        if current_time < task.schedule_time:
            return False

        # Check if already run today
        if task.last_run:
            if task.last_run.date() == now.date():
                # Already ran today
                return False

        return True

    def _run_tasks(self):
        """
        Check and run any tasks that are due.
        """
        for task in self.tasks.values():
            if self._should_run_task(task):
                try:
                    print(f"⏰ Running scheduled task: {task.agent_name} - {task.task_name}")
                    task.task_function()
                    task.last_run = datetime.now()
                except Exception as e:
                    print(f"❌ Error running scheduled task {task.id}: {e}")

    def start(self):
        """
        Start the scheduler in a background thread.
        """
        if self.running:
            print("Scheduler already running")
            return

        self.running = True

        def scheduler_loop():
            print("✓ Scheduler started")
            while self.running:
                self._run_tasks()
                time_module.sleep(self.check_interval)

        thread = threading.Thread(target=scheduler_loop, daemon=True)
        thread.start()

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        print("✓ Scheduler stopped")

    def list_tasks(self) -> List[Dict]:
        """List all scheduled tasks."""
        return [
            {
                'id': task.id,
                'agent': task.agent_name,
                'task': task.task_name,
                'schedule_time': task.schedule_time.strftime('%H:%M'),
                'enabled': task.enabled,
                'last_run': task.last_run.isoformat() if task.last_run else None
            }
            for task in self.tasks.values()
        ]


# Global scheduler instance
scheduler = SimpleScheduler()
