from django.forms import ModelForm, HiddenInput, RadioSelect

from litreview.models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        # exclude = ['user']
        fields = "__all__"
        widgets = {"user": HiddenInput}


class ReviewForm(ModelForm):
    # rating = ChoiceField()
    class Meta:
        model = Review
        # exclude = ['user', ]
        fields = "__all__"
        widgets = {"user": HiddenInput, "ticket": HiddenInput, "rating": RadioSelect}
