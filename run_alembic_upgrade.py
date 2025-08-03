import os
import sys

from alembic import command
from alembic.config import Config

test_mode = False

if "--test" in sys.argv:
    test_mode = True
    sys.argv.remove("--test")

if test_mode:
    os.environ["ENV"] = "test"

alembic_cnfg = Config("alembic.ini")
command.upgrade(alembic_cnfg, "head")
