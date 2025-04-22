class Power:
    """
    Base class for powers
    """

    def __init__(self):
        self.name = None
        self.available = False
        self.description = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Power(name={self.name}, available={self.available})"

    def is_available(self) -> bool:
        return self.available

    def consume(self):
        """
        Consume the power, making it unavailable for future use.
        Dummy method - implemented in child classes
        """
        pass
