from dataclasses import dataclass

@dataclass
class TrajectoryPoint:
    latitude: float
    longitude: float
    altitude: float

class Trajectory:
    points: list

    def __init__(self, points=None):
        self.points = points if points else []

    @classmethod
    def load(cls, filename):
        traj = cls()
        try:
            with open(filename, "rt") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 3:
                        continue
                    lat, lon, alt = map(float, parts)
                    traj.points.append(TrajectoryPoint(lat, lon, alt))
            return traj, None
        except Exception as ex:
            return None, f"Failed to read trajectory: {ex}"

    def __len__(self):
        return len(self.points)

    def __getitem__(self, idx):
        return self.points[idx]
