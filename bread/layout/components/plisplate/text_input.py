from django.utils.translation import gettext as _

import plisplate

from .button import Button
from .form import FORM_NAME_SCOPED
from .icon import Icon


class TextInput(plisplate.DIV):
    def __init__(
        self, fieldname, placeholder="", light=False, widgetattributes={}, **attributes,
    ):
        self.fieldname = fieldname
        attributes["_class"] = (
            attributes.get("_class", "") + " bx--form-item bx--text-input-wrapper"
        )
        widgetattributes["_class"] = (
            widgetattributes.get("_class", "")
            + f" bx--text-input {'bx--text-input--light' if light else ''}"
        )

        super().__init__(
            plisplate.LABEL(_class="bx--label"),
            plisplate.DIV(
                plisplate.INPUT(placeholder=placeholder, **widgetattributes),
                _class="bx--text-input__field-wrapper",
            ),
            **attributes,
        )
        # for easier reference in the render method:
        self.label = self[0]
        self.input = self[1][0]

    def render(self, context):
        boundfield = context[FORM_NAME_SCOPED][self.fieldname]

        if boundfield.field.disabled:
            self.label.attributes["_class"] += " bx--label--disabled"
            self.input.attributes["disabled"] = True
        if boundfield is not None:
            self.label.attributes["_for"] = boundfield.id_for_label
            self.label.append(boundfield.label)
            if not boundfield.field.required:
                self.label.append(_(" (optional)"))
            if boundfield.help_text:
                self.append(
                    plisplate.DIV(boundfield.help_text, _class="bx--form__helper-text")
                )
            if boundfield.errors:
                self[1].attributes["data-invalid"] = True
                self[1].append(
                    Icon(
                        "warning--filled",
                        size=16,
                        _class="bx--text-input__invalid-icon",
                    )
                )
                self.append(
                    plisplate.DIV(
                        plisplate.UL(*[plisplate.LI(e) for e in boundfield.errors]),
                        _class="bx--form-requirement",
                    )
                )
        return super().render(context)


class PasswordInput(TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes["data-text-input"] = True
        self.attributes["_class"] += " bx--password-input-wrapper"
        self.input.attributes["type"] = "password"
        self.input.attributes["data-toggle-password-visibility"] = True
        self.input.attributes["_class"] += " bx--password-input"
        showhidebtn = Button(_("Show password"), notext=True)
        showhidebtn.attributes[
            "_class"
        ] = "bx--text-input--password__visibility__toggle bx--tooltip__trigger bx--tooltip--a11y bx--tooltip--bottom bx--tooltip--align-center"
        showhidebtn.append(
            Icon(
                "view--off",
                _class="bx--icon--visibility-off",
                hidden="true",
                aria_hidden="true",
            )
        )
        showhidebtn.append(
            Icon("view", _class="bx--icon--visibility-on", aria_hidden="true")
        )
        self[1].append(showhidebtn)
