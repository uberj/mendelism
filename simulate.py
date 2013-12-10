from mendelism.cell import Cell, Chromosome1, make_gamete
import operator
import itertools
import sys

import argparse


def by_n(original_list, list_size=2):
    return [
        original_list[i:i+list_size]
        for i in xrange(0, len(original_list), list_size)
    ]


def f1_self_pollination(genome, g_results, f2_results):
    cell1 = Cell([Chromosome1(dna) for dna in genome])
    cell2 = Cell([Chromosome1(dna) for dna in genome])
    sperm, egg = make_gamete(cell1, g_results) + make_gamete(cell2, g_results)
    zygote_dna = ''.join(
        sorted(sperm.genome + egg.genome, key=lambda t: t.lower())
    )

    for gene in by_n(zygote_dna):
        dna = ''.join(sorted(gene))
        f2_results.setdefault(dna, 0)
        f2_results[dna] += 1

    return g_results, f2_results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate Miosis.')
    parser.add_argument('chromosomes', metavar='CHR', type=str, nargs='+',
                        help='A list single-stranded DNA representations')
    parser.add_argument('--num-trials', type=int, default=10000,
                        help='How many simulations should be done?')
    args = parser.parse_args()
    chroms = args.chromosomes

    lengths = {}
    for chrom in chroms:
        n = lengths.setdefault(len(chrom), 0)
        lengths[len(chrom)] += 1

    for length, count in lengths.items():
        if count % 2:
            print "There is not an even number of chromosomes length %s" % (
                length
            )
            sys.exit(1)

    NUM_TRIALS = args.num_trials
    g_results = {}
    f2_results = {}

    for x in range(NUM_TRIALS):
        f1_self_pollination(chroms, g_results, f2_results)

    def print_results(results):
        for r, n in sorted(results):
            print "%s:   %s" % (r, n)
    print "Gamete Results"
    print "--------------"
    print_results(
        [(i[0], i[1]/float(8 * NUM_TRIALS)) for i in g_results.items()]
    )
    print ""
    print "F2 Results"
    print "-----------"
    f2_numbers = [(i[0], i[1]/float(NUM_TRIALS)) for i in f2_results.items()]
    print_results(f2_numbers)
    trait_buckets = {}
    for f2_t, f2_n in f2_numbers:
        bucket = trait_buckets.setdefault(f2_t.lower(), [])
        bucket.append((f2_t, f2_n))

    print ""
    print "Aggregate Probabilities"
    print "-----------------------"
    probs = []
    num_traits = len(trait_buckets.keys())
    for el in itertools.product(*trait_buckets.values()):
        genome = ''.join(map(lambda e: e[0], el))
        prob = reduce(operator.mul, (map(lambda e: e[1], el)))
        probs.append(prob)
        print "%s:    %s" % (genome, prob)

    print "Sum of aggregate probabilities: %s " % sum(probs)
