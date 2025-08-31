from datetime import timedelta, datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Reservation, Table


class ReservationForm(forms.ModelForm):
    # Кастомные choices для времени
    TIME_CHOICES = [
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
    ]

    DURATION_CHOICES = [
        (1, '1 час'),
        (2, '2 часа'),
        (3, '3 часа'),
        (4, '4 часа'),
        (5, '5 часов'),
    ]

    start_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.RadioSelect,
        label="Время"
    )

    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.RadioSelect,
        label="Продолжительность бронирования"
    )

    class Meta:
        model = Reservation
        fields = ["date", "start_time", "duration", "table", "guests", "celebration"]
        labels = {
            "date": "Дата",
            "start_time": "Время",
            "duration": "Продолжительность бронирования",
            "table": "Стол",
            "guests": "Количество гостей",
            "celebration": "Праздник"
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control datepicker'}),
            'table': forms.Select(attrs={'class': 'form-select'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'celebration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        # Динамически загружаем столы
        self.fields['table'].queryset = Table.objects.filter(status=True)
        self.fields['table'].empty_label = "Выберите стол"

        # Устанавливаем атрибуты для options столов
        self.fields['table'].widget.attrs.update({
            'class': 'form-select',
            'data-live-search': 'true'
        })

        # Устанавливаем начальную дату (сегодня)
        self.fields['date'].initial = timezone.now().date()

        # Для radio кнопок времени
        self.fields['start_time'].widget.attrs = {'class': 'btn-check'}
        self.fields['duration'].widget.attrs = {'class': 'btn-check'}

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        date = cleaned_data.get("date")  # Исправлено: cleaned_data вместо self.cleaned_data
        time = datetime.strptime(cleaned_data.get("start_time"), '%H:%M').time()
        guests = cleaned_data.get("guests")
        table = cleaned_data.get("table")
        now_date = timezone.localtime(timezone.now()).date()
        now_time = timezone.localtime(timezone.now()).time()

        try:
            table_reservation = Reservation.objects.get(date=date, table=table)
                    # Создаем фиктивную дату
            dummy_date = timezone.now().date()
            # Комбинируем дату и время
            combined_datetime = datetime.combine(dummy_date, time)
            # Прибавляем часы
            reserve_time = combined_datetime + timedelta(hours=table_reservation.duration)
            if date and time and date == now_date and time <= reserve_time.time():
                raise ValidationError("Столик на это время уже занят")
        except Reservation.DoesNotExist:
            pass



        # Проверка даты
        if date and date < now_date:
            raise ValidationError("Невозможно забронировать столик на прошедшую дату")

        # Проверка времени (только если дата сегодня)
        if date and time and date == now_date and time <= now_time:
            raise ValidationError("Невозможно забронировать столик на прошедшее время")

        # Проверка количества гостей
        if guests and guests < 1:
            raise ValidationError("Число гостей не может быть меньше 1")

        # Проверка вместимости стола
        if guests and table and hasattr(table, 'seats'):
            if guests > table.seats:
                raise ValidationError(f"Число гостей не может быть больше {table.seats}")

        # Проверка состояния стола
        if not table.status:
            raise ValidationError(f"Стол {table.number} не доступен для бронирования")



        return cleaned_data