from .main import algorithm  # Import the main method
from .betweenness_reduction import * # import subparts if needed
from .helper_functions import *

# Essentially exposes everything that doesn't start with "_", since "_"
# is used to denote private methods which should not be exposed.
__all__ = [name for name in dir() if not name.startswith("_")]