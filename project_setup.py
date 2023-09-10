import os

has_minimal_setup = int(input("Has minimal setup\n0 - no\n1 - yes\n\n"))

if has_minimal_setup:
    folders : list = ["src", "libs"]
else:
    folders : list = ["docs", ["src", "libs"], "logs"]

for directory in folders:
    if isinstance(directory, list):  # Check if it has subdirs
        for subdirectory in directory:
            os.makedirs(subdirectory, exist_ok=True)
    else:
        os.makedirs(directory, exist_ok=True)

program_name = input("what shoudl the programs name be?\n > ")

makefile_contents : str = f"""
# Compiler and flags
CC = gcc
CFLAGS_COMMON = -Wall -Wextra -Isrc/libs -std=c2x
CFLAGS_RELEASE = -O2
CFLAGS_DEBUG = -g -DDEBUG

# Directories
SRC_DIR = src
BUILD_DIR = build
RELEASE_DIR = $(BUILD_DIR)/release
DEBUG_DIR = $(BUILD_DIR)/debug

# List of source files
SRC_FILES = $(wildcard $(SRC_DIR)/*.c)
LIB_FILES = $(wildcard $(SRC_DIR)/libs/*.c)

# Create a list of object files corresponding to source files
OBJ_RELEASE = $(patsubst $(SRC_DIR)/%.c,$(RELEASE_DIR)/%.o,$(SRC_FILES) $(LIB_FILES))
OBJ_DEBUG = $(patsubst $(SRC_DIR)/%.c,$(DEBUG_DIR)/%.o,$(SRC_FILES) $(LIB_FILES))

# Target executables
RELEASE_TARGET = $(RELEASE_DIR)/{program_name}
DEBUG_TARGET = $(DEBUG_DIR)/{program_name}

# By default, build the release version
all: release

# Release build
release: CFLAGS = $(CFLAGS_COMMON) $(CFLAGS_RELEASE)
release: $(RELEASE_TARGET)

$(RELEASE_TARGET): $(OBJ_RELEASE)
        $(CC) $(CFLAGS) -o $@ $^

$(RELEASE_DIR)/%.o: $(SRC_DIR)/%.c
        @mkdir -p $(@D)
        $(CC) $(CFLAGS) -c $< -o $@

# Debug build
dev: CFLAGS = $(CFLAGS_COMMON) $(CFLAGS_DEBUG)
dev: $(DEBUG_TARGET)

$(DEBUG_TARGET): $(OBJ_DEBUG)
        $(CC) $(CFLAGS) -o $@ $^

$(DEBUG_DIR)/%.o: $(SRC_DIR)/%.c
        @mkdir -p $(@D)
        $(CC) $(CFLAGS) -c $< -o $@

# Clean rule
clean:
        rm -rf $(BUILD_DIR)

.PHONY: all release debug clean
"""

with open("makefile", "w") as f:
    f.write(makefile_contents)

with open("src/main.c", "w") as f2:
    f2.write("""#include <stdio.h>\n\n\nint main(void){\n\nprintf("Hello, world!");\n\nreturn 0;}""")
