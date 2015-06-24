#!/usr/bin/env perl

# This perl script will use regex to convert .pre-json files to .json files


# 1. All comments will be deleted

# 2. Commas will be added to the end of all top-level dics

# 3. Everything will be wrapped in a large array

# 4. Lists and arrays where the last element is followed by a comma will have the comma deleted
