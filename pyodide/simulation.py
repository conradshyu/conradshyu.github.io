"""A small, dimensionless 2D ideal-gas simulation for Pyodide."""

import json
import math
import random


class GasSimulation:
    """Non-interacting point particles in a rectangular, reflecting container."""

    def __init__(self, particle_count, temperature, width=10.0, height=7.5, seed=None):
        if not isinstance(particle_count, int) or particle_count < 1:
            raise ValueError("particle_count must be a positive integer")
        if not math.isfinite(temperature) or temperature <= 0:
            raise ValueError("temperature must be a positive finite number")
        if not math.isfinite(width) or width <= 0:
            raise ValueError("width must be a positive finite number")
        if not math.isfinite(height) or height <= 0:
            raise ValueError("height must be a positive finite number")

        self.width = float(width)
        self.height = float(height)
        self.random = random.Random(seed)
        speed_sigma = math.sqrt(temperature)
        self.particles = [
            [
                self.random.uniform(0, self.width),
                self.random.uniform(0, self.height),
                self.random.gauss(0, speed_sigma),
                self.random.gauss(0, speed_sigma),
            ]
            for _ in range(particle_count)
        ]

    def step(self, dt):
        """Advance positions and reflect particles elastically from the walls."""
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("dt must be a non-negative finite number")

        for particle in self.particles:
            particle[0], particle[2] = self._reflect(
                particle[0], particle[2], dt, self.width
            )
            particle[1], particle[3] = self._reflect(
                particle[1], particle[3], dt, self.height
            )

    @staticmethod
    def _reflect(position, velocity, dt, limit):
        position += velocity * dt
        while position < 0 or position > limit:
            if position < 0:
                position = -position
                velocity = -velocity
            elif position > limit:
                position = 2 * limit - position
                velocity = -velocity
        return position, velocity

    def temperature(self):
        """Return k_B=1 temperature from the mean kinetic energy per degree."""
        speed_squared = sum(
            particle[2] ** 2 + particle[3] ** 2 for particle in self.particles
        )
        return speed_squared / (2 * len(self.particles))

    def pressure(self):
        """Return the 2D ideal-gas pressure estimate, P = N T / area."""
        return len(self.particles) * self.temperature() / (self.width * self.height)

    def state(self):
        return {
            "width": self.width,
            "height": self.height,
            "particles": self.particles,
            "count": len(self.particles),
            "temperature": self.temperature(),
            "pressure": self.pressure(),
            "energy": sum(
                (particle[2] ** 2 + particle[3] ** 2) / 2
                for particle in self.particles
            ),
        }


_simulation = None


def initialize(particle_count, temperature, seed=None):
    global _simulation
    _simulation = GasSimulation(
        int(particle_count),
        float(temperature),
        seed=int(seed) if seed is not None else None,
    )


def advance(dt):
    if _simulation is None:
        raise RuntimeError("Call initialize before advance")
    _simulation.step(dt)


def state_json():
    if _simulation is None:
        raise RuntimeError("Call initialize before state_json")
    return json.dumps(_simulation.state())
