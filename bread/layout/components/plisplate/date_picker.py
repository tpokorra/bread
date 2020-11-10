from _strptime import TimeRE

from bread.utils.datetimeformatstring import to_php_formatstr
from django.utils import formats
from django.utils.translation import gettext as _

import plisplate

from .form import FORM_NAME_SCOPED
from .icon import Icon


class DatePicker(plisplate.DIV):
    def __init__(
        self,
        fieldname,
        placeholder="",
        light=False,
        short=False,
        simple=False,
        widgetattributes={},
        **attributes,
    ):
        self.fieldname = fieldname
        attributes["_class"] = attributes.get("_class", "") + " bx--form-item"
        picker_attribs = (
            {}
            if simple
            else {"data-date-picker": True, "data-date-picker-type": "single"}
        )
        widgetattributes["_class"] = (
            widgetattributes.get("_class", "") + " bx--date-picker__input"
        )

        input = plisplate.INPUT(
            placeholder=placeholder, type="text", **widgetattributes,
        )
        self.input = input
        if not simple:
            input.attributes["data-date-picker-input"] = True
            input = plisplate.DIV(
                input,
                Icon(
                    "calendar",
                    size=16,
                    _class="bx--date-picker__icon",
                    data_date_picker_icon="true",
                ),
                _class="bx--date-picker-input__wrapper",
            )

        super().__init__(
            plisplate.DIV(
                plisplate.DIV(
                    plisplate.LABEL(_class="bx--label"),
                    input,
                    _class="bx--date-picker-container",
                ),
                _class="bx--date-picker"
                + (" bx--date-picker--simple" if simple else "bx--date-picker--single")
                + (" bx--date-picker--short" if short else "")
                + (" bx--date-picker--light" if light else ""),
                **picker_attribs,
            ),
            **attributes,
        )
        # for easier reference in the render method:
        self.label = self[0][0][0]
        self.simple = simple

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
            else:
                self.input.attributes["required"] = True

            dateformat = (
                boundfield.field.widget.format
                or formats.get_format(boundfield.field.widget.format_key)[0]
            )
            dateformat_widget = to_php_formatstr(
                boundfield.field.widget.format, boundfield.field.widget.format_key
            )
            if self.simple:
                self.input.attributes["pattern"] = TimeRE().compile(dateformat).pattern
            else:
                self.input.attributes["data_date_format"] = dateformat_widget

            if boundfield.auto_id:
                self.input.attributes["id"] = boundfield.auto_id
            self.input.attributes["name"] = boundfield.html_name
            value = boundfield.field.widget.format_value(boundfield.value())
            if value is not None:
                self.input.attributes["value"] = value
            if boundfield.help_text:
                self[0][0].append(
                    plisplate.DIV(boundfield.help_text, _class="bx--form__helper-text")
                )
            if boundfield.errors:
                self.input.attributes["data-invalid"] = True
                self[0][0].append(
                    plisplate.DIV(
                        plisplate.UL(*[plisplate.LI(e) for e in boundfield.errors]),
                        _class="bx--form-requirement",
                    )
                )
                self[1].append(
                    Icon(
                        "warning--filled",
                        size=16,
                        _class="bx--text-input__invalid-icon",
                    )
                )
        return super().render(context)