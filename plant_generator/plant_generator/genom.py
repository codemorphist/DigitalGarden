from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from tools import Color
from random import randint, uniform
from copy import deepcopy


@dataclass
class AgentGenom:
    length: int
    length_deviation: int

    size: int
    size_from_ancestor: int
    size_from_level: int
    size_changes: int

    red: int
    green: int
    blue: int
    red_changes: int
    green_changes: int
    blue_changes: int
    color_from_ancestor: int
    color_deviation: int

    number_branches: int
    angle_branches: int
    angle_deviation: int

    turn: int
    random_turn: int
    down: int

    @staticmethod
    def random() -> AgentGenom:
        r, g, b = Color.random()
        rc, gc, bc = Color.random()

        return AgentGenom(
            length=randint(20, 150),
            length_deviation=randint(0, 30),
            size=randint(5, 80),
            size_from_ancestor=randint(10, 90),
            size_from_level=randint(5, 100),
            size_changes=randint(-30, 30),
            red=r, green=g, blue=b,
            red_changes=rc, green_changes=gc, blue_changes=bc,
            color_deviation=randint(-20, 20),
            color_from_ancestor=randint(0, 80),
            number_branches=randint(1, 3),
            angle_branches=randint(0, 120),
            angle_deviation=randint(10, 30),
            turn=randint(-120, 120),
            random_turn=randint(0, 80),
            down=randint(-30, 30)
        )

    @classmethod
    def attr_list(cls) -> list:
        class_attributes = [attr for attr in AgentGenom.__annotations__]
        return class_attributes

    @staticmethod
    def empty() -> AgentGenom:
        return AgentGenom(*[0 for _ in AgentGenom.attr_list()])

    def __iter__(self):
        for attr in self.attr_list():
            yield attr, getattr(self, attr)


class PlantGenom:
    def __init__(self, genom: list[AgentGenom]):
        self.genom = genom

    def evolve(self,
               generation: int,
               agent_genom: AgentGenom) -> Optional[AgentGenom]:
        """
        Evolute genom of Agent to new generation
        """
        if generation >= len(self.genom):
            return None

        evolved_genom = deepcopy(self.genom[generation])

        size_percent = evolved_genom.size_from_ancestor / 100
        evolved_genom.size = (evolved_genom.size_from_level + evolved_genom.size) / 2
        evolved_genom.size = size_percent * (agent_genom.size + evolved_genom.size)

        len_deviation = agent_genom.length_deviation
        evolved_genom.length += randint(-len_deviation, len_deviation)
        evolved_genom.angle_branches += agent_genom.angle_deviation

        ar = agent_genom.red + evolved_genom.color_deviation
        ag = agent_genom.green + evolved_genom.color_deviation
        ab = agent_genom.blue + evolved_genom.color_deviation

        sr = evolved_genom.red
        sg = evolved_genom.green
        sb = evolved_genom.blue

        acolor = Color(ar, ag, ab)
        scolor = Color(sr, sg, sb)

        r, g, b = ((acolor + scolor) * (evolved_genom.color_from_ancestor / 100)).rgb

        evolved_genom.red = r
        evolved_genom.green = g
        evolved_genom.blue = b

        return evolved_genom

    def __iter__(self):
        """
        Convert genom to dict in next format

        'Agent 1': { ... },
        'Agent 2': { ... },
                     ...
        """
        for i, agent in enumerate(self.genom):
            yield f"Agent{i}", dict(agent)

    @staticmethod
    def random(generations: int = 9) -> PlantGenom:
        return PlantGenom([
            AgentGenom.random() for _ in range(generations)
        ])

    @staticmethod
    def dict_is_genome(entries_dict: dict) -> bool:
        """
        This static method echoes that of the UserFrame class, but is instead
        used for the case when the variables are ordinary strings; that is to say,
        it is a simple check for being capable of being seen as a genome
        """
        try:
            for _, val in entries_dict.items():
                int(val)
            return True
        except:
            return False

    @staticmethod
    def export_genom(genom: PlantGenom) -> str:
        """
        Impoort genom to string

        Output format
                A1  A2  A3  ..
            G1
            G2
            G3
            ..
        """
        transposed = list(zip(*genom.table()))
        agents_str = [" ".join(map(str, map(int, agent))) for agent in transposed]
        return "\n".join(agents_str)

    @staticmethod
    def import_genom(genom: str) -> PlantGenom:
        """
        Export genom from string

        Imput format
                A1  A2  A3  ..
            G1
            G2
            G3
            ..
        """
        values = []
        for row in genom.rstrip().split("\n"):
            val_row = []
            for val in row.rstrip().split():
                val_row.append(int(val))
            values.append(val_row)

        agents = []
        for c in range(len(values[0])):
            gens = []
            for v in range(len(values)):
                gens.append(values[v][c])
            agents.append(AgentGenom(*gens))
        return PlantGenom(agents)

    @staticmethod
    def empty(agents: int = 9) -> PlantGenom:
        genom = []
        for _ in range(agents):
            genom.append(AgentGenom.empty())
        return PlantGenom(genom)

    def table(self) -> list[list]:
        genom_table = []

        for _, agent in self:
            a = []
            for gen in agent.values():
                a.append(gen)
            genom_table.append(a)

        return genom_table

    def __repr__(self) -> str:
        return f"PlantGenom({self.genom})"


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
    def mass_smash(plants: list[PlantGenom], method_name: str, mutations: int) -> PlantGenom:
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

        method = SmashMethod.construct_method(MethodIdentifier(name=method_name, mutations=mutations))

        smashed_genome = plants[0]
        for plant_genome in plants[1:]:
            smashed_genome = method(smashed_genome, plant_genome)

        return smashed_genome


class MethodIdentifier:
    ALLOWED_METHODS = ("Probabilistic", "Weighted Average")

    def __init__(self, name: str = "Probabilistic", proportion: float = 0.5, mutations: int = 0):
        assert name in MethodIdentifier.ALLOWED_METHODS, f"The 'name' argument must be in {MethodIdentifier.ALLOWED_METHODS}"
        assert isinstance(proportion, float) and 0 <= proportion <= 1, "The 'proportion' argument only accepts float values from [0;1]"
        assert isinstance(mutations, int) and 0 <= mutations <= 180, "The 'mutations' argument only accepts integer values from [0;180]"
        self.dictionary = {"Name": name, "Proportion": proportion, "Mutations": mutations}

    def __getitem__(self, key):
        return self.dictionary[key]

    def __setitem__(self, key, value):
        assert key in self.dictionary.keys(), "The key is either 'Name', 'Proportion', or 'Mutations'"
        match key:
            case "Name":
                assert value in MethodIdentifier.ALLOWED_METHODS, (f"The 'Name' key only accepts "
                                                                   f"string values from {MethodIdentifier.ALLOWED_METHODS}")
            case "Proportion":
                assert isinstance(value, float) and 0 <= value <= 1, ("The 'Proportion' key only accepts"
                                                                      "float values from [0;1]")
            case "Mutations":
                assert isinstance(value, int) and 0 <= value <= 180, ("The 'Mutations' key only accepts"
                                                                      "integer values from [0;180]")
        self.dictionary[key] = value

    def copy(self):
        return self.dictionary.copy()


class SmashMethod:
    FUNCTIONS = (SmashGenom.probabilistic, SmashGenom.average)
    REFERENCES = dict(zip(MethodIdentifier.ALLOWED_METHODS, FUNCTIONS))

    @staticmethod
    def construct_method(method_identifier: MethodIdentifier) -> callable:
        function_name = SmashMethod.REFERENCES[method_identifier["Name"]]
        weight = method_identifier["Proportion"]
        mutations = method_identifier["Mutations"]
        function = lambda genome_1, genome_2: function_name(genome_1, genome_2, weight, mutations)
        return function

if __name__ == '__main__':
    g1 = PlantGenom.random()
    g2 = PlantGenom.random()
    m = MethodIdentifier()
    method = SmashMethod.construct_method(m)
    g = method(g1, g2)
    print(g)
    print(PlantGenom.export_genom(g))
    print(g)