from typing import List
import math
import numpy as np
import plotly.graph_objects as go


def interval_pi_estimate(num_samples: int, intervals: List[int]) -> np.ndarray:
    sample_coordinates = np.random.uniform(0., 1., [2, num_samples])
    distance = np.linalg.norm(sample_coordinates, axis=0)

    pi_estimate = np.zeros(np.shape(intervals), dtype=np.float64)
    for index, value in enumerate(intervals):
        inside_quadrant = np.where(distance[0:value] < 1.)
        inside_count = np.shape(inside_quadrant)[1]
        pi_estimate[index] = 4 * inside_count / value
    return pi_estimate


if __name__ == '__main__':
    intervals_list = [20000, 40000, 60000, 80000, 100000]
    estimated_pi = interval_pi_estimate(100000, intervals_list)

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=intervals_list, y=estimated_pi,
                             mode='markers', name='markers'))
    fig.add_hline(y=math.pi, line_color='red')
    fig.show()
