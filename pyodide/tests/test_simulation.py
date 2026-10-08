import math
import unittest

from simulation import GasSimulation


class GasSimulationTests(unittest.TestCase):
    def setUp(self):
        self.simulation = GasSimulation(100, 2.0, seed=42)

    def test_seed_makes_initial_state_reproducible(self):
        other = GasSimulation(100, 2.0, seed=42)
        self.assertEqual(self.simulation.particles, other.particles)

    def test_particles_stay_inside_after_large_step(self):
        self.simulation.step(100)
        for x, y, _, _ in self.simulation.particles:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, self.simulation.width)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, self.simulation.height)

    def test_reflecting_walls_conserve_kinetic_energy(self):
        before = self.simulation.state()["energy"]
        self.simulation.step(100)
        after = self.simulation.state()["energy"]
        self.assertAlmostEqual(before, after)

    def test_pressure_obeys_two_dimensional_ideal_gas_law(self):
        state = self.simulation.state()
        self.assertAlmostEqual(
            state["pressure"] * state["width"] * state["height"],
            state["count"] * state["temperature"],
        )

    def test_rejects_invalid_particle_count_and_time_step(self):
        with self.assertRaises(ValueError):
            GasSimulation(0, 1.0)
        with self.assertRaises(ValueError):
            self.simulation.step(math.nan)


if __name__ == "__main__":
    unittest.main()
