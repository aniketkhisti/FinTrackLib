"""Income tax calculator for Indian tax slabs (FY 2024-25)."""
from typing import Dict, Optional
from .utils import format_inr


class TaxCalculator:
    """Calculate income tax for Indian tax slabs.
    
    Supports both Old Tax Regime (with deductions) and New Tax Regime
    (lower rates, no deductions) for FY 2024-25.
    """
    
    # New Tax Regime Slabs (FY 2024-25)
    NEW_REGIME_SLABS = [
        (0, 300000, 0),           # Up to ₹3 lakhs: Nil
        (300000, 700000, 5),       # ₹3-7 lakhs: 5%
        (700000, 1000000, 10),     # ₹7-10 lakhs: 10%
        (1000000, 1200000, 15),    # ₹10-12 lakhs: 15%
        (1200000, 1500000, 20),    # ₹12-15 lakhs: 20%
        (1500000, float('inf'), 30),  # Above ₹15 lakhs: 30%
    ]
    
    # Old Tax Regime Slabs (FY 2024-25)
    OLD_REGIME_SLABS = [
        (0, 250000, 0),            # Up to ₹2.5 lakhs: Nil
        (250000, 500000, 5),       # ₹2.5-5 lakhs: 5%
        (500000, 1000000, 20),     # ₹5-10 lakhs: 20%
        (1000000, float('inf'), 30),  # Above ₹10 lakhs: 30%
    ]
    
    STANDARD_DEDUCTION = 50000  # ₹50,000 standard deduction
    
    # Section 87A rebate limit (new regime)
    REBATE_87A_LIMIT = 700000  # ₹7 lakhs
    REBATE_87A_AMOUNT = 12500  # Maximum rebate ₹12,500 (FY 2024-25)
    
    def __init__(self):
        """Initialize the tax calculator."""
        pass
    
    def calculate_tax(self, income: float, regime: str = "new_regime",
                      deduction_80c: float = 0.0, deduction_80d: float = 0.0,
                      months_worked: Optional[int] = None) -> Dict:
        """Calculate income tax based on income and regime.
        
        Args:
            income: Actual income earned in INR (not annualized)
            regime: Tax regime - "new_regime" or "old_regime" (default: "new_regime")
            deduction_80c: 80C deduction amount (for old regime only)
            deduction_80d: 80D deduction amount (for old regime only)
            months_worked: Number of months worked (for partial year). If None, assumes full year (12 months)
            
        Returns:
            Dictionary containing:
            - taxable_income: Income after deductions
            - tax_before_rebate: Tax calculated before rebate
            - rebate_87a: Section 87A rebate amount
            - surcharge: Surcharge amount (for high income)
            - marginal_relief: Marginal relief amount (if applicable)
            - final_tax: Final tax payable
            - effective_rate: Effective tax rate as percentage
            - regime_used: Which regime was used
            - months_worked: Number of months worked (if partial year)
        """
        if income < 0:
            raise ValueError("Income cannot be negative")
        
        if regime not in ["new_regime", "old_regime"]:
            raise ValueError("Regime must be 'new_regime' or 'old_regime'")
        
        # Handle partial year employment - use actual income, don't annualize
        if months_worked is not None:
            if months_worked < 1 or months_worked > 12:
                raise ValueError("months_worked must be between 1 and 12")
            # Use actual income as-is for partial year calculations
            # Tax is calculated on actual income, not annualized
            pass
        
        if regime == "new_regime":
            return self._calculate_new_regime(income, months_worked)
        else:
            return self._calculate_old_regime(income, deduction_80c, deduction_80d, months_worked)
    
    def _calculate_new_regime(self, income: float, months_worked: Optional[int] = None) -> Dict:
        """Calculate tax under new tax regime.
        
        New regime features:
        - Standard deduction of ₹50,000
        - Lower tax rates
        - Section 87A rebate for income up to ₹7 lakhs
        """
        # Apply standard deduction
        taxable_income = max(0, income - self.STANDARD_DEDUCTION)
        
        # Calculate tax based on slabs
        tax_before_rebate = self._calculate_tax_by_slabs(taxable_income, self.NEW_REGIME_SLABS)
        
        # Apply Section 87A rebate (for income up to ₹7 lakhs, inclusive)
        rebate_87a = 0.0
        if income <= self.REBATE_87A_LIMIT:
            rebate_87a = min(tax_before_rebate, self.REBATE_87A_AMOUNT)
        
        # Calculate surcharge for high income (new regime)
        surcharge = self._calculate_surcharge(tax_before_rebate, income)
        
        # Calculate marginal relief for surcharge
        marginal_relief = self._calculate_marginal_relief(income, tax_before_rebate, surcharge)
        surcharge_after_relief = max(0, surcharge - marginal_relief)
        
        # Final tax = tax_before_rebate - rebate + surcharge (after marginal relief)
        final_tax = max(0, tax_before_rebate - rebate_87a + surcharge_after_relief)
        effective_rate = (final_tax / income * 100) if income > 0 else 0.0
        
        result = {
            "taxable_income": taxable_income,
            "tax_before_rebate": tax_before_rebate,
            "rebate_87a": rebate_87a,
            "surcharge": surcharge_after_relief,
            "marginal_relief": marginal_relief,
            "final_tax": final_tax,
            "effective_rate": effective_rate,
            "regime_used": "new_regime"
        }
        
        if months_worked is not None:
            result["months_worked"] = months_worked
        
        return result
    
    def _calculate_old_regime(self, income: float, deduction_80c: float, 
                             deduction_80d: float, months_worked: Optional[int] = None) -> Dict:
        """Calculate tax under old tax regime.
        
        Old regime features:
        - Standard deduction of ₹50,000
        - 80C and 80D deductions
        - Higher tax rates but more deductions available
        """
        # Apply standard deduction
        taxable_income = income - self.STANDARD_DEDUCTION
        
        # Apply 80C and 80D deductions (with limits)
        deduction_80c = min(deduction_80c, 150000)  # 80C limit: ₹1.5 lakhs
        deduction_80d = min(deduction_80d, 25000)     # 80D limit: ₹25,000 for self/family
        
        taxable_income = max(0, taxable_income - deduction_80c - deduction_80d)
        
        # Calculate tax based on old regime slabs
        tax_before_rebate = self._calculate_tax_by_slabs(taxable_income, self.OLD_REGIME_SLABS)
        
        # No Section 87A rebate in old regime (only applicable to new regime)
        rebate_87a = 0.0
        
        # Calculate surcharge for high income (old regime)
        surcharge = self._calculate_surcharge(tax_before_rebate, income)
        
        # Calculate marginal relief for surcharge
        marginal_relief = self._calculate_marginal_relief(income, tax_before_rebate, surcharge)
        surcharge_after_relief = max(0, surcharge - marginal_relief)
        
        final_tax = tax_before_rebate + surcharge_after_relief
        effective_rate = (final_tax / income * 100) if income > 0 else 0.0
        
        result = {
            "taxable_income": taxable_income,
            "tax_before_rebate": tax_before_rebate,
            "rebate_87a": rebate_87a,
            "surcharge": surcharge_after_relief,
            "marginal_relief": marginal_relief,
            "final_tax": final_tax,
            "effective_rate": effective_rate,
            "regime_used": "old_regime",
            "deduction_80c": deduction_80c,
            "deduction_80d": deduction_80d
        }
        
        if months_worked is not None:
            result["months_worked"] = months_worked
        
        return result
    
    def _calculate_tax_by_slabs(self, income: float, slabs: list) -> float:
        """Calculate tax based on tax slabs.
        
        Args:
            income: Taxable income
            slabs: List of tuples (min, max, rate)
            
        Returns:
            Total tax amount
        """
        tax = 0.0
        
        for min_income, max_income, rate in slabs:
            if income <= min_income:
                break
            
            taxable_in_slab = min(income, max_income) - min_income
            tax += (taxable_in_slab * rate) / 100
        
        return tax
    
    def _calculate_surcharge(self, tax_before_rebate: float, income: float) -> float:
        """Calculate surcharge based on income level.
        
        Surcharge rates (FY 2024-25):
        - 10% for income ₹50L-₹1Cr
        - 15% for income ₹1Cr-₹2Cr
        - 25% for income >₹2Cr
        
        Args:
            tax_before_rebate: Tax calculated before rebate
            income: Annual income
            
        Returns:
            Surcharge amount
        """
        if income <= 5000000:  # Up to ₹50 lakhs
            return 0.0
        elif income <= 10000000:  # ₹50L-₹1Cr
            return tax_before_rebate * 0.10
        elif income <= 20000000:  # ₹1Cr-₹2Cr
            return tax_before_rebate * 0.15
        else:  # Above ₹2Cr
            return tax_before_rebate * 0.25
    
    def _calculate_marginal_relief(self, income: float, tax_before_rebate: float, 
                                   surcharge: float) -> float:
        """Calculate marginal relief for surcharge.
        
        Marginal relief ensures that additional tax (tax + surcharge) doesn't exceed
        the additional income earned above the threshold.
        
        Formula: Relief = (tax + surcharge) - (income - threshold) - tax_at_threshold
        
        Args:
            income: Annual income
            tax_before_rebate: Tax calculated before rebate
            surcharge: Surcharge amount
            
        Returns:
            Marginal relief amount (if applicable)
        """
        if surcharge == 0:
            return 0.0
        
        # Thresholds for marginal relief
        if income > 5000000 and income <= 10000000:  # ₹50L-₹1Cr
            threshold = 5000000
            # Calculate tax at threshold (₹50L)
            # For simplicity, using approximate calculation
            # In practice, this would need exact tax calculation at threshold
            threshold_tax_approx = tax_before_rebate * (threshold / income)
            excess_income = income - threshold
            excess_tax = tax_before_rebate + surcharge - threshold_tax_approx
            
            # Marginal relief = excess tax - excess income
            if excess_tax > excess_income:
                relief = excess_tax - excess_income
                return min(relief, surcharge)
        
        elif income > 10000000 and income <= 20000000:  # ₹1Cr-₹2Cr
            threshold = 10000000
            threshold_tax_approx = tax_before_rebate * (threshold / income)
            excess_income = income - threshold
            excess_tax = tax_before_rebate + surcharge - threshold_tax_approx
            
            if excess_tax > excess_income:
                relief = excess_tax - excess_income
                return min(relief, surcharge)
        
        elif income > 20000000:  # Above ₹2Cr
            threshold = 20000000
            threshold_tax_approx = tax_before_rebate * (threshold / income)
            excess_income = income - threshold
            excess_tax = tax_before_rebate + surcharge - threshold_tax_approx
            
            if excess_tax > excess_income:
                relief = excess_tax - excess_income
                return min(relief, surcharge)
        
        return 0.0
    
    def compare_regimes(self, income: float, deduction_80c: float = 0.0,
                       deduction_80d: float = 0.0) -> Dict:
        """Compare both tax regimes and suggest which is better.
        
        Args:
            income: Annual income in INR
            deduction_80c: 80C deduction amount (for old regime)
            deduction_80d: 80D deduction amount (for old regime)
            
        Returns:
            Dictionary with comparison results:
            - new_regime_tax: Tax under new regime
            - old_regime_tax: Tax under old regime
            - recommended_regime: Which regime is better
            - savings: Amount saved by choosing recommended regime
        """
        new_regime_result = self.calculate_tax(income, "new_regime")
        old_regime_result = self.calculate_tax(income, "old_regime", 
                                               deduction_80c, deduction_80d)
        
        new_tax = new_regime_result["final_tax"]
        old_tax = old_regime_result["final_tax"]
        
        if new_tax < old_tax:
            recommended = "new_regime"
            savings = old_tax - new_tax
        elif old_tax < new_tax:
            recommended = "old_regime"
            savings = new_tax - old_tax
        else:
            recommended = "equal"
            savings = 0.0
        
        return {
            "new_regime_tax": new_tax,
            "old_regime_tax": old_tax,
            "recommended_regime": recommended,
            "savings": savings,
            "new_regime_details": new_regime_result,
            "old_regime_details": old_regime_result
        }
    
    def get_tax_breakdown(self, income: float, regime: str = "new_regime",
                         deduction_80c: float = 0.0, deduction_80d: float = 0.0) -> str:
        """Generate formatted tax breakdown report.
        
        Args:
            income: Annual income in INR
            regime: Tax regime ("new_regime" or "old_regime")
            deduction_80c: 80C deduction (old regime only)
            deduction_80d: 80D deduction (old regime only)
            
        Returns:
            Formatted string with tax breakdown
        """
        result = self.calculate_tax(income, regime, deduction_80c, deduction_80d)
        
        report = []
        report.append("=" * 50)
        report.append("INCOME TAX CALCULATION")
        report.append("=" * 50)
        report.append("")
        report.append(f"Regime: {result['regime_used'].upper().replace('_', ' ')}")
        report.append(f"Annual Income: {format_inr(income)}")
        report.append("")
        
        # Deductions
        report.append("Deductions:")
        report.append(f"  Standard Deduction: {format_inr(self.STANDARD_DEDUCTION)}")
        
        if regime == "old_regime":
            if deduction_80c > 0:
                report.append(f"  80C Deduction: {format_inr(deduction_80c)}")
            if deduction_80d > 0:
                report.append(f"  80D Deduction: {format_inr(deduction_80d)}")
        
        report.append("")
        report.append(f"Taxable Income: {format_inr(result['taxable_income'])}")
        report.append(f"Tax (before rebate): {format_inr(result['tax_before_rebate'])}")
        
        if result['rebate_87a'] > 0:
            report.append(f"Rebate u/s 87A: {format_inr(result['rebate_87a'])}")
        
        report.append("-" * 30)
        report.append(f"Final Tax Payable: {format_inr(result['final_tax'])}")
        report.append(f"Effective Tax Rate: {result['effective_rate']:.2f}%")
        report.append("=" * 50)
        
        return "\n".join(report)
