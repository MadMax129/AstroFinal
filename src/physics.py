from vector import Vector2D
from planet import Planet
import numpy as np

G = 6.6743015 * 10**-11

class PhysicsEngine:
    def __init__(self, objects_list: list[Planet]):
        self.objects_list = objects_list
        self.N = len(objects_list)

        self.positions = np.zeros((self.N, 2))
        self.masses = np.zeros(self.N)
        self.velocities = np.zeros((self.N, 2))
        self.accelerations = np.zeros((self.N, 2))
        self.displacements = np.zeros((self.N, self.N, 2))
        self.dist_squared = np.zeros((self.N, self.N))
        self.inv_dist_cubed = np.zeros((self.N, self.N))
        self.accel_contributions = np.zeros((self.N, self.N, 2))

    def update_objects(self, TIME_DELTA):
        # Update positions, masses, velocities from objects_list
        for i, obj in enumerate(self.objects_list):
            self.positions[i, :] = obj.position.vector
            self.masses[i] = obj.mass
            self.velocities[i, :] = obj.velocity.vector

        # Compute pairwise displacement vectors (r_j - r_i)
        np.subtract(self.positions[np.newaxis, :, :], self.positions[:, np.newaxis, :], out=self.displacements)

        # Compute squared distances
        np.einsum('ijk,ijk->ij', self.displacements, self.displacements, out=self.dist_squared)
        # or could just do
        # np.sum(self.displacements ** 2, axis=2, out=self.dist_squared)

        # Avoid division by zero by setting the diagonal to infinity
        np.fill_diagonal(self.dist_squared, np.inf)

        # Compute inverse distances cubed
        np.power(self.dist_squared, -1.5, out=self.inv_dist_cubed, where=self.dist_squared != np.inf)

        # Compute gravitational acceleration contributions
        # G * m_j * (r_j - r_i) / |r_j - r_i|^3
        masses_j = self.masses[np.newaxis, :, np.newaxis]
        np.multiply(self.displacements, self.inv_dist_cubed[:, :, np.newaxis], out=self.accel_contributions)
        self.accel_contributions *= G
        self.accel_contributions *= masses_j

        # Sum over all j to get the total acceleration on each object i
        np.sum(self.accel_contributions, axis=1, out=self.accelerations)

        # Semi-implicit Euler integration
        self.velocities += TIME_DELTA * self.accelerations
        self.positions += TIME_DELTA * self.velocities

        # Update the objects with new velocities and positions
        for i, obj in enumerate(self.objects_list):
            obj.velocity.vector[:] = self.velocities[i, :]
            obj.position.vector[:] = self.positions[i, :]
