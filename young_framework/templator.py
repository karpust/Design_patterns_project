from jinja2 import Template


def render(template_name, **kwargs):
    template_path = f'templates/{template_name}'
    with open(template_path, encoding='utf-8') as t:
        template = Template(t.read())
    return template.render(**kwargs)
