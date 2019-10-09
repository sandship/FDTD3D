import numpy as np

class Boundary(object):
    def __init__(self, InitialzedParameter):
        return None

class PmlBoundary(Boundary):
    def __init__(self, InitialzedParameter):
        super().__init__(InitialzedParameter)
        return None
    
class PeriodicBoundary(Boundary):
    def __init__(self, InitialzedParameter):
        super().__init__(InitialzedParameter)
        return None
