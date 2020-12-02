import itertools
import numpy

print(numpy.prod(next(filter(lambda x: sum(x) == 2020, itertools.product(*([[x for x in map(int, open("input").read().split())]] * 2))))))
print(numpy.prod(next(filter(lambda x: sum(x) == 2020, itertools.product(*([[x for x in map(int, open("input").read().split())]] * 3))))))

"""
print(                                                                      # 9. Print the solution
    numpy.prod(                                                             # 8. multiply all the components
        next(                                                               # 7. Take the first element of the filter
            filter(                                                         # 6. Filter the cross product list
                lambda x: sum(x) == 2020,                                   # 5. Sum of all components == component_sum
                itertools.product(                                          # 4. Cross product of n copies of inputs
                    *([                                                     # 3. Unpacks the inputs to cross product
                        [x for x in map(int, open("input").read().split())] # 1. Creates a list of inputs
                    ] * 2)))                                                # 2. Creates list of copies
            )
        )
    )
"""