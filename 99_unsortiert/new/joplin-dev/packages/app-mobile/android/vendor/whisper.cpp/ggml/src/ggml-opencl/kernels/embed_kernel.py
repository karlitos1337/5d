#

import logging
import sys

logger = logging.getLogger("opencl-embed-kernel")


def main():
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) != 3:
        logger.info("Usage: python embed_kernel.py <input_file> <output_file>")
        sys.exit(1)

    ifile = open(sys.argv[1])
    ofile = open(sys.argv[2], "w")

    for i in ifile:
        ofile.write(f'R"({i})"\n')

    ifile.close()
    ofile.close()


if __name__ == "__main__":
    main()
