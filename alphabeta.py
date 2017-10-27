
tree = [
[[[8,3,7], [2,5,9], [5,3,8]], [[2,5,7], [9,4,8], [6,3,2]], [[4,9,5], [1,7,2], [2,4,6]]],
[[[1,4,7], [8,4,2], [5,7,8]], [[2,4,6], [9,5,6], [1,0,2]], [[4,5,3], [9,2,7], [3,1,7]]],
[[[9,5,6], [4,0,1], [3,4,5]], [[1,2,3], [7,3,4], [4,3,2]], [[8,2,7], [1,9,3], [2,7,3]]]]

tests = 0

def alphabeta(node, α, β, maximizingPlayer):
    global tests
    if isinstance(node, int):
        tests += 1
        return node
    if maximizingPlayer:
        v = -999
        for child in node:
            v = max(v, alphabeta(child, α, β, False))
            α = max(α, v)
            if β <= α:
                break # β cut-off
        return v
    else:
        v = 999
        for child in node:
            v = min(v, alphabeta(child, α, β, True))
            β = min(β, v)
            if β <= α:
                break # α cut-off
        return v

val = alphabeta(tree, -999, 999, False)
print(val)
print(tests)
