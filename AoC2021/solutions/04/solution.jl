#Advent of Code 2021 day 4
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Read data from file
    first_line_end = findfirst(isequal('\n'), data)
    first_line = data[1:first_line_end]
    # Bingo numbers
    numbers = map(x->parse(Int64, x), split(strip(first_line), ','))

    # Boards data
    data = data[first_line_end:end]
    players = count("\n", data) ÷ 6
    boards = Array{Int64, 3}(undef, 5, 5, players)
    boards[:] = map(x->parse(Int64, x), split(data))
    return numbers, boards
end

function task1(data)
    numbers, boards = data
    boards = deepcopy(boards)
    players = size(boards)[3]
    board_size = 5

    function someone_won(boards)
        for player in 1:players
            board = boards[:, :, player]

            for i in 1:board_size
                if sum(board[i, :]) == 0 || sum(board[:, i]) == 0
                    return player
                end
            end
        end
        return 0
    end

    for number in numbers
        replace!(boards, number => 0)
        winner = someone_won(boards)
        if winner != 0
            println("WINNER $(winner)")
            unmarked_sum = sum(boards[:, :, winner])
            println(boards[:, :, winner])
            return(unmarked_sum * number)
        end
    end
end

function task2(data)
    numbers, boards = data
    boards = deepcopy(boards)
    players = size(boards)[3]
    board_size = 5
    winner = fill(false, players)

    last_winner = 0
    function update_winners()
        for player in 1:players
            if !winner[player]

                board = boards[:, :, player]
                for i in 1:board_size
                    if sum(board[i, :]) == 0 || sum(board[:, i]) == 0
                        winner[player] = true
                        last_winner = player
                    end
                end
            end
        end
        return count(winner)
    end

    for number in numbers
        replace!(boards, number => 0)
        winners_n = update_winners()
        if winners_n == players
            unmarked_sum = sum(boards[:, :, last_winner])
            return unmarked_sum * number
        end
    end
end


function solution()
    data = load()
    println("First: $(task1(data))")
    println("Second: $(task2(data))")
end

solution()
