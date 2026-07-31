#include <iostream>

#include <nlohmann/json.hpp>
#include <nostromodb_shared.h>


struct RS : nostromodb::ResultSetExternal {
    void on_error(std::optional<size_t> stmt_id, std::string_view code, std::string message) override {
        if (stmt_id) {
            std::println(std::cout, "Error during statement {}: {}, {}.", *stmt_id, code, message);
        } else {
            std::println(std::cout, "Error: {}, {}.", code, message);
        }
    }

    void stmt(StmtGenerator stmt_gen) override {
        for (auto&& stmt: stmt_gen) {
            std::string schema_str;
            for (size_t i = 0; i < stmt._schema.size(); i++) {
                schema_str += std::format("{}:{}", stmt._schema.at(i), stmt._schema_types.at(i));
            }
            std::println(std::cout, "\n\nSchema for statement: {}/{}:\n{}", stmt._stmt_id, stmt._type, schema_str);

            if (auto& expl = stmt._explain) {
                std::println(std::cout, "Explain:\n{}", expl->_plan_type, expl->_plan_str);
            }

            if (auto& chunk_gen = stmt._chunk_gen) {
                for (auto&& chunk: *chunk_gen) {
                    if (chunk._is_rid) {
                        std::println(std::cout, "Received chunk for column {} at offset {}:", chunk._col_id, chunk._offset);
                    } else {
                        std::println(std::cout, "Received chunk for row_id at offset {}:", chunk._offset);
                    }

                    std::visit([](auto& v) {
                        std::cout << "======================\n";
                        for (auto&& el: v) {
                            std::cout << el << "\n";
                        }
                        std::cout << "======================\n";
                    }, chunk._vec);
                }
            }
        }
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
    mgr.run_statements("select invalid");
    mgr.run_statements("explain select 1+1");
}

int main() {
    run_nostromodb_queries();
    return 0;
}