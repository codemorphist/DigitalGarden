from .genom import AgentGenom, PlantGenom
from enum import Enum, auto
from random import randint


class SmashType(Enum):
    Probalistic = auto()    
    WeightedAverage = auto()


class SmashGenom:
    """
    Class which implement smash for genom of plants
    
    - Probalistic 
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
            c = randint(0, len(genom_table))
            r = randint(0, len(genom_table[0]))
            genom_table[c][r] = mut_table[c][r]
            mutations -= 1

        return PlantGenom([AgentGenom(*agent) for agent in genom_table])

    @staticmethod
    def probalistic(genom1: PlantGenom, 
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
        :param probability: Probalility for smash
        :param mutations: Mutations count
        :return: smashed_genome
        """
        # Probalistic part
        genom1_table = genom1.table()
        genom2_table = genom2.table()
        smashed_table = PlantGenom.empty().table()
        for c, agent in enumerate(smashed_table):
            for r in range(len(agent)):
                if randint(0, 100)/100 > probability:
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
            `Weight * Genome1 + (1 - weight) * Genome2`

        :param genom1: First parent genom 
        :param genom2: Second parent genom 
        :param weight: Weight for average
        :param mutations: Mutations count
        :return: smashed genome
        """
        # Averate part
        assert weight > 0, "Weight must be greater than zero"
        genom1_table = genom1.table()
        genom2_table = genom2.table()
        smashed_table = PlantGenom.empty().table()

        for c, agent in enumerate(smashed_table):
            for r in range(len(agent)):
                g1 = genom1_table[c][r]
                g2 = genom2_table[c][r]
                smashed_table[c][r] = int( weight * g1 + (1 - weight) * g2 )

        smashed_genom = PlantGenom([AgentGenom(*agent) for agent in smashed_table])
        return SmashGenom.mutate(smashed_genom, mutations)

    @staticmethod
    def mass_smash(plants: list[PlantGenom], way: SmashType, *args) -> PlantGenom:
        """
        Smash many plant for one time 

        :param plants: list of plants to smash
        :param way: way (method) to smash plants
        :param *args: other args for way
        :return: smashed genom
        """
        if not plants:
            return PlantGenom.empty()
        
        smash = None
        match way:
            case SmashType.Probalistic:
                smash = SmashGenom.probalistic
            case SmashType.WeightedAverage:
                smash = SmashGenom.average

        smashed_genome = plants[0]
        for plant_genome in plants[1:]:
            smashed_genome = smash(smashed_genome, plant_genome, *args)

        return smashed_genome

