#include <iostream>

#include <nlohmann/json.hpp>
#include <nostromodb_shared.h>


struct RS : nostromodb::ResultSetExternal {
    void on_error(std::optional<size_t> stmt_id, std::string_view code, std::string message) override {
        std::println(std::cout, "Error: {}, {}.", code, message);
    }

    void set_schema(size_t stmt_id, std::string_view type, Schema schema, SchemaTypes schema_types) override {
        std::string schema_str;
        for (size_t i = 0; i < schema.size(); i++) {
            schema_str += std::format("{}:{}", schema.at(i), schema_types.at(i));
        }
        std::println(std::cout, "\nSchema for statement: {}/{}:\n{}", stmt_id, type, schema_str);
    }

    void explain(size_t stmt_id, std::string_view plan_type, const std::string &plan_str) override {
        std::println(std::cout, "Statement {} {} explain:\n{}", stmt_id, plan_type, plan_str);
    }

    void column_chunk(size_t stmt_id, size_t col_id, size_t offset, std::vector<nlohmann::json> chunk) override {
        std::println(std::cout, "Statement {}: received column chunk for column {} at offset {}:\n{}", stmt_id, col_id, offset, to_string(nlohmann::json(chunk)));
    }

    void row_ids_chunk(size_t stmt_id, size_t offset, std::vector<uint64_t> chunk) override {
        std::println(std::cout, "Statement {}: received row_id at offset {}:\n{}", stmt_id, offset, to_string(nlohmann::json(chunk)));
    }

    void finished(size_t stmt_id, size_t num_selected, bool has_error) override {
        std::println(std::cout, "Statement {} finished.", stmt_id);
    }
};

void run_nostromodb_queries() {
    nostromodb::DbManager mgr{std::nullopt, std::make_unique<RS>()};
    mgr.run_statements("select 1+2");
    mgr.run_statements(R"(
insert into t values ({'a': 1, 'b': '1'}, {'a': 2, 'b': '2'}, {'a': 3, 'b': '3'});
pragma show_tables();
select a, b from t;
select sum(a) from t
)");
}

int main() {
    run_nostromodb_queries();
    return 0;
}