# mspy -- parse MS output into Python objects.

mspy is a (sort of stupidly) simple library to parse output Hudson's MS into
Python objects. The interface will mostly certainly change drastically, so
don't use in production.

## Installation

Install with:

    $ python setup.py install

## Examples

Load some MS output, do nothing, and print it out in MS format:

    # ms_cat.py
    import ms
		import sys

    ms = msReader(sys.stdin)
    sys.stdout.write(ms.header) # return ms header

    for rep in ms:
			sys.stdout.write(str(rep)) # print works too, but adds spaces

Then:

    ms 10 2 -t 10 | python ms_cat.py

## License

Copyright Vince Buffalo, 2014. Distributed under a BSD License.
