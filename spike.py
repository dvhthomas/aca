from jinja2 import Template

med = 'paint'
selected = 'fig'
MEDIUMS = {'paint': {'display': 'Paintings', 'subtypes': {'portrait':'Portraiture','abstract':'Abstract'}},'sculpture': {'display':'Sculpture','subtypes': {'fig':'Figurative','other':'Other'}}}
template = Template("""<select>
{%- for k,data in mediums.items() %}
	<optgroup>{{data['display']}}</option>
{%- for subtype,display in data['subtypes'].items() %}
{% if k == art_type and subtype == active %}
		<option value="{{ subtype }}" selected="selected">{{ display }}</option>
{% else %}
		<option value="{{ subtype }}">{{ display }}</option>
{% endif %}
{%- endfor %}
	</optgroup>
{%- endfor%}
</select>""")
print template.render(mediums=MEDIUMS, art_type=med,active=selected)

