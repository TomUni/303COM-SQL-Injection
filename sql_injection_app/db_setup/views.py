from . import ds_bp
from flask import render_template, request, redirect, url_for


@ds_bp.route("/<int:error>", methods=["GET", "POST"])
@ds_bp.route("/", methods=["GET", "POST"], defaults={"error": 0})
def blank(error):
    if error == 0:
        error = None
    elif error == 1:
        error = "Unable to connect with database."
    from sql_injection_app import app, db
    if request.method == "POST":
        host = request.form["host_field"]
        port = int(request.form["port_field"])
        user = request.form["user_field"]
        password = request.form["password_field"]
        db_name = request.form["database_field"]
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://' + user + ':' + password + '@' + host + ':' + str(
            port) + '/' + db_name + '?charset=utf8mb4'
        try:
            db.init_app(app)
            if db.session:
                return redirect(url_for("injection_portal.dashboard"))
        except Exception as e:
            error = e.__traceback__
    return render_template("db_setup/blank.html", db_setup_active=True, error=error, page_title="SQL Injection App")
