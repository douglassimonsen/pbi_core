# SSAS Changes

{% for table, changes in tables_with_changes.items() %}
## {{ table.capitalize() }}

{% for change in changes %}
- {{ change.entity.__repr__() }}: {{ change.change_type.value.capitalize() }}
  {% if change.change_type.value == 'UPDATED' %}
   | Field | From | To  |
   | ----- | ---- | --- |
  {% for field, (old_value, new_value) in change.field_changes.items() -%}
   | {{ field }} | {{ old_value }} | {{ new_value }} |
  {% endfor %}
  {% endif %}
{% endfor %}

{% endfor %}

**SSAS Metadata Tables Without Changes**: {{tables_without_changes}}