"""Module with a brute force TSP solver"""

from itertools import permutations
from typing import List, Tuple

import numpy as np


def solve_tsp_brute_force(
    distance_matrix: np.ndarray, open_tsp: bool = False
) -> Tuple[List, float]:
    """Solve TSP to optimality with a brute force approach

    Parameters
    ----------
    distance_matrix
        Distance matrix of shape (n x n) with the (i, j) entry indicating the
        distance from node i to j. It does not need to be symmetric

    open_tsp
        True for an open problem (the traveler does not return to the origin).
        In that case, the first column of the `distance_matrix` is zeroed.

    Returns
    -------
    permutation
        A permutation of nodes from 0 to n (with another 0 in case of a closed
        problem) that produces the least total distance

    distance
        The total distance the optimal permutation produces

    Notes
    ----
    The algorithm checks all permutations and returns the one with smallest
    distance. In principle, the total number of possibilities would be n! for
    n nodes. However, we can fix node 0 and permutate only the remaining,
    reducing the possibilities to (n - 1)!.
    """

    # Get all points from 1 to n (fix 0 as mentioned in the notes)
    points = range(1, distance_matrix.shape[0])
    if open_tsp:
        # Copy the matrix to prevent messing with external data
        distance_matrix = distance_matrix.copy()
        distance_matrix[:, 0] = 0

    best_distance = np.inf
    best_solution = None
    for permutation in permutations(points):
        distance = _permutation_distance(permutation, distance_matrix)
        if distance < best_distance:
            best_distance = distance
            best_solution = permutation

    # Insert node 0 at the beginning, and also at the end of not an open
    # problem
    best_solution = [0] + list(best_solution)
    if not open_tsp:
        best_solution.append(0)

    return best_solution, best_distance


def _permutation_distance(permutation, distance_matrix):
    """Compute distance of a given permutation"""
    permutation = list(permutation)
    ind1 = [0] + permutation
    ind2 = permutation + [0]
    return distance_matrix[ind1, ind2].sum()