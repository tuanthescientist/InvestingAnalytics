import unittest
import pandas as pd
from src.analysis import calculate_returns, calculate_volatility

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        # Create dummy data
        self.prices = pd.DataFrame({
            'Asset_A': [100, 102, 104, 103, 105],
            'Asset_B': [50, 51, 52, 51, 53]
        })

    def test_calculate_returns(self):
        returns = calculate_returns(self.prices)
        self.assertEqual(len(returns), 4) # Should lose one row
        self.assertAlmostEqual(returns.iloc[0]['Asset_A'], 0.02)

    def test_calculate_volatility(self):
        returns = calculate_returns(self.prices)
        vol = calculate_volatility(returns, annualized=True)
        self.assertTrue(isinstance(vol, pd.Series))
        self.assertEqual(len(vol), 2)

if __name__ == '__main__':
    unittest.main()
