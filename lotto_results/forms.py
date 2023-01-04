from django import forms


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
        error_messages={
            "invalid": "ניתן להקליד מספרים בלבד!",
        },
        widget=forms.TextInput(attrs={"placeholder": "הקלד מספר הגרלה"}),
    )

    def clean(self) -> None:
        number = self.cleaned_data.get("number")

        # Check if the form data is correctly bound to the form
        if number is not None:
            if not 2500 <= number <= 3540:
                self.add_error(
                    "number",
                    "מספר לא תקין. המספר חייב להיות בין 2500 ל-3540.",
                )
            else:
                try:
                    number = int(number)
                except ValueError:
                    self.add_error(
                        "number",
                        "ניתן להקליד מספרים בלבד!",
                    )
