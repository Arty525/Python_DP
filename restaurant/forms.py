import os
from datetime import timedelta, datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from .models import Reservation, Table, Content, Contacts, Team, Service, Feedback, Chief, SousChef


class ReservationSearchForm(forms.Form):

    START_TIME_CHOICES = [
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

    start_time = forms.ChoiceField(
        choices=START_TIME_CHOICES,
        widget=forms.RadioSelect,
        label="Время",
        required=False
    )

    class Meta:
        fields = ["date", "start_time", "first_name", "last_name", "table", "guests", "celebration"]
        labels = {
            "date": "Дата",
            "start_time": "Время",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "table": "Стол",
            "guests": "Количество гостей",
            "celebration": "Праздник"
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control datepicker'}),
            'first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control textinput'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control textinput'}),
            'table': forms.Select(attrs={'class': 'form-select'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'celebration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReservationForm(forms.ModelForm):
    # Кастомные choices для времени
    START_TIME_CHOICES = [
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
        choices=START_TIME_CHOICES,
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
        date = cleaned_data.get("date")
        duration = int(cleaned_data.get("duration"))
        time = datetime.strptime(cleaned_data.get("start_time"), '%H:%M').time()
        guests = cleaned_data.get("guests")
        table = cleaned_data.get("table")
        now_date = timezone.localtime(timezone.now()).date()
        now_time = timezone.localtime(timezone.now()).time()

        dummy_date = timezone.now().date()
        combined_datetime = datetime.combine(dummy_date, time)
        reserve_time = combined_datetime + timedelta(hours=duration)

        print(reserve_time.time(),"|", datetime.strptime("22:00", '%H:%M').time())

        if reserve_time.time() > datetime.strptime("22:00", '%H:%M').time():
            raise forms.ValidationError("Время бронирования превышает время работы ресторана")

        try:
            table_reservation = Reservation.objects.get(date=date, table=table, status__in=['active', 'created'])
            if table_reservation:
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


class CarouselUploadForm(forms.ModelForm):
    content_type = forms.CharField(initial='carousel', widget=forms.HiddenInput())
    class Meta:
        model = Content
        fields = ['content_type', 'title', 'image', 'is_active']
        required = ['image', 'title']
        labels = {
            "title": "Название",
            "image": "Изображение",
            "is_active": "Показ изображения"
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image is None:
            raise ValidationError('Загрузите изображение')

        valid_extensions = ['.jpg', '.jpeg', '.png']
        extension = os.path.splitext(image.name)[1].lower()
        if extension not in valid_extensions:
            raise ValidationError(f'Недопустимый формат файла, разрешены форматы: {valid_extensions}')

        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError('Файл слишком большой. Максимальный размер 5 Мб')
        return image


class RestaurantDescriptionForm(forms.ModelForm):
    content_type = forms.CharField(initial='description', widget=forms.HiddenInput())
    class Meta:
        model = Content
        fields = ['content_type', 'title', 'text']
        required = ['text', 'title']
        labels = {
            "text": "Текст",
            "title": "Название",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RestaurantHistoryForm(forms.ModelForm):
    content_type = forms.CharField(initial='history', widget=forms.HiddenInput())

    class Meta:
        model = Content
        fields = ['content_type', 'title', 'text', 'image']
        required = ['text', 'image', 'title']
        exclude = ['video']
        labels = {
            "text": "Текст",
            "title": "Название",
            "image": "Фото основателя",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image is not None:
            valid_extensions = ['.jpg', '.jpeg', '.png']
            extension = os.path.splitext(image.name)[1].lower()
            if extension not in valid_extensions:
                raise ValidationError(f'Недопустимый формат файла, разрешены форматы: {valid_extensions}')

            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError('Файл слишком большой. Максимальный размер 5 Мб')
            return image


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

        labels = {
            'title': 'Название услуги',
            'description': 'Описание услуги',
            'image': 'Изображение',
            'price': 'Стоимость услуги',
            'is_active': 'Активна',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image is not None:
            valid_extensions = ['.jpg', '.jpeg', '.png']
            extension = os.path.splitext(image.name)[1].lower()
            if extension not in valid_extensions:
                raise ValidationError(f'Недопустимый формат файла, разрешены форматы: {valid_extensions}')

            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError('Файл слишком большой. Максимальный размер 5 Мб')
            return image


class RestaurantMissionForm(forms.ModelForm):
    content_type = forms.CharField(initial='mission', widget=forms.HiddenInput())

    class Meta:
        model = Content
        fields = ['content_type', 'title', 'text']
        required = ['text', 'title']
        exclude = ['video']
        labels = {
            "text": "Текст",
            "title": "Название",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['mobile_phone_number', 'phone_number', 'email', 'city', 'address', 'subway', 'vk', 'tg']
        required = ['mobile_phone_number', 'phone_number', 'email', 'city', 'address']
        labels = {
            'mobile_phone_number': 'Мобильный телефон',
            'phone_number': 'Телефон',
            'email': 'Email',
            'city': 'Город',
            'address': 'Адрес',
            'subway': 'Станция метро',
            'vk': 'VK',
            'tg': 'Telegram'
        }
        widgets = {
            'mobile_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'subway': forms.TextInput(attrs={'class': 'form-control'}),
            'vk': forms.TextInput(attrs={'class': 'form-control'}),
            'tg': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChiefForm(forms.ModelForm):
    class Meta:
        model = Chief
        fields = '__all__'
        labels = {
            'name': 'Шеф',
            'photo': 'Фото шефа',
            'description': 'Описание шефа',
            'vk': 'Ссылка на VK шефа',
            'tg': 'Ссылка на Telegram канал шефа',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'vk': forms.TextInput(attrs={'class': 'form-control'}),
            'tg': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_photo(self):
            image = self.cleaned_data.get('chief_photo', False)
            if image is not None:
                valid_extensions = ['.jpg', '.jpeg', '.png']
                extension = os.path.splitext(image.name)[1].lower()
                if extension not in valid_extensions:
                    raise ValidationError(f'Недопустимый формат файла, разрешены форматы: {valid_extensions}')

                max_size = 5 * 400 * 600
                if image.size > max_size:
                    raise ValidationError('Файл слишком большой. Максимальный размер 5 Мб 400x600 px')
                return image


class SousChefForm(forms.ModelForm):
    class Meta:
        model = SousChef
        fields = '__all__'
        labels = {
            'name': 'Су-шеф',
            'photo': 'Фото су-шефа',
            'description': 'Описание су-шефа',
            'vk': 'Ссылка на VK су-шефа',
            'tg': 'Ссылка на Telegram канал су-шефа',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'vk': forms.TextInput(attrs={'class': 'form-control'}),
            'tg': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_photo(self):
            image = self.cleaned_data.get('chief_photo', False)
            if image is not None:
                valid_extensions = ['.jpg', '.jpeg', '.png']
                extension = os.path.splitext(image.name)[1].lower()
                if extension not in valid_extensions:
                    raise ValidationError(f'Недопустимый формат файла, разрешены форматы: {valid_extensions}')

                max_size = 5 * 400 * 600
                if image.size > max_size:
                    raise ValidationError('Файл слишком большой. Максимальный размер 5 Мб 400x600 px')
                return image


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        labels = {
            'description': 'Описание команды',
            'photo': 'Фото команды'
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

        def clean_photo(self):
            image = self.cleaned_data.get('team_photo', False)
            if image is not None:
                valid_extensions = ['.jpg', '.jpeg', '.png']
                extension = os.path.splitext(image.name)[1].lower()
                if extension not in valid_extensions:
                    raise ValidationError(f'Недопустимый формат файла, разрешены форматы: {valid_extensions}')

                max_size = 5 * 1000 * 400
                if image.size > max_size:
                    raise ValidationError('Файл слишком большой. Максимальный размер 5 Мб 1000x400 px')
                return image

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['first_name', 'last_name', 'email', 'phone', 'text', 'image']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'text': 'Сообщение',
            'image': 'Изображение'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Напишите нам все, что хотите сказать.'}),
        }

        def clean_image(self):
            image = self.cleaned_data.get('image', False)
            if image is not None:
                valid_extensions = ['.jpg', '.jpeg', '.png']
                extension = os.path.splitext(image.name)[1].lower()
                if extension not in valid_extensions:
                    raise ValidationError(f'Недопустимый формат файла, разрешены форматы: {valid_extensions}')

                max_size = 5 * 1024 * 1024
                if image.size > max_size:
                    raise ValidationError('Файл слишком большой. Максимальный размер 5 Мб')
                return image