#!/bin/zsh

# python tests
# curriculum is excluded right now since we're not using it anyway
names=(attr clogging decorate helper math_graph mongo node nodeattribute pmdag user)
nx_names=(graph_extend digraph_extend dag)

test_names=()
for name in $names
do
	test_names=($test_names "test_${name}.py")
done
for name in $nx_names
do
	test_names=($test_names "networkx/classes/test_${name}.py")
done

py.test -x -s -vv $test_names
# py.test $test_names
