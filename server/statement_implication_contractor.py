import DiGraph

def partition_cycles(cycle_nodes):
	"Given a bunch of nodes (that are ALL part of some cycle), return a set where each element is a single cycle"


def find_dir_cycles(G):
	"Look for something like P0 --> P1 --> P2 --> P0 and return the guilty :) nodes"
# 	for each connected component

# 	start at all sources simultaneously

# 	at each step, add all

# 	--

# 	runner starts at a source

# 	each step he goes down

# 	if there is an option, we launch




# -------------

# 	delete all sources, since they can't be part of a cycle
# 	delete all sinks, for the same reason
# 	repeat as long as you can!
	GC = G.clone()
	while GC.sources():
		sources = GC.sources()
		GC.remove_nodes(sources)
	# then same for sinks


	# what you are left with is cycles
	set_of_cycles = partition_cycles(cycle_nodes)
	return set_of_cycles


def contract_dir_cycle():
	# or maybe just "contract nodes" can work in full generality
	"Combine the nodes into one"

