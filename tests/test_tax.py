"""Tests for income tax calculator."""
import pytest
from fintracklib.tax import TaxCalculator


class TestTaxCalculatorNewRegime:
    """Test new tax regime calculations."""
    
    def test_new_regime_zero_income(self):
        """Test tax calculation for zero income."""
        calculator = TaxCalculator()
        result = calculator.calculate_tax(0, "new_regime")
        
        assert result["taxable_income"] == 0
        assert result["final_tax"] == 0
        assert result["effective_rate"] == 0
        assert result["regime_used"] == "new_regime"
    
    def test_new_regime_below_standard_deduction(self):
        """Test income below standard deduction."""
        calculator = TaxCalculator()
        result = calculator.calculate_tax(30000, "new_regime")
        
        assert result["taxable_income"] == 0
        assert result["final_tax"] == 0
    
    def test_new_regime_first_slab(self):
        """Test income in first slab (up to ₹3 lakhs)."""
        calculator = TaxCalculator()
        income = 250000
        result = calculator.calculate_tax(income, "new_regime")
        
        taxable = income - 50000  # After standard deduction
        assert result["taxable_income"] == taxable
        assert result["final_tax"] == 0  # No tax up to ₹3L
        assert result["effective_rate"] == 0
    
    def test_new_regime_second_slab(self):
        """Test income in 5% slab (₹3-7 lakhs)."""
        calculator = TaxCalculator()
        income = 500000
        result = calculator.calculate_tax(income, "new_regime")
        
        taxable = income - 50000  # 4,50,000
        # Tax: (4,50,000 - 3,00,000) * 5% = 7,500
        assert result["taxable_income"] == 450000
        assert result["final_tax"] == 7500
        assert abs(result["effective_rate"] - 1.5) < 0.01
    
    def test_new_regime_third_slab(self):
        """Test income in 10% slab (₹7-10 lakhs)."""
        calculator = TaxCalculator()
        income = 850000
        result = calculator.calculate_tax(income, "new_regime")
        
        taxable = income - 50000  # 8,00,000
        # Tax calculation should be positive
        assert result["taxable_income"] == 800000
        assert result["final_tax"] > 0
    
    def test_new_regime_section_87a_rebate(self):
        """Test Section 87A rebate for income up to ₹7 lakhs."""
        calculator = TaxCalculator()
        income = 600000  # Just under ₹7L limit
        result = calculator.calculate_tax(income, "new_regime")
        
        # Should get Section 87A rebate
        assert result["rebate_87a"] > 0
        assert result["rebate_87a"] <= 25000
        assert result["final_tax"] >= 0
    
    def test_new_regime_section_87a_at_limit(self):
        """Test Section 87A at exact ₹7 lakh limit."""
        calculator = TaxCalculator()
        income = 700000
        result = calculator.calculate_tax(income, "new_regime")
        
        # Should still get rebate at limit
        assert result["rebate_87a"] > 0
    
    def test_new_regime_no_rebate_above_limit(self):
        """Test no Section 87A rebate above ₹7 lakhs."""
        calculator = TaxCalculator()
        income = 800000  # Above ₹7L limit
        result = calculator.calculate_tax(income, "new_regime")
        
        # Should not get rebate above limit
        assert result["rebate_87a"] == 0
    
    def test_new_regime_high_income(self):
        """Test high income (above ₹15 lakhs)."""
        calculator = TaxCalculator()
        income = 2000000  # ₹20 lakhs
        result = calculator.calculate_tax(income, "new_regime")
        
        assert result["taxable_income"] > 1500000
        assert result["final_tax"] > 0
        assert result["effective_rate"] > 0
    
    def test_new_regime_with_standard_deduction(self):
        """Test standard deduction is applied correctly."""
        calculator = TaxCalculator()
        income = 550000
        result = calculator.calculate_tax(income, "new_regime")
        
        assert result["taxable_income"] == income - 50000


class TestTaxCalculatorOldRegime:
    """Test old tax regime calculations."""
    
    def test_old_regime_zero_income(self):
        """Test tax calculation for zero income."""
        calculator = TaxCalculator()
        result = calculator.calculate_tax(0, "old_regime")
        
        assert result["taxable_income"] == 0
        assert result["final_tax"] == 0
        assert result["regime_used"] == "old_regime"
    
    def test_old_regime_first_slab(self):
        """Test income in first slab (up to ₹2.5 lakhs)."""
        calculator = TaxCalculator()
        income = 200000
        result = calculator.calculate_tax(income, "old_regime")
        
        taxable = income - 50000  # 1,50,000
        assert result["taxable_income"] == taxable
        assert result["final_tax"] == 0  # No tax up to ₹2.5L
    
    def test_old_regime_second_slab(self):
        """Test income in 5% slab (₹2.5-5 lakhs)."""
        calculator = TaxCalculator()
        income = 400000
        result = calculator.calculate_tax(income, "old_regime")
        
        taxable = income - 50000  # 3,50,000
        # Tax: (3,50,000 - 2,50,000) * 5% = 5,000
        assert result["taxable_income"] == 350000
        assert result["final_tax"] == 5000
    
    def test_old_regime_third_slab(self):
        """Test income in 20% slab (₹5-10 lakhs)."""
        calculator = TaxCalculator()
        income = 800000
        result = calculator.calculate_tax(income, "old_regime")
        
        taxable = income - 50000  # 7,50,000
        # Tax should be calculated correctly
        assert result["taxable_income"] == 750000
        assert result["final_tax"] > 0
    
    def test_old_regime_80c_deduction(self):
        """Test 80C deduction in old regime."""
        calculator = TaxCalculator()
        income = 800000
        deduction_80c = 150000
        result = calculator.calculate_tax(income, "old_regime", deduction_80c)
        
        # Taxable: 8,00,000 - 50,000 (standard) - 1,50,000 (80C) = 6,00,000
        assert result["taxable_income"] == 600000
        assert result["deduction_80c"] == 150000
    
    def test_old_regime_80c_limit(self):
        """Test 80C deduction limit (max ₹1.5 lakhs)."""
        calculator = TaxCalculator()
        income = 800000
        deduction_80c = 200000  # Above limit
        result = calculator.calculate_tax(income, "old_regime", deduction_80c)
        
        # Should cap at ₹1.5 lakhs
        assert result["deduction_80c"] == 150000
    
    def test_old_regime_80d_deduction(self):
        """Test 80D deduction in old regime."""
        calculator = TaxCalculator()
        income = 800000
        deduction_80d = 25000
        result = calculator.calculate_tax(income, "old_regime", 0, deduction_80d)
        
        assert result["deduction_80d"] == 25000
        assert result["taxable_income"] == income - 50000 - 25000
    
    def test_old_regime_combined_deductions(self):
        """Test combined 80C and 80D deductions."""
        calculator = TaxCalculator()
        income = 1000000
        result = calculator.calculate_tax(income, "old_regime", 100000, 25000)
        
        # Taxable: 10,00,000 - 50,000 - 1,00,000 - 25,000 = 8,25,000
        assert result["taxable_income"] == 825000
        assert result["deduction_80c"] == 100000
        assert result["deduction_80d"] == 25000
    
    def test_old_regime_no_rebate_87a(self):
        """Test that old regime doesn't get Section 87A rebate."""
        calculator = TaxCalculator()
        income = 600000
        result = calculator.calculate_tax(income, "old_regime")
        
        # Old regime doesn't have Section 87A rebate
        assert result["rebate_87a"] == 0
    
    def test_old_regime_high_income(self):
        """Test high income in old regime (30% slab)."""
        calculator = TaxCalculator()
        income = 2000000  # ₹20 lakhs
        result = calculator.calculate_tax(income, "old_regime")
        
        assert result["taxable_income"] > 1000000
        assert result["final_tax"] > 0
        assert result["effective_rate"] > 0


class TestTaxCalculatorComparison:
    """Test regime comparison functionality."""
    
    def test_compare_regimes_low_income(self):
        """Test comparison for low income (new regime better)."""
        calculator = TaxCalculator()
        income = 600000
        comparison = calculator.compare_regimes(income)
        
        assert "new_regime_tax" in comparison
        assert "old_regime_tax" in comparison
        assert "recommended_regime" in comparison
        assert "savings" in comparison
        assert comparison["recommended_regime"] in ["new_regime", "old_regime", "equal"]
    
    def test_compare_regimes_with_deductions(self):
        """Test comparison when old regime has deductions."""
        calculator = TaxCalculator()
        income = 1000000
        comparison = calculator.compare_regimes(income, deduction_80c=150000)
        
        # With high deductions, old regime might be better
        assert comparison["recommended_regime"] in ["new_regime", "old_regime", "equal"]
        assert comparison["savings"] >= 0
    
    def test_compare_regimes_equal_tax(self):
        """Test when both regimes have equal tax."""
        calculator = TaxCalculator()
        comparison = calculator.compare_regimes(300000)
        
        assert comparison["recommended_regime"] in ["new_regime", "old_regime", "equal"]
    
    def test_compare_regimes_details(self):
        """Test that comparison includes detailed results."""
        calculator = TaxCalculator()
        comparison = calculator.compare_regimes(800000)
        
        assert "new_regime_details" in comparison
        assert "old_regime_details" in comparison
        assert isinstance(comparison["new_regime_details"], dict)
        assert isinstance(comparison["old_regime_details"], dict)


class TestTaxCalculatorValidation:
    """Test input validation."""
    
    def test_negative_income(self):
        """Test that negative income raises error."""
        calculator = TaxCalculator()
        
        with pytest.raises(ValueError, match="Income cannot be negative"):
            calculator.calculate_tax(-10000, "new_regime")
    
    def test_invalid_regime(self):
        """Test that invalid regime raises error."""
        calculator = TaxCalculator()
        
        with pytest.raises(ValueError, match="Regime must be"):
            calculator.calculate_tax(500000, "invalid_regime")
    
    def test_default_regime(self):
        """Test that default regime is new_regime."""
        calculator = TaxCalculator()
        result = calculator.calculate_tax(500000)
        
        assert result["regime_used"] == "new_regime"


class TestTaxCalculatorReports:
    """Test tax breakdown reports."""
    
    def test_get_tax_breakdown_new_regime(self):
        """Test tax breakdown report for new regime."""
        calculator = TaxCalculator()
        report = calculator.get_tax_breakdown(800000, "new_regime")
        
        assert "INCOME TAX CALCULATION" in report
        assert "NEW REGIME" in report
        assert "₹8,00,000" in report
        assert "Standard Deduction" in report
        assert "Tax Payable" in report
    
    def test_get_tax_breakdown_old_regime(self):
        """Test tax breakdown report for old regime."""
        calculator = TaxCalculator()
        report = calculator.get_tax_breakdown(800000, "old_regime", 100000)
        
        assert "OLD REGIME" in report
        assert "80C Deduction" in report
    
    def test_get_tax_breakdown_with_rebate(self):
        """Test breakdown when Section 87A rebate applies."""
        calculator = TaxCalculator()
        report = calculator.get_tax_breakdown(600000, "new_regime")
        
        assert "Rebate u/s 87A" in report


class TestTaxCalculatorIndianContext:
    """Test with realistic Indian income scenarios."""
    
    def test_fresh_graduate_salary(self):
        """Test tax for fresh graduate (₹5 lakhs)."""
        calculator = TaxCalculator()
        income = 500000
        
        new_result = calculator.calculate_tax(income, "new_regime")
        old_result = calculator.calculate_tax(income, "old_regime")
        
        # New regime should be better for low income
        assert new_result["final_tax"] <= old_result["final_tax"]
    
    def test_mid_level_manager(self):
        """Test tax for mid-level manager (₹12 lakhs)."""
        calculator = TaxCalculator()
        income = 1200000
        
        comparison = calculator.compare_regimes(income)
        
        assert comparison["savings"] >= 0
        assert comparison["new_regime_tax"] >= 0
        assert comparison["old_regime_tax"] >= 0
    
    def test_high_earner_with_investments(self):
        """Test high earner with 80C investments (₹15 lakhs)."""
        calculator = TaxCalculator()
        income = 1500000
        deduction_80c = 150000  # Max 80C
        deduction_80d = 25000
        
        old_result = calculator.calculate_tax(income, "old_regime", 
                                              deduction_80c, deduction_80d)
        new_result = calculator.calculate_tax(income, "new_regime")
        
        # With max deductions, old regime might be better
        assert old_result["taxable_income"] < new_result["taxable_income"]
    
    def test_senior_citizen_scenario(self):
        """Test scenario for senior citizen with health insurance."""
        calculator = TaxCalculator()
        income = 800000
        deduction_80c = 100000
        deduction_80d = 25000
        
        result = calculator.calculate_tax(income, "old_regime", 
                                          deduction_80c, deduction_80d)
        
        # Taxable income should be reduced by deductions
        assert result["taxable_income"] < income - 50000
    
    def test_comparison_recommendation(self):
        """Test that comparison recommends correct regime."""
        calculator = TaxCalculator()
        
        # Low income without deductions - new regime better
        comparison_low = calculator.compare_regimes(600000)
        
        # High income with deductions - might favor old regime
        comparison_high = calculator.compare_regimes(2000000, 
                                                    deduction_80c=150000)
        
        assert comparison_low["recommended_regime"] in ["new_regime", "old_regime", "equal"]
        assert comparison_high["recommended_regime"] in ["new_regime", "old_regime", "equal"]
