from django.forms import ModelForm, HiddenInput, ChoiceField, RadioSelect, TextInput, Textarea, Select

from litreview.models import User, Ticket, Review, UserFollows


class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		# exclude = ['user']
		fields = "__all__"
		widgets = {'user': HiddenInput}

class ReviewForm(ModelForm):
	# rating = ChoiceField()
	class Meta:
		model = Review
		# exclude = ['user', ]
		fields = "__all__"
		widgets = {'user': HiddenInput, 'ticket': HiddenInput, 'rating': RadioSelect}

class TestForm(ModelForm):
	class Meta:
		model = Review
		fields = "__all__"
		widgets = {
			'rating': RadioSelect()
		}
