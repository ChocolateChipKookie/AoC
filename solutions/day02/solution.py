policy = [(*map(int, x[0].split("-")), x[1][0], x[2]) for x in [x.split(" ") for x in open("input").read().strip().split('\n')]]
print(f"First: {len([1 for x in policy if x[0] <= x[3].count(x[2]) <= x[1]])}")
print(f"Second: {len([1 for x in policy if (x[3][x[0]-1] == x[2]) != (x[3][x[1]-1] == x[2])])}")

"""
# Parse inputs to tuple(first, second, 'value', 'password')
policy = [(*map(int, x[0].split("-")), x[1][0], x[2]) for x in [x.split(" ") for x in open("input").read().strip().split('\n')]]

# First star
print(f"First: {
    len(    # Get length of resulting array
        [1 for x in policy if # Add one to array if condition is valid
            x[0] <= x[3].count(x[2]) <= x[1] # Number of values in password is in range first <= count <= second
        ]
    )}")

# Same as first, but with a bit more complicated condition
# No zero indexing
print("Second: {}".format(
    len(                                        # Get length of resulting array
        [1 for x in policy if                   # Add one to array if condition is valid
            (x[3][x[0]-1] == x[2]) != (x[3][x[1]-1] == x[2])
        ]
    )))
"""