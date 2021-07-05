from . import ip_bp
from flask import render_template, request, redirect, url_for
from sql_injection_app import db
from sql_injection_app.database import add_authentication_preset, add_product_preset, stored_procedure_preset, \
    get_all_tables, get_all_tables_with_rows, get_all_results, execute_query
from sqlalchemy.exc import OperationalError, ProgrammingError


@ip_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    try:
        db.create_all()
        add_authentication_preset()
        stored_procedure_preset()
        add_product_preset()
        tables = get_all_tables_with_rows()
    except AssertionError:
        return redirect(url_for("db_setup.blank"))
    except OperationalError:
        return redirect(url_for("db_setup.blank", error=1))
    return render_template("injection_portal/dashboard.html", db_setup_active=True, tables=tables,
                           page_title="DB Setup")


@ip_bp.route("/tautology", methods=["GET", "POST"])
def tautology():
    preset_error = None
    custom_error = None
    result = []
    query_field = None
    preset_fields = None
    try:
        tables = get_all_tables()
        if request.method == "POST":
            if list(request.form.keys()).__contains__("query_field"):
                query_field = request.form["query_field"]
                result, custom_error = execute_query(query_field)
            else:
                username = request.form["username_field"]
                password = request.form["password_field"]
                table = request.form["table_field"]
                preset_fields = [username, password, table]
                try:
                    query = "Select * from " + table + " where password='" + password + "' and username='" + username + "';"

                    print("Executing by Preset:")
                    print(query)
                    result = db.engine.execute(query)
                    preset_error = ["success", ]
                except (OperationalError, ProgrammingError) as err:
                    preset_error = ["warning", err]

    except AssertionError:
        return redirect(url_for("db_setup.blank"))

    data, preset_error, custom_error = get_all_results(result, preset_error, custom_error)

    return render_template("injection_portal/authentication.html", tautology_active=True, data=data,
                           preset_error=preset_error, custom_error=custom_error, query=query_field, tables=tables,
                           preset=preset_fields, form_action_url=url_for('injection_portal.tautology'),
                           method_title="Tautology Attack", page_title="Tautology Attack")


@ip_bp.route("/illegal", methods=["GET", "POST"])
def illegal():
    preset_error = None
    custom_error = None
    result = []
    query_field = None
    preset_fields = None
    try:
        tables = get_all_tables()
        tables = sorted(tables, reverse=True)
        if request.method == "POST":
            if list(request.form.keys()).__contains__("query_field"):
                query_field = request.form["query_field"]
                result, custom_error = execute_query(query_field)
            else:
                search = request.form["search_field"]
                table = request.form["table_field"]
                preset_fields = [search, table]
                try:
                    query = "Select * from " + table + " where name like '%%" + search + "%%';"

                    print("Executing by Preset:")
                    print(query)
                    result = db.engine.execute(query)
                    preset_error = ["success", ]
                except (OperationalError, ProgrammingError) as err:
                    preset_error = ["warning", err]
    except AssertionError:
        return redirect(url_for("db_setup.blank"))

    data, preset_error, custom_error = get_all_results(result, preset_error, custom_error)

    return render_template("injection_portal/search.html", illegal_active=True, data=data,
                           preset_error=preset_error, custom_error=custom_error, query=query_field, tables=tables,
                           preset=preset_fields, form_action_url=url_for('injection_portal.illegal'),
                           method_title="Illegal Queries Attack", page_title="Illegal Queries Attack")


@ip_bp.route("/union", methods=["GET", "POST"])
def union():
    preset_error = None
    custom_error = None
    result = []
    query_field = None
    preset_fields = None
    try:
        tables = get_all_tables()
        if request.method == "POST":
            if list(request.form.keys()).__contains__("query_field"):
                query_field = request.form["query_field"]
                result, custom_error = execute_query(query_field)
            else:
                username = request.form["username_field"]
                password = request.form["password_field"]
                table = request.form["table_field"]
                preset_fields = [username, password, table]
                try:
                    query = "Select * from " + table + " where password='" + password + "' and username='" + username + "';"

                    print("Executing by Preset:")
                    print(query)
                    result = db.engine.execute(query)
                    preset_error = ["success"]
                except (OperationalError, ProgrammingError) as err:
                    preset_error = ["warning", err]

    except AssertionError:
        return redirect(url_for("db_setup.blank"))

    data, preset_error, custom_error = get_all_results(result, preset_error, custom_error)

    return render_template("injection_portal/authentication.html", union_active=True, data=data,
                           preset_error=preset_error, custom_error=custom_error, query=query_field, tables=tables,
                           preset=preset_fields, form_action_url=url_for('injection_portal.union'),
                           method_title="Union Attack", page_title="Union Attack")


@ip_bp.route("/piggy_backed", methods=["GET", "POST"])
def piggy_backed():
    preset_error = None
    custom_error = None
    result = []
    query_field = None
    preset_fields = None
    try:
        tables = get_all_tables()
        tables = sorted(tables, reverse=True)
        if request.method == "POST":
            if list(request.form.keys()).__contains__("query_field"):
                query_field = request.form["query_field"]
                result, custom_error = execute_query(query_field)
            else:
                search = request.form["search_field"]
                table = request.form["table_field"]
                preset_fields = [search, table]
                try:
                    query = "Select * from " + table + " where name like '%%" + search + "%%';"

                    print("Executing by Preset:")
                    print(query)
                    result = db.engine.execute(query)
                    preset_error = ["success", ]
                except (OperationalError, ProgrammingError) as err:
                    preset_error = ["warning", err]
    except AssertionError:
        return redirect(url_for("db_setup.blank"))

    data, preset_error, custom_error = get_all_results(result, preset_error, custom_error)

    return render_template("injection_portal/search.html", piggy_backed_active=True, data=data,
                           preset_error=preset_error, custom_error=custom_error, query=query_field, tables=tables,
                           preset=preset_fields, form_action_url=url_for('injection_portal.piggy_backed'),
                           method_title="Piggy Backed Attack", page_title="Piggy Backed Attack")


@ip_bp.route("/stored_procedure", methods=["GET", "POST"])
def stored_procedure():
    preset_error = None
    custom_error = None
    result = []
    query_field = None
    preset_fields = None
    try:
        tables = get_all_tables()
        if request.method == "POST":
            if list(request.form.keys()).__contains__("query_field"):
                query_field = request.form["query_field"]
                result, custom_error = execute_query(query_field)
            else:
                username = request.form["username_field"]
                password = request.form["password_field"]
                table = request.form["table_field"]
                preset_fields = [username, password, table]
                try:
                    query = "Select * from " + table + " where password='" + password + "' and username='" + username + "';"

                    print("Executing by Preset:")
                    print(query)
                    result = db.engine.execute(query)
                    preset_error = ["success"]
                except (OperationalError, ProgrammingError) as err:
                    preset_error = ["warning", err]

    except AssertionError:
        return redirect(url_for("db_setup.blank"))

    data, preset_error, custom_error = get_all_results(result, preset_error, custom_error)

    return render_template("injection_portal/authentication.html", stored_procedure_active=True, data=data,
                           preset_error=preset_error, custom_error=custom_error, query=query_field, tables=tables,
                           preset=preset_fields, form_action_url=url_for('injection_portal.stored_procedure'),
                           method_title="Stored Procedure Attack", page_title="Stored Procedure Attack")


@ip_bp.route("/inference", methods=["GET", "POST"])
def inference():
    preset_error = None
    custom_error = None
    result = []
    query_field = None
    preset_fields = None
    try:
        tables = get_all_tables()
        if request.method == "POST":
            if list(request.form.keys()).__contains__("query_field"):
                query_field = request.form["query_field"]
                result, custom_error = execute_query(query_field)
            else:
                username = request.form["username_field"]
                password = request.form["password_field"]
                table = request.form["table_field"]
                preset_fields = [username, password, table]
                try:
                    query = "Select * from " + table + " where password='" + password + "' and username='" + username + "';"

                    print("Executing by Preset:")
                    print(query)
                    result = db.engine.execute(query)
                    preset_error = ["success"]
                except (OperationalError, ProgrammingError) as err:
                    preset_error = ["warning", err]

    except AssertionError:
        return redirect(url_for("db_setup.blank"))

    data, preset_error, custom_error = get_all_results(result, preset_error, custom_error)

    return render_template("injection_portal/authentication.html", inference_active=True, data=data,
                           preset_error=preset_error, custom_error=custom_error, query=query_field, tables=tables,
                           preset=preset_fields, form_action_url=url_for('injection_portal.inference'),
                           method_title="Inference Attack", page_title="Inference Attack")


@ip_bp.route("/alternate_encoding", methods=["GET", "POST"])
def alternate_encoding():
    preset_error = None
    custom_error = None
    result = []
    query_field = None
    preset_fields = None
    try:
        tables = get_all_tables()
        if request.method == "POST":
            if list(request.form.keys()).__contains__("query_field"):
                query_field = request.form["query_field"]
                result, custom_error = execute_query(query_field)
            else:
                username = request.form["username_field"]
                password = request.form["password_field"]
                table = request.form["table_field"]
                preset_fields = [username, password, table]
                try:
                    query = "Select * from " + table + " where password='" + password + "' and username='" + username + "';"

                    print("Executing by Preset:")
                    print(query)
                    result = db.engine.execute(query)
                    preset_error = ["success"]
                except (OperationalError, ProgrammingError) as err:
                    preset_error = ["warning", err]

    except AssertionError:
        return redirect(url_for("db_setup.blank"))

    data, preset_error, custom_error = get_all_results(result, preset_error, custom_error)

    return render_template("injection_portal/authentication.html", alternate_encoding_active=True, data=data,
                           preset_error=preset_error, custom_error=custom_error, query=query_field, tables=tables,
                           preset=preset_fields, form_action_url=url_for('injection_portal.alternate_encoding'),
                           method_title="Alternate Encoding Attack", page_title="Alternate Encoding Attack")
