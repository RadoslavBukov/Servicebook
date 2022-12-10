
class DisabledFormMixin:
    disabled_fields = ()
    fields = {}

    def _disable_fields(self):
        if self.disabled_fields == '__all__':
            fields = self.fields.keys()
        else:
            fields = self.disabled_fields

        for field_name in fields:
            if field_name in self.fields:
                field = self.fields[field_name]
                # field.widget.attrs['disabled'] = 'disabled'
                field.widget.attrs['readonly'] = 'readonly'


# class HiddenFormMixin:
#     hidden_fields = ()
#     fields = {}
#
#     def _hidden_fields(self):
#         if self.hidden_fields == '__all__':
#             fields = self.fields.keys()
#         else:
#             fields = self.hidden_fields
#
#         for field_name in fields:
#             if field_name in self.fields:
#                 field = self.fields[field_name]
#                 field.widget.attrs['is_hidden'] = True