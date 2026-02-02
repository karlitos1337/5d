#
#

import logging
import sys

logger = logging.getLogger("opencl-embed-kernel")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logger.error("Usage: %s <input> <output>" % sys.argv[0])
        sys.exit(1)

    ifile = open(sys.argv[1])
    ofile = open(sys.argv[2], "w")

    for i in ifile:
        ofile.write(f'R"({i})"\n')

    ifile.close()
    ofile.close()
