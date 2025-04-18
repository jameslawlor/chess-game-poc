class Power():
    """
    Base class for powers
    """
    def __init__(self):
        self.name = None
        self.available = False
        self.description = None
        self.icon = None
        self.icon_path = None
        self.available = True

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Power(name={self.name}, available={self.available})"
    
    def is_available(self) -> bool:
        return self.available

    def activate(self):
        """
        Activate the power, making it unavailable for future use.
        Dummy method - implemented in child classes
        """
        pass



class RookTeleportPower(Power):
    """
    Allows the player to teleport a rook to any empty square.
    """
    def __init__(self):
        super().__init__()
        self.name = "Rook Teleport"
        self.description = "Teleport a rook to any empty square."

    def activate(self):
        """
        Activate the Rook Teleport power.
        """
        # Logic to teleport a rook goes here
        print(f"{self.name} activated! You can teleport a rook.")
        self.available = False
        # Logic to consume the power goes here


class DoubleMovePower(Power):
    """
    Allows the player to move twice in one turn.
    """
    def __init__(self):
        super().__init__()
        self.name = "Double Move"
        self.description = "Take two turns in a row."

    def activate(self):
        """
        Activate the Double Move power.
        """
        # Logic to teleport a rook goes here
        print(f"{self.name} activated! You can now move twice.")
        self.available = False
        # Logic to consume the power goes here