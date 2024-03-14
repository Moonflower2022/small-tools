import numpy as np
from scipy.spatial.distance import cdist

# implementation of boids with:
# separation
# alignment
# cohesion

class Boids():
    def __init__(self, width, height, deterence_border, deterence_force, num, separation_radius, alignment_raduis, cohesion_radius, starting_velo_range, max_velo, separation_weight=1, alignment_weight=0.125, cohesion_weight=0.01, attraction_weight=0.01, seed=None):


        self.width = width
        self.height = height
        if seed:
            np.random.seed(seed)
        self.boid_positions = np.column_stack((np.random.uniform(0, width, num), np.random.uniform(0, height, num)))
        self.boid_velocities = np.column_stack((np.random.uniform(-starting_velo_range, starting_velo_range, num), np.random.uniform(-starting_velo_range, starting_velo_range, num)))
        self.separation_radius = separation_radius
        self.alignment_raduis = alignment_raduis
        self.cohesion_radius = cohesion_radius
        self.deterence_border = deterence_border
        self.deterence_force = deterence_force
        self.num = num

        self.max_velo = max_velo

        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight
        self.attraction_weight = attraction_weight

    def update_velocities(self, attraction_point):
        distances = cdist(self.boid_positions, self.boid_positions)
        
        flock_mate_positions = [self.boid_positions[mesh] for mesh in np.logical_and(distances < self.separation_radius, distances != 0)]
        self.separation_vectors = np.array([np.sum(self.boid_positions[i] - positions, axis=0) for i, positions in enumerate(flock_mate_positions)]) * self.separation_weight
        #separation_vectors = np.array([centroid - self.boid_positions[i] for i, centroid in enumerate(centroids)])

        percieved_velocities = np.array([np.sum(self.boid_velocities[mesh], axis=0) for mesh in 
                                         np.logical_and(distances < self.alignment_raduis, 
                                         distances != 0
                                                        )
                                                        ]) 
        self.alignment_vectors = (percieved_velocities / (self.num - 1) - self.boid_velocities) * self.alignment_weight

        all_positions = [self.boid_positions[mesh] for mesh in np.logical_and(distances < self.cohesion_radius, distances != 0)]
        flock_mass_center = np.array([self.boid_positions[i] if len(positions) == 0 else np.mean(positions, axis=0) for i, positions in enumerate(all_positions)])
        self.cohesion_vectors = (flock_mass_center - self.boid_positions)*self.cohesion_weight
        
        self.border_vectors = np.zeros((self.num, 2))
        self.border_vectors[:, 0] = np.where(self.boid_positions[:, 0] > self.width - self.deterence_border, -self.deterence_force, self.border_vectors[:, 0])
        self.border_vectors[:, 0] = np.where(self.boid_positions[:, 0] < self.deterence_border, self.deterence_force, self.border_vectors[:, 0])
        self.border_vectors[:, 1] = np.where(self.boid_positions[:, 1] > self.height - self.deterence_border, -self.deterence_force, self.border_vectors[:, 1])
        self.border_vectors[:, 1] = np.where(self.boid_positions[:, 1] < self.deterence_border, self.deterence_force, self.border_vectors[:, 1])

        self.attraction_vectors = np.zeros((self.num, 2)) if type(attraction_point) == type(None) else (np.array(attraction_point) - self.boid_positions) * self.attraction_weight

        self.boid_velocities += self.border_vectors + self.cohesion_vectors + self.alignment_vectors + self.separation_vectors + self.attraction_vectors

        

    def update_positions(self, dt):
        self.boid_velocities = np.clip(self.boid_velocities, -self.max_velo, self.max_velo)
        self.boid_positions += self.boid_velocities * dt
