import unittest
from discount_engine.allocator import allocate_discounts

class DiscountAllocationTests(unittest.TestCase):

    def test_typical_distribution(self):
        # Sample agents with varying metrics
        sample_agents = [
            {"id": "X1", "performanceScore": 95, "seniorityMonths": 24, "targetAchievedPercent": 90, "activeClients": 15},
            {"id": "X2", "performanceScore": 60, "seniorityMonths": 12, "targetAchievedPercent": 50, "activeClients": 5},
            {"id": "X3", "performanceScore": 80, "seniorityMonths": 6,  "targetAchievedPercent": 70, "activeClients": 10}
        ]

        # Run allocation
        response = allocate_discounts(10000, sample_agents, {})

        # Extract results
        assigned = {agent['id']: agent['assignedDiscount'] for agent in response['allocations']}

        # Validate total distribution and relative shares
        self.assertEqual(sum(assigned.values()), 10000)
        self.assertGreater(assigned["X1"], assigned["X2"])
        self.assertGreater(assigned["X1"], assigned["X3"])

    def test_equal_metric_agents(self):
        uniform_agents = [
            {"id": f"Y{i}", "performanceScore": 50, "seniorityMonths": 10,
             "targetAchievedPercent": 50, "activeClients": 5}
            for i in range(3)
        ]

        # Allocate kitty
        response = allocate_discounts(999, uniform_agents, {})
        allocations = [agent['assignedDiscount'] for agent in response['allocations']]

        # Check fairness and rounding consistency
        self.assertLessEqual(max(allocations) - min(allocations), 1)
        self.assertTrue(998 <= sum(allocations) <= 999)

    def test_edge_case_minimum_threshold(self):
        # Extremely small allocation with rounding and minimum threshold
        low_agents = [
            {"id": "Z1", "performanceScore": 1, "seniorityMonths": 1, "targetAchievedPercent": 1, "activeClients": 1},
            {"id": "Z2", "performanceScore": 0, "seniorityMonths": 0, "targetAchievedPercent": 0, "activeClients": 0}
        ]

        # Provide config with min allocation percent
        result = allocate_discounts(5, low_agents, {"min_allocation_percent": 0.2})
        assigned = {agent['id']: agent['assignedDiscount'] for agent in result['allocations']}

        # Assert thresholds and full allocation usage
        self.assertGreaterEqual(assigned["Z1"], 1)
        self.assertGreaterEqual(assigned["Z2"], 1)
        self.assertEqual(sum(assigned.values()), 5)

if __name__ == '__main__':
    unittest.main()
