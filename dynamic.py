from flask import Flask, render_template_string, request
from wtforms import Form, StringField, IntegerField, BooleanField
import json

app = Flask(__name__)

# Map field types to WTForms classes
FIELD_TYPES = {
    "StringField": StringField,
    "IntegerField": IntegerField,
    "BooleanField": BooleanField
}

# Sample JSON schema
form_schema = [
    {"name": "username", "type": "StringField", "label": "Username"},
    {"name": "email", "type": "StringField", "label": "Email"},
    {"name": "age", "type": "IntegerField", "label": "Age"},
    {"name": "subscribe", "type": "BooleanField", "label": "Subscribe to newsletter"}
]

# Dynamic form class generator
def create_dynamic_form(schema):
    class DynamicForm(Form):
        pass

    for field in schema:
        field_class = FIELD_TYPES.get(field["type"])
        if field_class:
            setattr(DynamicForm, field["name"], field_class(field["label"]))
    return DynamicForm

# HTML template
form_template = """
<!doctype html>
<title>Dynamic Form</title>
<h2>Dynamic Form Builder</h2>
<form method="POST">
  {% for field in form %}
    <div>{{ field.label }} {{ field() }}</div>
  {% endfor %}
  <input type="submit" value="Submit">
</form>
{% if data %}
  <h3>Submitted Data:</h3>
  <pre>{{ data }}</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def dynamic_form():
    DynamicForm = create_dynamic_form(form_schema)
    form = DynamicForm(request.form)
    data = None
    if request.method == "POST" and form.validate():
        data = {field.name: field.data for field in form}
    return render_template_string(form_template, form=form, data=data)

if __name__ == "__main__":
    app.run(debug=True)




