from typing import Any, Union

from jinja2 import Environment, PackageLoader, select_autoescape, exceptions

env = Environment(loader=PackageLoader('src', 'bot/templates/messages'), autoescape=select_autoescape())


def render(
    template_name: str,
    **kwargs: Union[int, str, dict[str, Any]],
) -> str:
    if not template_name.endswith('.jinja2'):
        template_name = f'{template_name}.jinja2'
    try:
        template = env.get_template(template_name)
    except exceptions.TemplateNotFound:
        template = env.get_template(f'examples/{template_name}.example')
    rendered_template = template.render(**kwargs)
    return rendered_template.format()
