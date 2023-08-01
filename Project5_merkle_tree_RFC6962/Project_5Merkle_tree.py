import hashlib
import math

# 计算节点的哈希值
def hash_node(left_child, right_child):
    if left_child is None:
        return right_child

    if right_child is None:
        return left_child

    sha256 = hashlib.sha256()
    sha256.update(left_child + right_child)
    return sha256.digest()

# 构建Merkle树
def build_merkle_tree(leaves):
    num_leaves = len(leaves)
    # 计算叶子节点数目最近的2的幂次方
    num_nodes = int(math.pow(2, math.ceil(math.log(num_leaves, 2))))
    tree = [None] * (2 * num_nodes - 1)

    # 填充叶子节点
    for i in range(num_leaves):
        tree[num_nodes - 1 + i] = hashlib.sha256(leaves[i].encode()).digest()

    # 计算内部节点
    for i in range(num_nodes - 2, -1, -1):
        tree[i] = hash_node(tree[2 * i + 1], tree[2 * i + 2])

    return tree

# 打印Merkle树信息
def print_merkle_tree(tree):
    num_levels = int(math.log(len(tree), 2)) + 1
    level_start_index = 0
    for level in range(num_levels):
        print("Level %d:" % level)
        level_length = int(math.pow(2, level))
        for i in range(level_start_index, level_start_index + level_length):
            node = tree[i]
            if node is not None:
                print("Node %d: %s" % (i, node.hex()))
        level_start_index += level_length
        print()


if __name__ == "__main__":
    leaves = ["data1", "data2", "data3", "data4", "data5"]
    merkle_tree = build_merkle_tree(leaves)
    print_merkle_tree(merkle_tree)

    # 打印根节点的哈希值
    print("Root hash:")
    print(merkle_tree[0].hex())

