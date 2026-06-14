add_executable(nostromodb_example
        main.cpp
)
target_link_libraries(nostromodb_example
        PRIVATE ${NOSTROMODB_LIB}
        PRIVATE nlohmann_json::nlohmann_json
)