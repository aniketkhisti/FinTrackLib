"""Savings goals management for major life events."""
from datetime import datetime, timedelta
from typing import List, Optional
from .models import SavingsGoal
from .utils import format_inr


class SavingsGoalManager:
    """Manages multiple savings goals for major life events.
    
    Provides functionality to create, track, and manage savings goals
    with Indian context and INR formatting.
    """
    
    def __init__(self):
        """Initialize the savings goal manager."""
        self.goals: List[SavingsGoal] = []
        self._next_id = 1
    
    def create_goal(self, name: str, target_amount: float, 
                   deadline: Optional[datetime] = None) -> SavingsGoal:
        """Create a new savings goal.
        
        Args:
            name: Goal name (e.g., "Wedding", "House down payment")
            target_amount: Target amount to save in INR
            deadline: Target date (defaults to 1 year from now)
            
        Returns:
            Created SavingsGoal object
            
        Raises:
            ValueError: If target_amount is not positive
        """
        if deadline is None:
            deadline = datetime.now() + timedelta(days=365)
        
        goal = SavingsGoal(
            name=name,
            target_amount=target_amount,
            deadline=deadline,
            id=self._next_id
        )
        
        self.goals.append(goal)
        self._next_id += 1
        return goal
    
    def get_goal(self, goal_id: int) -> Optional[SavingsGoal]:
        """Get a savings goal by ID.
        
        Args:
            goal_id: Goal ID to find
            
        Returns:
            SavingsGoal object if found, None otherwise
        """
        for goal in self.goals:
            if goal.id == goal_id:
                return goal
        return None
    
    def add_contribution(self, goal_id: int, amount: float) -> bool:
        """Add a contribution to a savings goal.
        
        Args:
            goal_id: ID of the goal to contribute to
            amount: Amount to contribute
            
        Returns:
            True if contribution added successfully, False if goal not found
            
        Raises:
            ValueError: If amount is not positive
        """
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        goal.add_contribution(amount)
        return True
    
    def get_all_goals(self) -> List[SavingsGoal]:
        """Get all savings goals.
        
        Returns:
            List of all SavingsGoal objects
        """
        return self.goals.copy()
    
    def get_goals_by_status(self, exceeded: bool = None) -> List[SavingsGoal]:
        """Get goals filtered by exceeded status.
        
        Args:
            exceeded: True for exceeded goals, False for not exceeded, None for all
            
        Returns:
            List of filtered SavingsGoal objects
        """
        if exceeded is None:
            return self.goals.copy()
        
        return [goal for goal in self.goals if goal.is_exceeded() == exceeded]
    
    def get_goals_due_soon(self, months: int = 6) -> List[SavingsGoal]:
        """Get goals that are due within specified months.
        
        Args:
            months: Number of months to look ahead (default: 6)
            
        Returns:
            List of goals due within the specified period
        """
        cutoff_date = datetime.now() + timedelta(days=months * 30)
        return [goal for goal in self.goals if goal.deadline <= cutoff_date]
    
    def get_total_saved(self) -> float:
        """Get total amount saved across all goals.
        
        Returns:
            Total amount saved in INR
        """
        return sum(goal.current_saved for goal in self.goals)
    
    def get_total_target(self) -> float:
        """Get total target amount across all goals.
        
        Returns:
            Total target amount in INR
        """
        return sum(goal.target_amount for goal in self.goals)
    
    def get_overall_progress(self) -> float:
        """Get overall progress across all goals.
        
        Returns:
            Overall progress percentage (0-100)
        """
        total_target = self.get_total_target()
        if total_target == 0:
            return 0.0
        
        total_saved = self.get_total_saved()
        return min((total_saved / total_target) * 100, 100.0)
    
    def generate_summary_report(self) -> str:
        """Generate a formatted summary report of all goals.
        
        Returns:
            Formatted string report with INR amounts
        """
        if not self.goals:
            return "No savings goals set yet."
        
        report = []
        report.append("=" * 50)
        report.append("SAVINGS GOALS SUMMARY")
        report.append("=" * 50)
        report.append("")
        
        # Individual goals
        for goal in self.goals:
            status = "✓ EXCEEDED" if goal.is_exceeded() else f"{goal.progress_percentage():.1f}%"
            report.append(f"{goal.name}:")
            report.append(f"  Target: {format_inr(goal.target_amount)}")
            report.append(f"  Saved:  {format_inr(goal.current_saved)}")
            report.append(f"  Status: {status}")
            
            if goal.is_exceeded():
                excess = goal.excess_amount()
                report.append(f"  Excess: {format_inr(excess)}")
            else:
                remaining = goal.remaining_amount()
                monthly_req = goal.monthly_required()
                report.append(f"  Remaining: {format_inr(remaining)}")
                if monthly_req > 0:
                    report.append(f"  Monthly needed: {format_inr(monthly_req)}")
            
            report.append("")
        
        # Overall summary
        total_saved = self.get_total_saved()
        total_target = self.get_total_target()
        overall_progress = self.get_overall_progress()
        
        report.append("-" * 30)
        report.append("OVERALL SUMMARY")
        report.append("-" * 30)
        report.append(f"Total saved: {format_inr(total_saved)}")
        report.append(f"Total target: {format_inr(total_target)}")
        report.append(f"Overall progress: {overall_progress:.1f}%")
        report.append("=" * 50)
        
        return "\n".join(report)
    
    def delete_goal(self, goal_id: int) -> bool:
        """Delete a savings goal.
        
        Args:
            goal_id: ID of the goal to delete
            
        Returns:
            True if goal deleted successfully, False if not found
        """
        for i, goal in enumerate(self.goals):
            if goal.id == goal_id:
                del self.goals[i]
                return True
        return False
    
    def update_goal_deadline(self, goal_id: int, new_deadline: datetime) -> bool:
        """Update a goal's deadline.
        
        Args:
            goal_id: ID of the goal to update
            new_deadline: New deadline date
            
        Returns:
            True if updated successfully, False if goal not found
            
        Raises:
            ValueError: If new deadline is in the past
        """
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        if new_deadline <= datetime.now():
            raise ValueError("Deadline must be in the future")
        
        goal.deadline = new_deadline
        return True
