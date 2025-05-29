import unittest
from unittest.mock import patch, MagicMock
from openai_api_benchmark import BenchmarkStats, generate_prompts

class TestBenchmarkStats(unittest.TestCase):
    def test_stats_calculation(self):
        stats = BenchmarkStats()
        stats.add_result(True, 0.1, 0.5)
        stats.add_result(True, 0.2, 0.6)
        stats.add_result(False, 0.0, 0.0)
        
        results = stats.calculate_stats()
        self.assertAlmostEqual(results['avg_ttft'], 0.15, places=7)
        self.assertAlmostEqual(results['avg_completion_time'], 0.55, places=7)

class TestGeneratePrompts(unittest.TestCase):
    def test_generate_prompts(self):
        prompts = generate_prompts(5, 50)
        self.assertEqual(len(prompts), 5)
        self.assertTrue(all(len(p) <= 50 for p in prompts))

if __name__ == '__main__':
    unittest.main()
