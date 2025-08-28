from django import forms

from .models import Reservation

class ReservationForm(forms.Form):
    class Meta:
        model = Reservation
        fields = ["date", "time", "table", "guests", "celebration"]

        def __init__(self):
            super(ReservationForm, self).__init__()

            self.fields["date"].widgets.attrs.update(
                {"class": "form-control", "placeholder": "Дата"}
            )
            self.fields["time"].widgets.attrs.update(
                {"class": "form-control", "placeholder": "Время"}
            )
            self.fields["guests"].widgets.attrs.update(
                {"class": "form-control", "placeholder": "Гости"}
            )
            self.fields["table"].widgets.attrs.update(
                {"class": "form-check", "placeholder": "Стол"}
            )
            self.fields["celebration"].widgets.attrs.update(
                {"class": "radio", "placeholder": "У вас праздник?"}
            )


