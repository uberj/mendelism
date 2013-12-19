import argparse
from itertools import product
import numpy as np


class Buckets(object):
    def __init__(self, parter=lambda i: i):
        self.parter = parter
        self.buckets = []
        self._buckets = {}

    def add(self, item):
        h = self.parter(item)
        bucket = self._buckets.setdefault(h, [])
        if not bucket in self.buckets:
            self.buckets.append(bucket)
        bucket.append(item)

    def __str__(self):
        return str(self.buckets)

    def __repr__(self):
        return repr(self.buckets)


def foil(g):
    buckets = Buckets(parter=lambda a: a.lower())
    [buckets.add(a) for a in g]
    return product(*buckets.buckets)


def main(in_g1, in_g2):
    g1 = list(foil(in_g1))
    g2 = list(foil(in_g2))

    results = []
    for products in product(g1, g2):
        results.append(''.join(map(''.join, products)))

    data = np.array(results)
    display_results(data, g1, g2)


def display_results(data, g1, g2):
    # Priting hacks

    m = len(g1)
    data.shape = (m, m)
    print "%s" % ' ' * len(list(g2)[0]),
    for g_top in g2:
        print '%s' % (''.join(g_top).ljust(m + 4)),
    print ""

    for i, g in enumerate(data):
        print "%s" % ''.join(list(g1)[i]),
        for g_i in g:
            print "%s" % ''.join(
                sorted(g_i, key=lambda a: a.lower())
            ).ljust(m + 4),
        print ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate Miosis.')
    parser.add_argument('chromosomes', metavar='CHR', type=str, nargs='+',
                        help='Genese to cross (i.e. YYRR or YyRr)')
    args = parser.parse_args()
    in_g1, in_g2 = args.chromosomes

    assert len(in_g1) == len(in_g2)

    main(in_g1, in_g2)
