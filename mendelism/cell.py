import sys
import random
import itertools


class Chromosome1(object):
    """A single strand of DNA"""
    def __init__(self, dna):
        self.dna = list(dna)

    def __len__(self):
        return len(self.dna)

    def __str__(self):
        return "%s" % ''.join(sorted(self.dna))

    def __repr__(self):
        return "<Single-DNA-Strand %s>" % self

    @classmethod
    def replicate(cls, ch):
        return cls(ch.dna)


class Homolog(object):
    """A chromosomes with two sister chromatids"""
    def __init__(self, ch1, ch2):
        self.sister1 = ch1
        self.sister2 = ch2

    def __len__(self):
        return len(self.sister1)

    def __str__(self):
        return "%s | %s" % (self.sister1, self.sister2)

    def __repr__(self):
        return "<Homologous Chromosome %s>" % self


class Cohesion(object):
    @classmethod
    def bind(cls, ch1, ch2):
        return Homolog(ch1, ch2)


class Cell(object):
    def __init__(self, chromosomes):
        self.chromosomes = chromosomes
        self.state = 'G0'

    def __str__(self):
        return "state %s -- %s" % (self.state, self.chromosomes)

    def __repr__(self):
        return "<Cell %s>" % self

    @property
    def genes(self):
        genes = {}
        for ch in self.chromosomes:
            for allele in ch.dna:
                genes.setdefault(allele.upper(), []).append(allele)
        return genes

    @property
    def genome(self):
        genome = ''
        for charater, gene in self.genes.iteritems():
            genome += ''.join(gene)
        return genome

    def mieosis(self):
        # Make a cell go through miosis
        Cell.synthesize(self)
        self.state = 'M'
        Cell.prophase_1(self)
        Cell.metaphase_1(self)
        Cell.anaphase_1(self)
        Cell.telophase_1(self)
        cell1, cell2 = Cell.cytokinesis_1(self)

        def miosis_2(cell):
            Cell.prophase_2(cell)
            Cell.metaphase_2(cell)
            Cell.anaphase_2(cell)
            Cell.telophase_2(cell)
            return Cell.cytokinesis_2(cell)

        return itertools.chain(miosis_2(cell1), miosis_2(cell2))

    @classmethod
    def synthesize(cls, cell):
        """Copy the each chromosome"""
        cell.state = 'S'
        cell.chromosomes = [
            cell.chromosomes, map(Chromosome1.replicate, cell.chromosomes)
        ]
        cell.state = 'G2'

    @classmethod
    def prophase_1(cls, cell):
        """The chromosomes form homologous pairs consisting of who pairs of
        sister chromatids
        """
        cell.state = 'Prophase I'

        # Homologs form
        cell.chromosomes = list(
            itertools.starmap(Homolog, zip(*cell.chromosomes))
        )

        homoloug_pairs = []

        # Homologs are paired off
        for i in range(0, len(cell.chromosomes), 2):
            chs = [cell.chromosomes[i], cell.chromosomes[i + 1]]
            # We need to chose randomly between these two chromosomes. One will
            # end up in one cell after cytokinesisI and one will end up in the
            # other.
            random.shuffle(chs)
            homoloug_pairs.append(chs)

        # Cross over the sister1 chromatids
        for pair in homoloug_pairs:
            c_len = len(pair[0].sister1) - 1
            crossover_points = [
                random.randint(0, c_len)
                for x in xrange(random.randint(0, c_len))
            ]
            for point in crossover_points:
                # Swap allels
                pair[0].sister1.dna[point], pair[1].sister2.dna[point] = (
                    pair[1].sister2.dna[point], pair[0].sister1.dna[point]
                )

        cell.chromosomes = homoloug_pairs

    @classmethod
    def metaphase_1(cls, cell):
        cell.state = 'Metaphase I'
        # The metaphase plate forms

    @classmethod
    def anaphase_1(cls, cell):
        cell.state = 'Anaphase I'
        # The metaphase plate is broken and homologs start traveling toward
        # their respective poles
        dna1, dna2 = zip(*cell.chromosomes)
        cell.chromosomes = [dna1, dna2]

    @classmethod
    def telophase_1(cls, cell):
        cell.state = 'Telophase I'

    @classmethod
    def cytokinesis_1(cls, cell):
        cell.state = 'Cytokensis I'
        # Create two new haploid daughter cells
        return cls(cell.chromosomes[0]), cls(cell.chromosomes[1])

    @classmethod
    def prophase_2(cls, cell):
        cell.state = 'Prophase II'
        # spindles forming

    @classmethod
    def metaphase_2(cls, cell):
        cell.state = 'Metaphase II'
        # metaphase plate forms

    @classmethod
    def anaphase_2(cls, cell):
        cell.state = 'Anaphase II'
        # Split the sister chromatids
        cell.chromosomes = [
            [ch.sister1, ch.sister2] for ch in cell.chromosomes
        ]
        # Shuffle chromatids onto either side of the metaphase plate
        map(random.shuffle, cell.chromosomes)

    @classmethod
    def telophase_2(cls, cell):
        cell.state = 'Telophase II'

    @classmethod
    def cytokinesis_2(cls, cell):
        cell.state = 'Cytokensis II'
        dna1, dna2 = zip(*cell.chromosomes)
        return Gamete(dna1), Gamete(dna2)


class Gamete(Cell):
    def __repr__(self):
        return "<Gamete %s>" % self


def by_n(original_list, list_size=2):
    return [
        original_list[i:i+list_size]
        for i in xrange(0, len(original_list), list_size)
    ]


def make_gamete(cell, g_results):
    gametes = list(cell.mieosis())
    # Record for debugging analysis
    for cell in gametes:
        g_results.setdefault(cell.genome, 0)
        g_results[cell.genome] += 1
    return random.sample(gametes, 1)
