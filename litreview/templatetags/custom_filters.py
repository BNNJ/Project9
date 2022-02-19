from django import template

register = template.Library()

@register.filter(name='field_type')
def field_type(field):
	return field.__class__.__name__

@register.filter(name='add_classes')
def add_classes(tag, args):
	"""Add classes to a field input tag"""
	base = tag.field.widget.attrs.get('class', '').split()
	new = args.split(' ')
	classes = ' '.join(set(base + new)).strip()
	return tag.as_widget(attrs={'class': classes})

@register.filter(name='get_page')
def get_page(url):
	return url.split('/')[1]

@register.filter(name='string_list')
def string_list(args):
	return args.split(' ')

@register.filter(name='qurl')
def qurl(url, params):
	if url[-1] == '/':
		url = url[:-1]

	params = {p.split('=')[0]: p.split('=')[1] for p in params.split(',')}

	qstring = '&'.join(f"{k}={v}" for k, v in params.items())

	return f"{url}?{qstring}"
