from plant_generator import PlantGenom, SmashMethod, SmashGenom


class MethodConfig:
    """
    Class implement finite state machine for smash method frame
    """
    METHODS = [method.value.title() for method in SmashMethod]

    def __init__(self):
        self._method = SmashMethod.Probabilistic
        self._proportion = 0.5
        self._mutations = 0

    @property
    def method(self):
        return self._method
    @method.setter
    def method(self, value):
        value = SmashMethod(value)
        if value is None:
            return
        self._method = value 

    @property
    def method_name(self) -> str:
        return self.method.value.title()

    @property
    def proportion(self):
        return int(self._proportion * 100)
    @proportion.setter
    def proportion(self, value):
        self._proportion = value/100

    @property
    def mutations(self):
        """The mutations property."""
        return self._mutations
    @mutations.setter
    def mutations(self, value):
        self._mutations = value

    def smash(self, plant1: PlantGenom, plant2: PlantGenom) -> PlantGenom:
        smash = SmashGenom.get_smash(self.method)
        return smash(plant1, plant2, self.proportion/100, self.mutations)
