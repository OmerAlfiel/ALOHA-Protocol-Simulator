"""
Channel model for ALOHA simulation.
"""
from config import FRAME_TIME

class Channel:
    """Represents the shared communication channel."""
    def __init__(self):
        self.transmissions = []
        self.stats = {'success': 0, 'collision': 0}
    
    def add_transmission(self, node_id):
        """Add a node's transmission to the channel."""
        self.transmissions.append(node_id)
    
    def resolve(self):
        """Resolve current transmissions and detect collisions."""
        # If no transmissions, return no success, no collision
        if not self.transmissions:
            return False, None, False, []
        
        # Single transmission = success
        if len(self.transmissions) == 1:
            successful_node = self.transmissions[0]
            self.stats['success'] += 1
            self.transmissions = []  # Clear channel
            return True, successful_node, False, []
        
        # Multiple transmissions = collision
        else:
            collided_nodes = self.transmissions.copy()
            self.stats['collision'] += 1
            self.transmissions = []  # Clear channel
            return False, None, True, collided_nodes
