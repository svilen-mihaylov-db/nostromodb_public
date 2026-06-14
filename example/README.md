Example usage of nostromodb's shared library.

The main piece of the demo is the "RS" struct which extends from nostromodb's internal structures. It delivers
results back to the client. There are several methods which return schema information, errors, results, etc.
Override the handlers to work in a way that is suitable to your application.

The DBManager is initialized with std::nullopt as first argument which makes it temporary. Supply a filename 
in an existing directory to persist the database. The directory needs to exists, but not the filename (it is created if needed).

Lastly, several example queries are issued.