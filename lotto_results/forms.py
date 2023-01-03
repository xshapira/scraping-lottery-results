from django import forms
from django.core.exceptions import ValidationError


class LotteryResultsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        fields = ("number",)
        required = ("number",)
        labels = {"number": "מספר ההגרלה:"}
        widgets = {
            "number": forms.TextInput(
                attrs={"placeholder": "הקלד מספר הגרלה"},
            )
        }

    number = forms.IntegerField(
        min_value=2500,
        max_value=3540,
        widget=forms.TextInput(attrs={"placeholder": "הקלד מספר הגרלה"}),
    )

    def clean(self) -> None:
        if number := self.cleaned_data.get("number"):
            try:
                number = int(number)
            except ValidationError:
                self.add_error(
                    "number",
                    "ניתן להקליד מספרים בלבד!",
                )

            else:
                if not 2500 <= number <= 3540:
                    self.add_error(
                        "number",
                        forms.ValidationError(
                            "מספר לא תקין. המספר חייב להיות בין 2500 ל-3540."
                        ),
                    )

        else:
            self.add_error(
                "number",
                forms.ValidationError("נא הקלד מספר הגרלה."),
            )
