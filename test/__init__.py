import sys
import os
testdir = os.path.dirname(__file__)

# add ../src/mafia_schedule
srcdir = '../src/mafia_schedule'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

# add src/mafia_schedule - may be it helps unit test discover
srcdir = 'mafia_schedule'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


# we turn off formatting here as we need to import src AFTER changing sys.path
# fmt: off
import src.mafia_schedule
# fmt: on
