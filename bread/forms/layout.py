from crispy_forms.bootstrap import Container, ContainerHolder
from crispy_forms.layout import Div, Layout
from crispy_forms.utils import TEMPLATE_PACK, render_field
from django.core.exceptions import ImproperlyConfigured
from django.forms.formsets import DELETION_FIELD_NAME
from django.template.loader import render_to_string


class InlineLayout(Layout):
    def __init__(self, inlinefield, *args, **kwargs):
        super().__init__(inlinefield)
        self.fieldname = inlinefield
        self.args = args
        self.kwargs = kwargs

    def get_inline_layout(self):
        if (
            DELETION_FIELD_NAME not in self.args
            and DELETION_FIELD_NAME not in self.kwargs
        ):
            self.args = self.args + (DELETION_FIELD_NAME, "id")
        return Layout(*self.args, **self.kwargs)


class CollapsibleGroup(Container):
    template = "%s/collapsible-group.html"


class Collapsible(ContainerHolder):
    template = "%s/collapsible.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        content = []
        self.open_target_group_for_form(form)

        for group in self.fields:
            group.data_parent = self.css_id
            content.append(
                render_field(
                    group,
                    form,
                    form_style,
                    context,
                    template_pack=template_pack,
                    **kwargs,
                )
            )

        template = self.get_template_name(template_pack)
        context.update({"collapsible": self, "content": "\n".join(content)})

        return render_to_string(template, context.flatten())


class Tab(Container):
    css_class = "tab"
    link_template = "%s/tab.html"

    def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
        return render_to_string(self.link_template % template_pack, {"tab": self})


class Tabs(ContainerHolder):
    template = "%s/tabs.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        for tab in self.fields:
            tab.errors = False

        for tab in self.fields:
            tab.errors = any(e in tab for e in form.errors.keys())

        self.open_target_group_for_form(form)
        links = "".join(tab.render_link(template_pack) for tab in self.fields)
        content = self.get_rendered_fields(form, form_style, context, template_pack)

        context.update({"tabs": self, "links": links, "content": content})
        template = self.get_template_name(template_pack)
        return render_to_string(template, context.flatten())


class Row(Div):
    @classmethod
    def with_columns(cls, *args):
        return Row(*[Col(width, field) for field, width in args])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.css_class = "row"


class Col(Div):
    def __init__(self, width=1, *args, **kwargs):
        if not 1 <= width <= 12:
            raise ImproperlyConfigured("width must be a number between 1 and 12")
        super().__init__(*args, **kwargs)
        self.css_class = f"col s{width}"