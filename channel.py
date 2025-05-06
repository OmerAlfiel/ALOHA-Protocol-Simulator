# channel.py
"""
Channel model for ALOHA simulation.
"""
class Channel:
    def __init__(self):
        self.transmissions = []
        self.total_attempts = 0
        self.successful_transmissions = 0
        self.collisions = 0

    def reset(self):
        self.transmissions.clear()

    def add_transmission(self, node_id):
        self.transmissions.append(node_id)
        self.total_attempts += 1

    def resolve(self):
        if len(self.transmissions) == 1:
            success = True
            winner = self.transmissions[0]
            self.successful_transmissions += 1
        else:
            success = False
            winner = None
            if len(self.transmissions) > 1:
                self.collisions += 1
        
        collided = len(self.transmissions) > 1
        nodes_involved = self.transmissions.copy()
        self.reset()
        return success, winner, collided, nodes_involved

    def get_statistics(self):
        return {
            "total_attempts": self.total_attempts,
            "successful": self.successful_transmissions,
            "collisions": self.collisions,
            "efficiency": self.successful_transmissions / self.total_attempts if self.total_attempts > 0 else 0
        }