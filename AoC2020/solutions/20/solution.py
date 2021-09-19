#Advent of Code 2020 day 20
from util import *
import math
DAY = 20
YEAR = 2020


def get_data():
    tiles = get_input(DAY, YEAR).split('\n\n')
    data = []
    for tile in tiles:
        lines = tile.split('\n')
        id = int(get_integers(lines[0])[0])
        image = lines[1:]
        data.append((id, image))
    return data


data = get_data()

edges = {}


def get_edges(tile):
    edges = []
    edges.append(tile[0])
    edges.append("".join([line[0] for line in tile[::-1]]))
    edges.append(tile[-1][::-1])
    edges.append("".join([line[-1] for line in tile]))
    return edges


for _, tile in data:
    def add_edge(edge):
        if edge in edges:
            edges[edge] += 1
        else:
            edges[edge] = 1
    for edge in get_edges(tile):
        add_edge(edge)
        add_edge(edge[::-1])


def first(data):
    res = []
    # For every tile in data
    for id, tile in data:
        # Count border edges
        count = 0
        for edge in get_edges(tile):
            # It is a border edge if it only occurs a 2n + 1 time
            if edges[edge] % 2 == 1:
                count += 1
            elif edges[edge[::-1]] % 2 == 1:
                count += 1
        if count == 2:
            res.append(id)
    return math.prod(res)


def rotate(array, times):
    def rotate_func(arr):
        return list(zip(*arr[::-1]))

    times = times % 4
    array = [[c for c in line] for line in array]
    for _ in range(times):
        array = rotate_func(array)
    return ["".join(line) for line in array]

def flip(array):
    return [line[::-1] for line in array]


def print_tile(tile):
    for line in tile:
        print(line)

def second(data):
    def create_map(data):
        corners = []
        # For every tile in data
        for id, tile in data:
            # Count border edges
            count = 0
            for edge in get_edges(tile):
                # It is a border edge if it only occurs a 2n + 1 time
                if edges[edge] % 2 == 1:
                    count += 1
                elif edges[edge[::-1]] % 2 == 1:
                    count += 1
            if count == 2:
                corners.append(id)

        dimensions = int(math.sqrt(len(data)))
        tile_dimensions = len(data[0][1])

        tiles = {id: tile for (id, tile) in data}
        edge_map = {}

        for id, tile in data:
            for edge in get_edges(tile):
                if edge in edge_map:
                    edge_map[edge].append(id)
                else:
                    edge_map[edge] = [id]

                if edge[::-1] in edge_map:
                    edge_map[edge[::-1]].append(id)
                else:
                    edge_map[edge[::-1]] = [id]

        free_edges = set(edge for edge in edges if edges[edge] % 2 == 1)

        map = [[0 for x in range(dimensions)] for y in range(dimensions)]

        """
        Start with 0 0, and then do a sweep from left to right, top to bottom
        """

        map[0][0] = corners[0]
        tile = tiles[corners[0]]
        """
        Up left down right
        Number of rotates needed for it to get to position 0    
        """
        unique = []
        for i, edge in enumerate(get_edges(tile)):
            if edges[edge] % 2 == 1:
                unique.append((i + 4) % 4)

        tiles[corners[0]] = rotate(tiles[corners[0]], min(unique))

        active_tiles = set(id for id in tiles)
        active_tiles.remove(corners[0])

        # Do the first row
        for i in range(1, dimensions):
            previous_id = map[0][i-1]
            previous_tile = tiles[previous_id]

            # Flip because different reading direction
            common_edge = get_edges(previous_tile)[3][::-1]
            # Tiles with that edge and still active
            possible_tiles = []
            for p in set(edge_map[common_edge]).intersection(active_tiles):
                # Check if any of the edges of the tile p are free
                has_free = any([edge in free_edges for edge in get_edges(tiles[p])])
                if has_free:
                    possible_tiles.append(p)

            if len(possible_tiles) > 1:
                raise RuntimeError("Too many possibilities")

            current = possible_tiles[0]
            tile = tiles[current]

            normal_edges = get_edges(tile)
            flipped_edges = [edge[::-1] for edge in normal_edges]
            if common_edge in normal_edges:
                loc = normal_edges.index(common_edge)
                tile = rotate(tile, loc - 1)
            else:
                assert common_edge in flipped_edges, "Common not in edges"
                loc = flipped_edges.index(common_edge)
                tile = rotate(tile, loc)
                tile = flip(tile)
                tile = rotate(tile, 3)
            assert get_edges(tile)[0] in free_edges, "UP EDGE NOT UNIQUE"
            tiles[current] = tile
            map[0][i] = current
            active_tiles.remove(current)

        # First column
        for i in range(1, dimensions):
            previous_id = map[i-1][0]
            previous_tile = tiles[previous_id]

            common_edge = get_edges(previous_tile)[2][::-1]
            # Tiles with that edge and still active
            possible_tiles = []
            for p in set(edge_map[common_edge]).intersection(active_tiles):
                # Check if any of the edges of the tile p are free
                has_free = any([edge in free_edges for edge in get_edges(tiles[p])])
                if has_free:
                    possible_tiles.append(p)

            if len(possible_tiles) > 1:
                raise RuntimeError("Too many possibilities")

            current = possible_tiles[0]
            tile = tiles[current]

            normal_edges = get_edges(tile)
            flipped_edges = [edge[::-1] for edge in normal_edges]
            if common_edge in normal_edges:
                loc = normal_edges.index(common_edge)
                tile = rotate(tile, loc)
            else:
                assert common_edge in flipped_edges, "Common not in edges"
                loc = flipped_edges.index(common_edge)
                tile = rotate(tile, loc)
                tile = flip(tile)
            assert get_edges(tile)[1] in free_edges, "LEFT EDGE NOT UNIQUE"
            tiles[current] = tile
            map[i][0] = current
            active_tiles.remove(current)

        # Everything else
        for y in range(1, dimensions):
            for x in range(1, dimensions):
                up_i = map[y-1][x]
                left_i = map[y][x-1]
                up = tiles[up_i]
                left = tiles[left_i]

                common_edge_up = get_edges(up)[2][::-1]
                common_edge_left = get_edges(left)[3][::-1]

                possible_up = set(edge_map[common_edge_up])
                possible_left = set(edge_map[common_edge_left])
                possible_tiles = possible_up.intersection(possible_left)
                possible_tiles = possible_tiles.intersection(active_tiles)

                if len(possible_tiles) > 1:
                    raise RuntimeError("Too many possibilities")

                current = next(iter(possible_tiles))
                tile = tiles[current]

                normal_edges = get_edges(tile)
                flipped_edges = [edge[::-1] for edge in normal_edges]
                if common_edge_up in normal_edges:
                    loc = normal_edges.index(common_edge_up)
                    tile = rotate(tile, loc)
                else:
                    assert common_edge_up in flipped_edges, "Common not in edges"
                    loc = flipped_edges.index(common_edge_up)
                    tile = rotate(tile, loc)
                    tile = flip(tile)

                assert get_edges(tile)[1] == common_edge_left, "Edges don't line up!"
                tiles[current] = tile
                map[y][x] = current
                active_tiles.remove(current)

        full_map = []
        for row in map:
            lines = ["" for x in range(1, tile_dimensions-1)]
            for tile in row:
                for i, line in enumerate(tiles[tile][1:-1]):
                    lines[i] += line[1:-1]
            full_map.extend(lines)
        return full_map

    map = create_map(data)

    map_height = len(map)
    map_width = len(map[0])

    monster_outline = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
    ]

    monster_body = [[i for i, x in enumerate(line) if x == '#'] for line in monster_outline]
    monster_height = len(monster_outline)
    monster_width = len(monster_outline[0])

    def count_monsters(map):
        monsters = []
        for y in range(0, map_height - monster_height):
            for x in range(0, map_width - monster_width):
                res = []
                for dy, line in enumerate(monster_body):
                    y_start = y + dy
                    x_start = x
                    match = [map[y_start][x_start+x] == "#" for x in line]
                    res.append(all(match))
                if all(res):
                    monsters.append((x, y))
        return monsters

    monsters = None
    for i in range(4):
        monsters = count_monsters(map)
        if len(monsters) != 0:
            break
        map = rotate(map, 1)

    if not monsters:
        map = flip(map)
        for i in range(4):
            monsters = count_monsters(map)
            if len(monsters) != 0:
                break
            map = rotate(map, 1)
    assert monsters, "Monsters not found"

    map = [[c for c in line] for line in map]
    for x, y in monsters:
        for dy, line in enumerate(monster_body):
            for dx in line:
                map[y + dy][x + dx] = '0'

    map = ["".join(line) for line in map]
    #print_tile(map)
    return sum(line.count('#') for line in map)

print(f"First:  {first(data)}")
print(f"Second: {second(data)}")
