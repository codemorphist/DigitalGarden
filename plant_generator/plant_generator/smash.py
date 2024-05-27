from .genom import AgentGenom, PlantGenom
from random import randint, uniform
from enum import Enum


class SmashMethod(Enum):
    Probabilistic = "probalistic"
    WeightedAverage = "weighted average"

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


class SmashGenom:
    """
    Class which implements smash for genomes of plants

    - Probabilistic
    - Weighted Average
    - Mass Smash
    """

    @staticmethod
    def mutate(genom: PlantGenom,
               mutations: int) -> PlantGenom:
        """
        Mutate genom
        """
        genom_table = genom.table()

        mut_table = PlantGenom.random().table()
        while mutations:
            c = randint(0, len(genom_table) - 1)
            r = randint(0, len(genom_table[0]) - 1)
            genom_table[c][r] = mut_table[c][r]
            mutations -= 1

        return PlantGenom([AgentGenom(*agent) for agent in genom_table])

    @staticmethod
    def probabilistic(genom1: PlantGenom,
                      genom2: PlantGenom,
                      probability: float,
                      mutations: int) -> PlantGenom:
        """
        A probabilistic method of smashing two plant genomes

        Algorithm:
        1.  We go through each gene in the table
        2.  We randomly generate a number from 0 to 100
        4.  If it is greater than the Probability, we take the gene for the Descendant from Genome2,
            otherwise from Genome1
        5.  At the end, we randomly select a cell from the Descendant genome
            and write a randomly generated number into it
        6.  We repeat [5] as many times as there are mutations

        :param genom1: First parent genom
        :param genom2: Second parent genom
        :param probability: Probability for smash
        :param mutations: Mutations count
        :return: smashed_genome
        """
        # Probabilistic part
        genom1_table = genom1.table()
        genom2_table = genom2.table()
        smashed_table = PlantGenom.empty().table()
        for c, agent in enumerate(smashed_table):
            for r in range(len(agent)):
                if uniform(0.0, 1.0) > probability:
                    smashed_table[c][r] = genom2_table[c][r]
                else:
                    smashed_table[c][r] = genom1_table[c][r]

        smashed_genom = PlantGenom([AgentGenom(*agent) for agent in smashed_table])
        return SmashGenom.mutate(smashed_genom, mutations)

    @staticmethod
    def average(genom1: PlantGenom,
                genom2: PlantGenom,
                weight: float,
                mutations: int) -> PlantGenom:
        """
        Method of weighted average smashing of two plant genomes

        Algorithm:
        1.  We go through each gene in the table
        2.  For Descendant, we put a gene,
            the value of which is calculated as follows:
            `Weight * Genome1 + (1 - weight) * Genome22`

        :param genom1: First parent genom
        :param genom2: Second parent genom
        :param weight: Weight for average
        :param mutations: Mutations count
        :return: smashed genome
        """
        # Averaging part
        assert 0 <= weight <= 1, "The weight must be a float the interval [0;1]"
        genom1_table = genom1.table()
        genom2_table = genom2.table()
        smashed_table = PlantGenom.empty().table()

        for c, agent in enumerate(smashed_table):
            for r in range(len(agent)):
                g1 = genom1_table[c][r]
                g2 = genom2_table[c][r]
                smashed_table[c][r] = int(weight * g1 + (1 - weight) * g2)

        smashed_genom = PlantGenom([AgentGenom(*agent) for agent in smashed_table])
        return SmashGenom.mutate(smashed_genom, mutations)

    @staticmethod
    def get_smash(method: SmashMethod):
        """
        Get smash method by method type
        :return: smash method
        """
        match method:
            case SmashMethod.Probabilistic:
                return SmashGenom.probabilistic
            case SmashMethod.WeightedAverage:
                return SmashGenom.average
            case _:
                raise TypeError(f"Invalid method: {repr(method)}")

    @staticmethod
    def mass_smash(plants: list[PlantGenom], method: SmashMethod, *args, **kwargs) -> PlantGenom:
        """
        Smash many plant for one time

        :param plants: list of plants to smash
        :param method_name: way (method) to smash plants
        :param *args: other args for way ???
        :param mutations: the number of mutations
        :return: smashed genome
        """
        if not plants:
            return PlantGenom.empty()

        smash = SmashGenom.get_smash(method)
        
        smashed_genome = plants[0]
        for plant_genome in plants[1:]:
            smashed_genome = smash(smashed_genome, plant_genome, *args, **kwargs)

        return smashed_genome


