# Canonical Cell Serialization

## Cell weight

`Weight` is a characteristic of each cell in tree of cells that defines by the following:
* If cell is a leave node in a tree of cell: `weight = 1`;
* For ordinary cells (not leaves) weight is a sum: `cell weight = children weight + 1`;
* If cell is a _special_, its weight is set to zero.


The algorithm below explains how and when we assign weights to each cell to create a weight balanced tree.


## Weight reorder algorithm 

Each cell is weight balanced tree and [reorder_cells()](https://github.com/ton-blockchain/ton/blob/15088bb8784eb0555469d223cd8a71b4e2711202/crypto/vm/boc.cpp#L249) method
reassigns weights based on cumulative child weight. The traversal order is roots -> children. It's a breadth-first search, _probably_ used to preserve cache linearity. It also triggers hashes size recalculation and reindexes the bag (roots) and each tree, sets new indexes for empty references. Reindexing is depth-first though, probably there is something that depends on this order of indexing, as whitepaper states it is preferred.



To follow the original node's bag of cells serialization you should:
- First, if the cell's weights are not set (node does this on cell import), we set the weight for each cell to `1 + sum_child_weight`, where `sum_child_weight` is the sum of its child node's weights. We add one so that leaves have a weight of 1.

- Iterate all roots, for each root cell:
  * Check if each of its references has a weight less than `maximum_possible_weight - 1 + ref_index` divided by the number of root cell's refs so that they share parents weight uniformly, we do (+ index) to make sure if language casts towards 0 on division we always get a mathematically rounded number (like for 5 / 3, c++ would return 1, but we want 2 here)
      
  * If some references violate that rule, we add them to the list (or more efficiently create a bitmask, as the original node does) and then iterate again over those and clamp their weight to `weight_left / invalid_ref_count`, where `weight_left` is `maximum_possible_weight - 1 - sum_of_valid_refs_weights`. In the code it could be implemented as a decrement of a counter variable, which is first initialized to `maximum_possible_weight - 1` and then gets decremented as `counter -= valid_ref_weight`. So essentially we redistribute the remaining weight between these nodes (balance them)

- Iterate over roots again, for each root:
  * Make sure the new sum of its reference's weights is less than `maximum_possible_weight`, check if the new sum became less than the previous root cell's weight, and clamp its weight to the new sum. (if `new_sum < root_cell_weight` set `root_cell_weight` equal to `new_sum`)
  * If the new sum is higher than the root's weight, then it should be a special node, which has 0 weight, set it. (Increment Internal hashes count here by the hashes count of the node)

- Iterate over roots again, for each root:
    If it's not a special node (if its weight > 0), increment the Top hashes count by the hashes count of the node.

- Recursively reindex tree:
  * First, we previsit all root cells. If we didn't previsit or visit this node before, check all its references recursively for special nodes. If we find a special node, we have to previsit and visit it before others, it does mean that the special node's children will come first in the list (their indexes will be the lowest ones). Then we add other node's children (order deepest -> highest). Roots come at the very end of the list (they have the biggest indexes). So in the end we get a sorted list where the deeper is node, the lower index it has.


`maximum_possible_weight` is a constant 64
    
## Denotes

  * The special cell does not have weight (it's 0)
  * Make sure weight on import is fitting into 8 bits (weight <= 255)
    
  * Internal hashes count is the sum of hash counts of all special root nodes
  * The top hashes count is the sum of hash counts of all other (not special) root nodes
