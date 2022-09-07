from flask import Blueprint, render_template
import library.adapters.repository as repo
import library.utilities.utilities as utils


user_blueprint = Blueprint('user_bp', __name__, url_prefix="/user")



@user_blueprint.route("/<user_name>")
def user_expanded(user_name):
    user = utils.get_user(user_name)
    return render_template('user/user_extend.html', user=user)