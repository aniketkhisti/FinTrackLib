"""Tests for savings goals functionality."""
import pytest
from datetime import datetime, timedelta
from fintracklib.models import SavingsGoal
from fintracklib.savings import SavingsGoalManager


class TestSavingsGoal:
    """Test SavingsGoal dataclass."""
    
    def test_create_savings_goal(self):
        """Test creating a basic savings goal."""
        goal = SavingsGoal(
            name="Wedding",
            target_amount=500000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        assert goal.name == "Wedding"
        assert goal.target_amount == 500000.0
        assert goal.current_saved == 0.0
        assert goal.id is None
    
    def test_create_goal_with_initial_savings(self):
        """Test creating goal with initial savings."""
        goal = SavingsGoal(
            name="House down payment",
            target_amount=2000000.0,
            current_saved=50000.0,
            deadline=datetime.now() + timedelta(days=730)
        )
        
        assert goal.current_saved == 50000.0
        assert goal.progress_percentage() == 2.5
    
    def test_goal_validation_negative_target(self):
        """Test validation for negative target amount."""
        with pytest.raises(ValueError, match="Target amount must be positive"):
            SavingsGoal(
                name="Test",
                target_amount=-1000.0,
                deadline=datetime.now() + timedelta(days=365)
            )
    
    def test_goal_validation_negative_savings(self):
        """Test validation for negative current savings."""
        with pytest.raises(ValueError, match="Current saved amount cannot be negative"):
            SavingsGoal(
                name="Test",
                target_amount=1000.0,
                current_saved=-100.0,
                deadline=datetime.now() + timedelta(days=365)
            )
    
    def test_goal_validation_past_deadline(self):
        """Test validation for deadline in the past."""
        with pytest.raises(ValueError, match="Deadline must be in the future"):
            SavingsGoal(
                name="Test",
                target_amount=1000.0,
                deadline=datetime.now() - timedelta(days=1)
            )
    
    def test_add_contribution(self):
        """Test adding contributions to goal."""
        goal = SavingsGoal(
            name="Education fund",
            target_amount=100000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        goal.add_contribution(10000.0)
        assert goal.current_saved == 10000.0
        
        goal.add_contribution(5000.0)
        assert goal.current_saved == 15000.0
    
    def test_add_negative_contribution(self):
        """Test adding negative contribution raises error."""
        goal = SavingsGoal(
            name="Test",
            target_amount=1000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        with pytest.raises(ValueError, match="Contribution amount must be positive"):
            goal.add_contribution(-100.0)
    
    def test_progress_percentage(self):
        """Test progress percentage calculation."""
        goal = SavingsGoal(
            name="Test",
            target_amount=100000.0,
            current_saved=25000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        assert goal.progress_percentage() == 25.0
        
        # Test capping at 100%
        goal.current_saved = 150000.0
        assert goal.progress_percentage() == 100.0
    
    def test_remaining_amount(self):
        """Test remaining amount calculation."""
        goal = SavingsGoal(
            name="Test",
            target_amount=100000.0,
            current_saved=30000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        assert goal.remaining_amount() == 70000.0
        
        # Test when exceeded
        goal.current_saved = 120000.0
        assert goal.remaining_amount() == -20000.0
    
    def test_is_exceeded(self):
        """Test exceeded status checking."""
        goal = SavingsGoal(
            name="Test",
            target_amount=100000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        assert not goal.is_exceeded()
        
        goal.current_saved = 100000.0
        assert not goal.is_exceeded()
        
        goal.current_saved = 100001.0
        assert goal.is_exceeded()
    
    def test_excess_amount(self):
        """Test excess amount calculation."""
        goal = SavingsGoal(
            name="Test",
            target_amount=100000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        assert goal.excess_amount() == 0.0
        
        goal.current_saved = 120000.0
        assert goal.excess_amount() == 20000.0
    
    def test_months_remaining(self):
        """Test months remaining calculation."""
        # Test with future deadline
        future_date = datetime.now() + timedelta(days=365)
        goal = SavingsGoal(
            name="Test",
            target_amount=100000.0,
            deadline=future_date
        )
        
        months = goal.months_remaining()
        assert 11 <= months <= 12  # Should be around 12 months
        
        # Test with past deadline - should raise ValueError due to validation
        past_date = datetime.now() - timedelta(days=30)
        with pytest.raises(ValueError, match="Deadline must be in the future"):
            SavingsGoal(
                name="Test Past",
                target_amount=100000.0,
                deadline=past_date
            )
    
    def test_monthly_required(self):
        """Test monthly required calculation."""
        goal = SavingsGoal(
            name="Test",
            target_amount=120000.0,
            current_saved=20000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        monthly_req = goal.monthly_required()
        # Should be around 100000/12 = 8333.33
        assert 8000 <= monthly_req <= 9000
    
    def test_is_on_track(self):
        """Test on-track status checking."""
        goal = SavingsGoal(
            name="Test",
            target_amount=120000.0,
            current_saved=20000.0,
            deadline=datetime.now() + timedelta(days=365)
        )
        
        # Test with sufficient monthly savings
        assert goal.is_on_track(10000.0)
        
        # Test with insufficient monthly savings
        assert not goal.is_on_track(5000.0)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        goal = SavingsGoal(
            name="Test Goal",
            target_amount=50000.0,
            current_saved=10000.0,
            deadline=datetime.now() + timedelta(days=180),
            id=123
        )
        
        goal_dict = goal.to_dict()
        
        assert goal_dict['id'] == 123
        assert goal_dict['name'] == "Test Goal"
        assert goal_dict['target_amount'] == 50000.0
        assert goal_dict['current_saved'] == 10000.0
        assert 'deadline' in goal_dict
        assert goal_dict['progress_percentage'] == 20.0
        assert goal_dict['remaining_amount'] == 40000.0
        assert not goal_dict['is_exceeded']


class TestSavingsGoalManager:
    """Test SavingsGoalManager class."""
    
    def test_create_manager(self):
        """Test creating a new manager."""
        manager = SavingsGoalManager()
        assert manager.goals == []
        assert manager._next_id == 1
    
    def test_create_goal(self):
        """Test creating a goal through manager."""
        manager = SavingsGoalManager()
        goal = manager.create_goal("Wedding", 500000.0)
        
        assert goal.name == "Wedding"
        assert goal.target_amount == 500000.0
        assert goal.id == 1
        assert len(manager.goals) == 1
        assert manager._next_id == 2
    
    def test_create_goal_with_deadline(self):
        """Test creating goal with custom deadline."""
        manager = SavingsGoalManager()
        deadline = datetime.now() + timedelta(days=730)
        goal = manager.create_goal("House", 2000000.0, deadline)
        
        assert goal.deadline == deadline
    
    def test_get_goal(self):
        """Test retrieving goal by ID."""
        manager = SavingsGoalManager()
        goal1 = manager.create_goal("Goal 1", 100000.0)
        goal2 = manager.create_goal("Goal 2", 200000.0)
        
        retrieved = manager.get_goal(goal1.id)
        assert retrieved == goal1
        
        retrieved = manager.get_goal(goal2.id)
        assert retrieved == goal2
        
        retrieved = manager.get_goal(999)
        assert retrieved is None
    
    def test_add_contribution(self):
        """Test adding contribution through manager."""
        manager = SavingsGoalManager()
        goal = manager.create_goal("Test", 100000.0)
        
        success = manager.add_contribution(goal.id, 10000.0)
        assert success
        assert goal.current_saved == 10000.0
        
        # Test with non-existent goal
        success = manager.add_contribution(999, 1000.0)
        assert not success
    
    def test_get_all_goals(self):
        """Test getting all goals."""
        manager = SavingsGoalManager()
        goal1 = manager.create_goal("Goal 1", 100000.0)
        goal2 = manager.create_goal("Goal 2", 200000.0)
        
        all_goals = manager.get_all_goals()
        assert len(all_goals) == 2
        assert goal1 in all_goals
        assert goal2 in all_goals
    
    def test_get_goals_by_status(self):
        """Test filtering goals by exceeded status."""
        manager = SavingsGoalManager()
        goal1 = manager.create_goal("Normal", 100000.0)
        goal2 = manager.create_goal("Exceeded", 100000.0)
        
        # Make goal2 exceeded
        goal2.current_saved = 150000.0
        
        normal_goals = manager.get_goals_by_status(exceeded=False)
        exceeded_goals = manager.get_goals_by_status(exceeded=True)
        all_goals = manager.get_goals_by_status(exceeded=None)
        
        assert len(normal_goals) == 1
        assert normal_goals[0] == goal1
        assert len(exceeded_goals) == 1
        assert exceeded_goals[0] == goal2
        assert len(all_goals) == 2
    
    def test_get_goals_due_soon(self):
        """Test getting goals due soon."""
        manager = SavingsGoalManager()
        
        # Goal due in 3 months
        soon_date = datetime.now() + timedelta(days=90)
        goal_soon = manager.create_goal("Soon", 100000.0, soon_date)
        
        # Goal due in 1 year
        later_date = datetime.now() + timedelta(days=365)
        goal_later = manager.create_goal("Later", 200000.0, later_date)
        
        due_soon = manager.get_goals_due_soon(months=6)
        assert len(due_soon) == 1
        assert due_soon[0] == goal_soon
    
    def test_get_total_saved(self):
        """Test getting total saved amount."""
        manager = SavingsGoalManager()
        goal1 = manager.create_goal("Goal 1", 100000.0)
        goal2 = manager.create_goal("Goal 2", 200000.0)
        
        goal1.current_saved = 30000.0
        goal2.current_saved = 50000.0
        
        total = manager.get_total_saved()
        assert total == 80000.0
    
    def test_get_total_target(self):
        """Test getting total target amount."""
        manager = SavingsGoalManager()
        manager.create_goal("Goal 1", 100000.0)
        manager.create_goal("Goal 2", 200000.0)
        
        total = manager.get_total_target()
        assert total == 300000.0
    
    def test_get_overall_progress(self):
        """Test getting overall progress."""
        manager = SavingsGoalManager()
        goal1 = manager.create_goal("Goal 1", 100000.0)
        goal2 = manager.create_goal("Goal 2", 200000.0)
        
        goal1.current_saved = 50000.0
        goal2.current_saved = 100000.0
        
        progress = manager.get_overall_progress()
        # (50000 + 100000) / (100000 + 200000) * 100 = 50%
        assert progress == 50.0
    
    def test_generate_summary_report(self):
        """Test generating summary report."""
        manager = SavingsGoalManager()
        
        # Test empty report
        report = manager.generate_summary_report()
        assert "No savings goals set yet." in report
        
        # Test with goals
        goal1 = manager.create_goal("Wedding", 500000.0)
        goal2 = manager.create_goal("House", 2000000.0)
        
        goal1.current_saved = 100000.0
        goal2.current_saved = 500000.0
        
        report = manager.generate_summary_report()
        assert "SAVINGS GOALS SUMMARY" in report
        assert "Wedding" in report
        assert "House" in report
        assert "₹5,00,000.00" in report  # Target amount
        assert "₹1,00,000.00" in report  # Saved amount
        assert "OVERALL SUMMARY" in report
    
    def test_delete_goal(self):
        """Test deleting a goal."""
        manager = SavingsGoalManager()
        goal1 = manager.create_goal("Goal 1", 100000.0)
        goal2 = manager.create_goal("Goal 2", 200000.0)
        
        # Delete goal1
        success = manager.delete_goal(goal1.id)
        assert success
        assert len(manager.goals) == 1
        assert manager.goals[0] == goal2
        
        # Try to delete non-existent goal
        success = manager.delete_goal(999)
        assert not success
    
    def test_update_goal_deadline(self):
        """Test updating goal deadline."""
        manager = SavingsGoalManager()
        goal = manager.create_goal("Test", 100000.0)
        new_deadline = datetime.now() + timedelta(days=730)
        
        success = manager.update_goal_deadline(goal.id, new_deadline)
        assert success
        assert goal.deadline == new_deadline
        
        # Test with non-existent goal
        success = manager.update_goal_deadline(999, new_deadline)
        assert not success
        
        # Test with past deadline
        past_deadline = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError, match="Deadline must be in the future"):
            manager.update_goal_deadline(goal.id, past_deadline)


class TestSavingsGoalsIntegration:
    """Integration tests for savings goals with Indian context."""
    
    def test_indian_wedding_goal(self):
        """Test realistic Indian wedding savings goal."""
        manager = SavingsGoalManager()
        
        # Create wedding goal: ₹5,00,000 in 2 years
        wedding_deadline = datetime.now() + timedelta(days=730)
        wedding_goal = manager.create_goal(
            "Wedding Expenses", 
            500000.0, 
            wedding_deadline
        )
        
        # Add some contributions
        manager.add_contribution(wedding_goal.id, 50000.0)  # Initial savings
        manager.add_contribution(wedding_goal.id, 25000.0)  # Bonus
        
        assert wedding_goal.current_saved == 75000.0
        assert wedding_goal.progress_percentage() == 15.0
        assert wedding_goal.remaining_amount() == 425000.0
        
        # Check monthly requirement
        monthly_req = wedding_goal.monthly_required()
        assert 15000 <= monthly_req <= 20000  # Around ₹17,000 per month
    
    def test_house_down_payment_goal(self):
        """Test house down payment goal with Indian amounts."""
        manager = SavingsGoalManager()
        
        # House worth ₹50,00,000, need 20% down payment = ₹10,00,000
        house_goal = manager.create_goal(
            "House Down Payment",
            1000000.0,  # ₹10 lakh
            datetime.now() + timedelta(days=1095)  # 3 years
        )
        
        # Add some savings
        manager.add_contribution(house_goal.id, 200000.0)  # ₹2 lakh saved
        
        assert house_goal.progress_percentage() == 20.0
        assert house_goal.remaining_amount() == 800000.0
        
        # Check if saving ₹25,000/month is on track
        assert house_goal.is_on_track(25000.0)
        assert not house_goal.is_on_track(15000.0)
    
    def test_education_fund_goal(self):
        """Test education fund goal."""
        manager = SavingsGoalManager()
        
        # Child's education fund: ₹15,00,000 in 10 years
        education_goal = manager.create_goal(
            "Child Education Fund",
            1500000.0,  # ₹15 lakh
            datetime.now() + timedelta(days=3650)  # 10 years
        )
        
        # Add some initial savings
        manager.add_contribution(education_goal.id, 100000.0)  # ₹1 lakh
        
        assert abs(education_goal.progress_percentage() - 6.67) < 0.01
        assert education_goal.months_remaining() >= 110  # Around 10 years
        
        # Monthly requirement should be around ₹11,700
        monthly_req = education_goal.monthly_required()
        assert 11000 <= monthly_req <= 12000
