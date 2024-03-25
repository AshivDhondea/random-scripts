import matplotlib.pyplot as plt
import numpy as np

num_segments = 180
radius = 10.


def _make_line(start_point: np.ndarray, end_point: np.ndarray, num_points: int) -> np.ndarray:
    x_coordinates = np.linspace(start_point[0], end_point[1], num=num_points, endpoint=True)
    y_coordinates = np.linspace(start_point[1], end_point[1], num=num_points, endpoint=True)
    return np.array([x_coordinates, y_coordinates])


def _polar_to_cartesian(polar_coordinates: np.ndarray) -> np.ndarray:
    rho = polar_coordinates[0, :]
    phi = polar_coordinates[1, :]
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return np.array([x, y])


def _cartesian_to_polar(cartesian_coordinates: np.ndarray) -> np.ndarray:
    rho = np.linalg.norm(cartesian_coordinates, axis=0)
    phi = np.arctan2(cartesian_coordinates[1, :], cartesian_coordinates[0, :])
    return np.array([rho, phi])


def _create_angles(start: float, end: float, increment: float):
    angles = np.arange(start, end, increment)
    return angles


endpoint_angles_deg = _create_angles(0., 180., 4.)
endpoint_angles_rad = np.radians(endpoint_angles_deg)
endpoint_polar_coordinates = np.array([radius * np.ones_like(endpoint_angles_deg), endpoint_angles_rad])
endpoint_cartesian_coordinates = _polar_to_cartesian(endpoint_polar_coordinates)

plt.scatter(endpoint_cartesian_coordinates[0, :], endpoint_cartesian_coordinates[1, :])
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.show()
