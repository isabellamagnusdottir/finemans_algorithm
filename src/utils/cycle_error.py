class NegativeCycleError(Exception):
    """Exception raised upon discovering a negatice cycle.
    """
    def __init__(self, message="A negative cycle was found!"):
        self.message = message
        super().__init__(self.message)
