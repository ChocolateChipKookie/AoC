# Advent of Code 2023 day 24
from util import *

YEAR = 2023
DAY = 24


def get_data():
    result = []
    for line in input_lines(DAY, YEAR):
        l, r = line.split(" @ ")
        pos = tuple(int(i) for i in l.split(", "))
        speed = tuple(int(i) for i in r.split(", "))
        result.append((pos, speed))
    return result


def intersection(l1, l2):
    def dot(p1, p2):
        return sum(u * v for u, v in zip(p1, p2))

    def norm2(p):
        return sum(c * c for c in p)

    def cross(p1, p2):
        return (
            p1[1] * p2[2] - p2[1] * p1[2],
            p1[2] * p2[0] - p2[2] * p1[0],
            p1[0] * p2[1] - p2[0] * p1[1],
        )

    def diff(p1, p2):
        return tuple(u - v for u, v in zip(p1, p2))

    da = l1[1]
    db = l2[1]
    dc = diff(l2[0], l1[0])

    cross_dab = cross(da, db)
    if dot(dc, cross_dab) != 0.0:
        return None
    norm_dab = norm2(cross_dab)
    if norm_dab == 0:
        return None

    s = dot(cross(dc, db), cross_dab) / norm2(cross_dab)
    if s < 0:
        return None
    return tuple(p + d * s for p, d in zip(*l1))


def first():
    test_area = 200000000000000, 400000000000000

    def ignore_z(p):
        return *p[:2], 0

    collisions = 0
    for h1 in data:
        for h2 in data:
            if h1 == h2:
                continue
            l1 = ignore_z(h1[0]), ignore_z(h1[1])
            l2 = ignore_z(h2[0]), ignore_z(h2[1])
            inter1 = intersection(l1, l2)
            inter2 = intersection(l2, l1)
            if not inter1 or not inter2:
                continue
            if all(test_area[0] <= p <= test_area[1] for p in inter1[:2]):
                collisions += 1
    return collisions // 2


def second():
    """
    x + ti * v = xi + ti * vi
    """

    def find_key_values():
        """
        Key hailstones are 2 hailstones with the same starting position
        and the same speed, in any dimension.
        Given the same speed and starting position we know that the
        starting position and speed of our rock in that dimension has to
        be the same.
        """
        for dim in range(3):
            values = [(p[dim], v[dim]) for p, v in data]
            assert len(set(values)) != len(values)
            for val in set(values):
                values.remove(val)
            if values:
                return *values.pop(), dim

    key_values = find_key_values()
    assert key_values is not None
    key_pos, key_speed, key_dim = key_values

    """
    x + ti * v = xi + ti * vi
    ti (v - vi) = xi - x
    ti = (xi - x) / (v - vi)

    Given the key dimension position and speed we can calculate the
    time to collision for each hailstone.
    Given the delta position and delta time to colision we can calculate
    the speed of the stone in that dimension.
    Now from any collision point, and time to collision and speed of the
    stone we can calculate the origin of the stone.
    """

    def calc_collision(pos, speed, time):
        return pos + speed * time

    result = 0
    for dim in range(3):
        filtered = ((p, v) for p, v in data if p[key_dim] != key_pos)
        pos1, speed1 = next(filtered)
        pos2, speed2 = next(filtered)
        time1 = (pos1[key_dim] - key_pos) // (key_speed - speed1[key_dim])
        time2 = (pos2[key_dim] - key_pos) // (key_speed - speed2[key_dim])
        collision1 = calc_collision(pos1[dim], speed1[dim], time1)
        collision2 = calc_collision(pos2[dim], speed2[dim], time2)

        dt = time2 - time1
        dp = collision2 - collision1
        v = dp // dt
        p = collision1 - v * time1
        result += p

    return result


data = get_data()

print("First:  ", first())
print("Second: ", second())
