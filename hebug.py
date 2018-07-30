import sys

from httptest.cli import main
from httptest.logger import logger

cmd = sys.argv.pop(1)

if cmd in ["htest"]:
    main()
else:
    logger.error("Miss debugging type.")
    example = "\n".join([
        "e.g.",
        "python hebug.py htest /path/to/testset_file"
    ])
    logger.error(example)