import random

import numpy as np
from typing import Tuple
from gym.envs.registration import register

from highway_env_v2 import utils
from highway_env_v2.envs.common.abstract import AbstractEnv
from highway_env_v2.envs.common.action import Action
from highway_env_v2.road.road import Road, RoadNetwork
from highway_env_v2.vehicle.controller import ControlledVehicle, ManualVehicle


class HighwayEnv(AbstractEnv):
    """
    A highway driving environment.

    The vehicle is driving on a straight highway with several lanes, and is rewarded for reaching a high speed,
    staying on the rightmost lanes and avoiding collisions.
    """

    RIGHT_LANE_REWARD: float = 0.1
    """The reward received when driving on the right-most lanes, linearly mapped to zero for other lanes."""

    HIGH_SPEED_REWARD: float = 0.4
    """The reward received when driving at full speed, linearly mapped to zero for lower speeds according to config["reward_speed_range"]."""

    LANE_CHANGE_REWARD: float = 0
    """The reward received at each lane change action."""

    def default_config(self) -> dict:
        config = super().default_config()
        config.update({
            "observation": {
                "type": "Kinematics"
            },
            "action": {
                "type": "DiscreteMetaAction",
            },
            "lanes_count": 4,
            "vehicles_count": 50,
            "controlled_vehicles": 1,
            "initial_lane_id": None,
            "duration": 40,  # [s]
            "ego_spacing": 2,
            "vehicles_density": 1,
            "collision_reward": -1,  # The reward received when colliding with a vehicle.
            "reward_speed_range": [20, 30],
            "offroad_terminal": False,
            "ego_position": None,
            "ego_heading": None,
            "crash_ends_test": True
        })
        return config

    def _reset(self) -> None:
        self._create_road()
        self._create_vehicles()

    def _create_road(self) -> None:
        """Create a road composed of straight adjacent lanes."""
        self.road = Road(network=RoadNetwork.straight_road_network(self.config["lanes_count"]),
                         np_random=self.np_random, record_history=self.config["show_trajectories"])

    def _create_vehicles(self) -> None:
        """Create some new random vehicles of a given type, and add them on the road."""

        vehicles_type = utils.class_from_path(self.config["other_vehicles_type"])

        self.controlled_vehicles = []
        for j in range(self.config["controlled_vehicles"]):
            if j == 0:
                if self.config["ego_position"] is not None and self.config["ego_heading"] is not None:
                    # Spawn the ego vehicle at a specifc location
                    vehicle = self.action_type.vehicle_class(self.road,
                                                             position=self.config["ego_position"],
                                                             heading=self.config["ego_heading"],
                                                             speed=25)
                else:
                    # Spawn the ego vehicle at a random location
                    vehicle = self.action_type.vehicle_class.create_random(self.road,
                                                                        speed=25,
                                                                        lane_id=self.config["initial_lane_id"],
                                                                        spacing=self.config["ego_spacing"])
                vehicle.color_id = -1
                vehicle.crash_ends_test = self.config["crash_ends_test"]
            else:
                # These are cars used by generated tests
                vehicle = ManualVehicle.create_random(self.road,
                                                      speed=25,
                                                      lane_id=self.config["initial_lane_id"],
                                                      spacing=1)
            self.controlled_vehicles.append(vehicle)
            self.road.vehicles.append(vehicle)

        first_vehicle = True
        # Place vehicles in front of the ego car
        for _ in range(int(self.config["vehicles_count"])):
            if first_vehicle:
                spacing = self.config["ego_spacing"]
                first_vehicle = False
            else:
                spacing = 1
            self.road.vehicles.append(vehicles_type.create_random(self.road, spacing=spacing / self.config["vehicles_density"]))

    def _reward(self, action: Action) -> float:
        """
        The reward is defined to foster driving at high speed, on the rightmost lanes, and to avoid collisions.
        :param action: the last action performed
        :return: the corresponding reward
        """
        neighbours = self.road.network.all_side_lanes(self.vehicle.lane_index)
        lane = self.vehicle.target_lane_index[2] if isinstance(self.vehicle, ControlledVehicle) \
            else self.vehicle.lane_index[2]
        scaled_speed = utils.lmap(self.vehicle.speed, self.config["reward_speed_range"], [0, 1])
        reward = \
            + self.config["collision_reward"] * self.vehicle.crashed \
            + self.RIGHT_LANE_REWARD * lane / max(len(neighbours) - 1, 1) \
            + self.HIGH_SPEED_REWARD * np.clip(scaled_speed, 0, 1)
        reward = utils.lmap(reward,
                          [self.config["collision_reward"], self.HIGH_SPEED_REWARD + self.RIGHT_LANE_REWARD],
                          [0, 1])
        reward = 0 if not self.vehicle.on_road else reward
        return reward

    def _is_terminal(self) -> bool:

        non_crashed_vehicles = []

        # Remove all crashed vehicles
        for v in self.road.vehicles:
            if not v.crashed:
                non_crashed_vehicles.append(v)
        self.road.vehicles = non_crashed_vehicles

        if self.config["crash_ends_test"]:
            """The episode is over if the ego vehicle crashed or the time is out."""
            return self.vehicle.crashed or self.steps >= self.config["duration"] or (self.config["offroad_terminal"] and not self.vehicle.on_road)        
        else:
            return self.steps >= self.config["duration"] or (self.config["offroad_terminal"] and not self.vehicle.on_road)

    def _cost(self, action: int) -> float:
        """The cost signal is the occurrence of collision."""
        return float(self.vehicle.crashed)

    def get_lines_covered(self):
        coverage = self.controlled_vehicles[0].code_coverage
        all_lines = np.arange(len(coverage))
        covered_lines = []
        for i in range(len(coverage)):
            if coverage[i] == 1:
                covered_lines.append(i)
        covered_lines = np.array(covered_lines)
        return covered_lines, all_lines

register(
    id='highway-v0',
    entry_point='highway_env_v2.envs:HighwayEnv',
)
