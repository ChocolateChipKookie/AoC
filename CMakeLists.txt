cmake_minimum_required(VERSION 3.28)
project(AoC)

find_package (Python COMPONENTS Interpreter)
set(CMAKE_CXX_STANDARD 23)

function(add_solution_target file_path)
  get_filename_component(solution_ext "${file_path}" EXT)
  if(solution_ext STREQUAL "")
    # Early exit for input and output files
    return()
  endif()
  string(SUBSTRING ${solution_ext} 1 -1 solution_ext)
  string(TOLOWER ${solution_ext} solution_ext)

  # Create target name
  get_filename_component(solution_day_path "${file_path}" DIRECTORY)
  get_filename_component(solution_day "${solution_day_path}" NAME)
  get_filename_component(solution_year_sub_path "${solution_day_path}" DIRECTORY)
  get_filename_component(solution_year_path "${solution_year_sub_path}" DIRECTORY)
  get_filename_component(solution_year "${solution_year_path}" NAME)
  string(TOLOWER ${solution_year} solution_year)
  set(target_name "${solution_year}-${solution_day}-${solution_ext}")

  # Add targets based on file type
  if(solution_ext STREQUAL "cpp")
    message("Adding c++ target: ${target_name} (${file_path})")
    set(cpp_target_name "${target_name}-build")
    add_executable(${cpp_target_name} ${file_path})
    target_include_directories(${cpp_target_name} PRIVATE "${solution_year_path}/include")

    set_target_properties(${cpp_target_name}
      PROPERTIES
      RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/cpp/"
    )
    add_custom_target(${target_name}
      COMMAND $<TARGET_FILE:${cpp_target_name}>
      DEPENDS ${cpp_target_name}
    )

    #   elseif(ext STREQUAL ".rs")
    #       add_custom_target(${target_name}
    #           COMMAND cargo build --manifest-path ${file_path}
    #           WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${dir_name})
  elseif(solution_ext STREQUAL "py")
    message("Adding c++ target: ${target_name} (${file_path})")
    add_custom_target(${target_name}
        COMMAND ${Python_EXECUTABLE} "${file_path}")
  else()
    message("Unsupported file type: ${file_path}")
  endif()
endfunction()

# Scan the directories and create targets
file(GLOB_RECURSE solution_files "AoC*/solutions/*")
foreach(file_path IN LISTS solution_files)
  add_solution_target(${file_path})
endforeach()
