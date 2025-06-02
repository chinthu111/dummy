from dataclasses import dataclass
from utils import get_env, get_env_float

ENV_TRAJECTORY_FILE = "TRAJECTORY_FILE"
ENV_WRITE_PERIOD = "WRITE_PERIOD"

DEFAULT_TRAJECTORY_FILE = "trajectory.csv"
DEFAULT_WRITE_PERIOD = 1.0

@dataclass
class ServiceEnv:
    trajectory_file: str
    write_period: float

    @classmethod
    def read(cls):
        return cls(
            trajectory_file=get_env(ENV_TRAJECTORY_FILE, DEFAULT_TRAJECTORY_FILE),
            write_period=get_env_float(ENV_WRITE_PERIOD, DEFAULT_WRITE_PERIOD)
        )
