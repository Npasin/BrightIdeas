from config import app
from controller_functions import index, new_acc, login, logout, user_page, validate_create_idea, delete_idea, edit_page, edit_idea, like, unlike, details, users

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=new_acc, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/userpage", view_func=user_page)
app.add_url_rule("/create_idea", view_func=validate_create_idea, methods=["POST"])
app.add_url_rule("/delete_idea/<idea_id>", view_func=delete_idea)
app.add_url_rule("/edit_idea/<idea_id>", view_func=edit_page)
app.add_url_rule("/confirm_idea_edit/<idea_id>", view_func=edit_idea, methods=["POST", "GET"])
app.add_url_rule("/like_idea/<idea_id>", view_func=like)
app.add_url_rule("/unlike_idea/<idea_id>", view_func=unlike)
app.add_url_rule("/details/<idea_id>", view_func=details)
app.add_url_rule("/users", view_func=users)


