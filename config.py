# Compiler

ARGUMENTS: str = '-Wall -std=c++20 -g'
"""g++ compiler flags."""

# Testing 

MAX_TESTS: int = 69
"""Number of testcases to run in total."""
MAX_PARALLEL_PROCESSES: int = 4
"""Maximum number of parallel processes."""

# Limits

SOLUTION_TIMELIMIT: float = 10.0    
"""Solution time limit in seconds."""
BRUTE_TIMELIMIT: float = 10.0
"""Brute time limit in seconds."""
GENERATOR_TIMELIMIT: float = 10.0
"""Generator time limit in seconds."""
CHECKER_TIMELIMIT: float = 10.0
"""Checker time limit in seconds."""

SOLUTION_MEMORYLIMIT: float = 6
"""Solution memory limit in MB."""
BRUTE_MEMORYLIMIT: float = 512
"""Brute memory limit in MB."""
GENERATOR_MEMORYLIMIT: float = 512
"""Generator memory limit in MB."""
CHECKER_MEMORYLIMIT: float = 512
"""Checker memory limit in MB."""

# Paths

BINARY_PATH: str = 'bin'
"""Destination for all compiled binaries."""
LOG_PATH: str = 'logs'
"""Destination for all compiler messages, as well as diff file."""
OUTPUT_PATH: str = 'out'
"""Destination for all generated tests."""
OLD_PATH: str = 'src_old'
"""Destination for previously compiled source files, used to prevent unnecessary compilations."""

SOLUTION_PATH: str = 'src/sol.cpp'
BRUTE_PATH: str = 'src/brute.cpp'
GENERATOR_PATH: str = 'src/gen.cpp'
CHECKER_PATH: str = 'src/checker.cpp'

# Miscellaneous

TERMINAL_UPDATE_TIME: float = 0.3
"""Terminal refresh rate in seconds (Don't change this, unnecesary)."""
MAX_LINES: int = 50
"""Maximum number of lines when displaying output of diff file."""
MAX_LINE_LENGTH: int = 100
"""Maximum number of characters per line when displaying output of diff file."""