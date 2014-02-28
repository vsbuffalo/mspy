import sys
import random
from collections import namedtuple
from operator import attrgetter, itemgetter

class Replicate(object):
    def __init__(self, segsites, positions, samples, command=None, seeds=None):
        self.command = command
        self.seeds = seeds
        assert(segsites == len(positions) == len(samples[0]))
        self.segsites = segsites
        self.positions = positions
        self.samples = samples
        self._pos_format = 1.4 # force some trailing zeros

    def __str__(self):
        out = (self.segsites, ' '.join(['{0:.4f}'.format(pos) for pos in self.positions]), '\n'.join(self.samples))
        # note: the trailing space after positions is in the original MS
        return "\n//\nsegsites: %d\npositions: %s \n%s\n" % out

class MSReader(object):
    def __init__(self, file_handle):
        """
        Initialize MS reader.
        """
        self._file_handle = file_handle
        self.command = None
        self.seeds = None
        self._get_header()
        self.replicates = list()

    def _get_header(self):
        """
        Get the MS command and seeds.
        """
        self.command = next(self._file_handle).strip()
        self.seeds = map(int, next(self._file_handle).strip().split())
        next(self._file_handle) # drop empty line
        next(self._file_handle) # drop first // line

    def __iter__(self):
        return self

    def next(self):
        """
        Iterator over simulations.
        """
        segsites = int(next(self._file_handle).strip().split(": ")[1])
        positions = map(float, next(self._file_handle).strip().split(": ")[1].split(" "))
        samples = list()
        line = next(self._file_handle).strip()
        while not line.startswith("//"):
            if len(line) > 0:
                samples.append(line)
            try:
                line = next(self._file_handle).strip()
            except StopIteration:
                break
        return Replicate(segsites, positions, samples, self.command, self.seeds)

    def read_replicates(self):
        """
        Read all replicates into a list.
        """
        for rep in self:
            self.replicates.append(rep)
        return self.replicates

    @property
    def header(self):
        """
        Return a string representing the header of this MS object (e.g.
        the command and seeds).
        """
        # trailing space after command follows MS.
        return "%s \n%s" % (ms.command, ' '.join(map(str, ms.seeds)))

if __name__ == "__main__":
    # as a test, this just returns the exact MS
    # input after parsing and turning it to objects.
    if sys.argv[1] == "-":
        fh = sys.stdin
    else:
        fh = open(sys.argv[1], 'r')
    ms = MSReader(fh)
    print ms.header
    for rep in ms:
        sys.stdout.write(str(rep))
