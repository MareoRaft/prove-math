#!/bin/zsh

# python tests
# curriculum is excluded right now since we're not using it anyway
names=(attr clogging  decorate helper math_graph mongo node nodeattribute pmdag user)

test_names=()
for name in $names; do
	test_names=($test_names "test_${name}.py")
done;

py.test -x -s -vv $test_names
