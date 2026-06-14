cmake_minimum_required(VERSION 4.2)
project(nostromodb_public)

set(CMAKE_CXX_STANDARD 23)

# The nostromodb shared library package needs to be installed.
find_library(NOSTROMODB_LIB NAMES nostromodb_shared)

include(FetchContent)
FetchContent_Declare(
        json
        GIT_REPOSITORY https://github.com/nlohmann/json.git
        GIT_TAG "v3.12.0"
        GIT_SHALLOW TRUE
        GIT_PROGRESS ON
        SYSTEM
)
FetchContent_MakeAvailable(json)

add_subdirectory(example)

