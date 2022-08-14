from enum import Enum
from typing import List

import numpy as np

from src.grlib.trajectory.general_direction_trajectory import GeneralDirectionTrajectory


class Direction(Enum):
    UP = 1
    RIGHT = UP
    INTO = UP
    STATIONARY = 0
    DOWN = -1
    LEFT = DOWN
    AWAY = DOWN


class GeneralDirectionBuilder:
    """
    Composes a trajectory as a sequence of Direction enum(1/0/-1) on multiple axi.
    Inspired by https://ieeexplore-ieee-org.tudelft.idm.oclc.org/stamp/stamp.jsp?tp=&arnumber=485888
    """
    def __init__(self, zero_precision=0.1):
        """

        :param zero_precision: how much is considered "no movement on the axis"
        """
        self.dimensions = 3
        self.zero_precision = zero_precision

    def make_trajectory(self, landmark_sequence) -> GeneralDirectionTrajectory:
        """
        Creates the trajectory
        :param landmark_sequence: a sequence of landmarks from (sample) frames
        :return: the trajectory encoding as an array
        """
        trajectory = [[] * self.dimensions]
        last = self.hand_center(landmark_sequence[0])
        for landmark in landmark_sequence[1:]:
            for i in range(self.dimensions):
                current = self.hand_center(landmark)
                lower_boundary = last[i] - self.zero_precision
                upper_boundary = last[i] + self.zero_precision
                if lower_boundary > current[i]:
                    trajectory[i].append(Direction.DOWN)
                elif upper_boundary < current[i]:
                    trajectory[i].append(Direction.UP)
                else:
                    trajectory[i].append(Direction.STATIONARY)
        return GeneralDirectionBuilder.object_from_lists(trajectory)

    @staticmethod
    def object_from_lists(trajectory_list) -> GeneralDirectionTrajectory:
        return GeneralDirectionTrajectory(
            len(trajectory_list[0]),
            np.array(trajectory_list[0]),
            np.array(trajectory_list[1]),
            np.array(trajectory_list[2])
        )

    def hand_center(self, hand_landmarks):
        return hand_landmarks[0]
