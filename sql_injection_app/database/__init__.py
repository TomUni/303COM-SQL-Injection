from . import models
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError


def add_authentication_preset():
    models.db.session.add(models.authentication('admin', '123', 1))
    models.db.session.add(models.authentication('test1', 'test1', 2))
    models.db.session.add(models.authentication('test2', 'test2', 3))
    try:
        models.db.session.commit()
    except IntegrityError:
        models.db.session.rollback()


def add_product_preset():
    models.db.session.add(models.product('Product 1', '123'))
    models.db.session.add(models.product('Product 2', '2'))
    models.db.session.add(models.product('Product 3', '256'))
    try:
        models.db.session.commit()
    except IntegrityError:
        models.db.session.rollback()


def stored_procedure_preset():
    try:
        # models.db.engine.execute("DELIMITER //")
        models.db.engine.execute(
            "CREATE PROCEDURE UpdateUserRole ( IN userRole int, IN un CHAR(64)) BEGIN UPDATE authentication set role=userRole WHERE name=un; commit; END;")
        # models.db.engine.execute("DELIMITER ;")
        models.db.session.commit()
    except (IntegrityError, OperationalError):
        models.db.session.rollback()


def get_all_tables_with_rows():
    results = models.db.engine.execute("Show tables;").all()
    tables = []
    for key in results:
        tables.append([key[0], models.db.engine.execute("Select count(*) from " + key[0]).first()[0]])
    return tables


def get_all_tables():
    results = models.db.engine.execute("Show tables;").all()
    tables = []
    for key in results:
        tables.append(key[0])
    return tables


def get_all_results(result, preset_error, custom_error):
    data = []
    if result:
        if result.returns_rows:
            for key in result.all():
                data.append(key)

            if len(data) == 1:
                results_string = " result was fetched."
            else:
                results_string = " results were fetched."
            if preset_error:
                preset_error.append(str(len(data)) + results_string)
            else:
                custom_error.append(str(len(data)) + results_string)
        else:
            if preset_error:
                preset_error.append("Action has been successfully completed.")
            else:
                custom_error.append("Action has been successfully completed.")
    return data, preset_error, custom_error


def execute_query(query):
    result = []
    try:
        print("Executing by Query:")
        print(query)
        result = models.db.engine.execute(query)
        models.db.session.commit()
        custom_error = ["success"]
    except (OperationalError, ProgrammingError) as err:
        custom_error = ["warning", err]
    return result, custom_error
