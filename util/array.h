//
// Created by Adi on 12/9/2022.
//

#ifndef AOC_ARRAY_H
#define AOC_ARRAY_H

#include <array>
#include <vector>
#include <cassert>
#include <exception>
#include <ranges>
#include <ostream>
#include <istream>
#include <sstream>

template <typename T_data>
class Grid {
private:
    class GridSpan{
    public:
        explicit GridSpan(std::vector<T_data>& data, size_t start, size_t stride)
            :   _data(data),
                _start(start),
                _stride(stride)
        {}
        T_data& operator[](size_t i){
            return _data[_start + _stride * i];
        }
    private:
        std::vector<T_data>& _data;
        size_t _stride;
        size_t _start;
    };

    std::array<size_t, 2> _size {0, 0};
    std::vector<T_data> _data;

    template<class T>
    static T parse(char c){
        return c;
    };

    template<>
    static char parse<char>(char c){
        return c;
    }

    template<>
    static int parse<int>(char c){
        return c - '0';
    }

public:
    Grid() = default;

    Grid(size_t width, size_t height, T_data fill = 0)
        :   _size{width, height},
            _data(width * height, fill)
    {};

    explicit Grid(std::array<size_t, 2> size, T_data fill = 0)
            :   _size{size},
                _data(size[0] * size[1], fill)
    {};


    ///////////////////
    /// Data access ///
    ///////////////////
    [[nodiscard]] T_data& get(size_t i){
        return _data.at(i);
    }
    [[nodiscard]] T_data& get(size_t x, size_t y){
        return _data.at(get_index(x, y));
    }

    [[nodiscard]] T_data& operator ()(size_t i){
        return _data[i];
    }
    [[nodiscard]] T_data& operator ()(size_t x, size_t y){
        return _data[get_index(x, y)];
    }
    [[nodiscard]] T_data get(size_t i) const {
        return _data.at(i);
    }
    [[nodiscard]] T_data get(size_t x, size_t y) const {
        return _data.at(get_index(x, y));
    }

    [[nodiscard]] T_data operator ()(size_t i) const {
        return _data[i];
    }
    [[nodiscard]] T_data operator ()(size_t x, size_t y) const {
        return _data[get_index(x, y)];
    }

    [[nodiscard]] Grid::GridSpan slice(size_t i, size_t dim = 1){
        if (dim == 1){
            return GridSpan(_data, i, _size[0]);
        }
        if (dim == 0){
            return GridSpan(_data, _size[0] * i, 1);
        }
        return ;
    }
    [[nodiscard]] Grid::GridSpan operator[](size_t x){
        return GridSpan(_data, x, _size[0]);
    }

    ////////////
    /// Size ///
    ////////////

    void resize(const std::array<size_t, 2>& new_size, T_data fill = 0){
        size_t new_length = new_size[0] * new_size[1];

        if (new_length > length()){
            _data.resize(new_length);
        }

        if (new_size[0] < _size[0]){
            for (size_t y = 0; y < std::min(new_size[1], _size[1]); ++y){
                for (size_t x = 0; x < new_size[0]; ++x){
                    size_t new_pos = x + y * new_size[0];
                    size_t old_pos = get_index(x, y);
                    _data[new_pos] = _data[old_pos];
                }
            }

            for (size_t y = _size[1]; y < new_size[1]; ++y){
                for (size_t x = 0; x < new_size[0]; ++x){
                    size_t new_pos = x + y * new_size[0];
                    _data[new_pos] = fill;
                }
            }
        }
        else if (new_size[0] > _size[0]){
            for (size_t y = new_size[1] - 1; y < new_size[1]; --y){
                for (size_t x = new_size[0] - 1; x < new_size[0]; --x){
                    size_t new_pos = x + y * new_size[0];
                    size_t old_pos = get_index(x, y);
                    _data[new_pos] = _data[old_pos];
                }
            }
            for (size_t y = 0; y < new_size[1]; ++y){
                for (size_t x = _size[0]; x < new_size[0]; ++x){
                    size_t new_pos = x + y * new_size[0];
                    _data[new_pos] = fill;
                }
            }
        }

        if (new_length < length()){
            _data.resize(new_length);
        }
        _size = new_size;
    }

    [[nodiscard]] std::array<size_t, 2> size() const {
        return _size;
    }
    [[nodiscard]] size_t length() const {
        return _data.size();
    }

    [[nodiscard]] const std::vector<T_data>& data() const {
        return _data;
    }

    [[nodiscard]] std::vector<T_data>& data() {
        return _data;
    }

    [[nodiscard]] size_t get_index(size_t x, size_t y) const {
        return y * _size[0] + x;
    }

    [[nodiscard]] std::array<size_t, 2> get_position(size_t i) const {
        return {i % _size[0], i / _size[0]};
    }


    /////////////////////////////
    /// Input/Output sterams  ///
    /////////////////////////////
    friend std::istream& operator>>(std::istream& is, Grid<T_data>& grid){
        char c;

        size_t i = 0;
        size_t width = 0;
        size_t height = 0;
        while (true){
            if (is.eof()){
                height += 1;
                break;
            }
            is.get(c);
            if (c == '\n'){
                height += 1;
                if(is.peek() == '\n'){
                    break;
                }
                if (width == 0) {
                    width = i;
                }
            }
            else{
                grid._data.push_back(parse<T_data>(c));
                i += 1;
            }
        }
        grid._size = {width, height};
        grid._data.resize(width * height);
        return is;
    }

    friend std::ostream& operator<<(std::ostream& os, const Grid<T_data>& grid){
        for (size_t i = 0; i < grid._data.size(); ++i){
            os << grid._data[i];
            if ((i + 1) % grid._size[0] == 0){
                os << '\n';
            }
        }
        return os;
    }
};

using IntGrid = Grid<int>;
using CharGrid = Grid<char>;

#endif //AOC_ARRAY_H
