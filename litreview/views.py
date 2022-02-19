from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory, HiddenInput, RadioSelect
from django.db.models import Value, CharField, BooleanField, Case, When, Q
from django.core.exceptions import PermissionDenied

from itertools import chain

from litreview.forms import TicketForm, ReviewForm, TestForm
from litreview.models import User, Ticket, Review, UserFollows

### AUTH ###
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('feed')
	else:
		form = UserCreationForm()
	return render(request, 'litreview/signup.html', {'form': form})

### TICKET ###

@login_required
def create_ticket(request):
	if request.method == 'POST':
		data = request.POST.copy()
		data.update({'user': request.user})
		form = TicketForm(data, request.FILES)
		if form.is_valid():
			t = form.save()
			return redirect('feed')
	else:
		form = TicketForm()
	return render(request, 'litreview/ticket/create_ticket.html', {'form': form})

@login_required
def edit_ticket(request, ticket_id):
	ticket = Ticket.objects.get(id=ticket_id)
	if ticket.user != request.user:
		raise PermissionDenied
	if request.method == 'POST':
		data = request.POST.copy()
		data.update({'user': request.user})
		form = modelform_factory(
			Ticket,
			fields='__all__',
			# widgets={'user': HiddenInput}
		)(data, request.FILES, instance=ticket)
		if form.is_valid():
			form.save()
			return redirect('posts')
	else:
		form = modelform_factory(
			Ticket,
			exclude=['user'],
		)(instance=ticket)
	return render(
		request,
		'litreview/ticket/edit_ticket.html',
		{'form': form}
	)

@login_required
def delete_ticket(request, ticket_id):
	try:
		ticket = Ticket.objects.get(id=ticket_id)
	except:
		pass
	if ticket.user != request.user:
		raise PermissionDenied
	ticket.delete()
	return redirect('posts')

### REVIEW ###

@login_required
def create_review(request):
	ticket = request.GET.get('ticket')
	if Review.objects.filter(ticket_id=ticket):
		pass
		# redirect('review_already_exists')

	if request.method == 'POST':
		user = request.user
		data = request.POST.copy()

		if ticket:
			ticket = Ticket.objects.get(id=ticket)
		else:
			data.update({'tform-user': user})
			ticket_form = TicketForm(data, request.FILES, prefix='tform')
			if ticket_form.is_valid():
				ticket = ticket_form.save()

		if ticket:
			data.update({'rform-user': user, 'rform-ticket': ticket})
			review_form = modelform_factory(
				Review,
				fields='__all__',
				widgets={'user': HiddenInput, 'ticket': HiddenInput, 'rating': RadioSelect}
			)(data, prefix='rform')

			if review_form.is_valid():
				review_form.save()
				return redirect('feed')
			else:
				print(data.get('rform-rating'))
				return redirect('create_review')
				# return create_ticket(request, ticket.id)
	else:
		if ticket:
			ticket = Ticket.objects.get(id=ticket)
		ticket_form = TicketForm(prefix='tform')
		review_form = modelform_factory(
			Review,
			exclude=['ticket', 'user'],
			widgets={'rating': RadioSelect}
		)(prefix='rform')
	return render(
		request,
		'litreview/review/create_review.html',
		{
			'review_form': review_form,
			'ticket_form': ticket_form,
			'ticket': ticket
		}
	)

@login_required
def edit_review(request, review_id):
	review = Review.objects.get(id=review_id)
	if review.user != request.user:
		raise PermissionDenied
	if request.method == 'POST':
		data = request.POST.copy()
		data.update({'user': request.user, 'ticket': review.ticket})
		form = modelform_factory(
			Review,
			fields='__all__',
			widgets={'ticket': HiddenInput, 'rating': RadioSelect}
		)(data, request.FILES, instance=review)
		if form.is_valid():
			form.save()
			return redirect('posts')
	else:
		form = modelform_factory(
			Review,
			exclude=['ticket', 'user'],
			widgets={'rating': RadioSelect}
		)(instance=review)
	return render(
		request,
		'litreview/review/edit_review.html',
		{'ticket': review.ticket,'form': form}
	)

@login_required
def delete_review(request, review_id):
	try:
		review = Review.objects.get(id=review_id)
	except:
		pass
	if review.user != request.user:
		raise PermissionDenied
	review.delete()
	return redirect('posts')

### FEED ###

@login_required
def feed(request):
	followed_users = [
		f.followed_user for f in UserFollows.objects.filter(user=request.user)
	]
	reviews = Review.objects.all()
	answered_tickets = [r.ticket.id for r in reviews]

	tickets = (
		Ticket.objects
		.filter(user__in=[*followed_users, request.user])
		.annotate(
			content_type=Value('ticket', CharField()),
			answered=Case(
				When(id__in=answered_tickets, then=Value(True, BooleanField())),
				default=Value(False, BooleanField())
			)
		)
	)

	user_tickets = list(Ticket.objects.filter(user=request.user))
	reviews = (
		reviews
		.filter(
			Q(user__in=[*followed_users, request.user])
			| Q(ticket__in=user_tickets)
		)
		.annotate(content_type=Value('review', CharField()))
	)

	posts = sorted(
		chain(reviews, tickets), 
		key=lambda post: post.time_created, 
		reverse=True
	)
	return render(request, 'litreview/posts.html', {'posts':posts})

### POSTS ###

@login_required
def posts(request):
	user = request.user

	if request.method == 'POST':
		pass
	else:
		pass
	pass

	reviews = (
		Review.objects
		.filter(user=user)
		.annotate(content_type=Value('review', CharField()))
	)
	tickets = (
		Ticket.objects
		.filter(user=user)
		.annotate(content_type=Value('ticket', CharField()))
	)
	posts = sorted(
		chain(reviews, tickets), 
		key=lambda post: post.time_created, 
		reverse=True
	)
	return render(request, 'litreview/posts.html', {'posts': posts})

### FOLLOW ###

@login_required
def follow(request):
	user = request.user

	if request.method == 'POST':
		data = request.POST.copy()
		data.update({'user': request.user})
		form = modelform_factory(UserFollows, fields='__all__')(data)
		print(dir(form))
		if int(user.id) == int(data.get('followed_user')):
			form.add_error(None, "Cannot follow yourself")
		if form.is_valid():
			form.save()
	else:
		form = modelform_factory(UserFollows, fields=['followed_user'])

	users = UserFollows.objects.all()
	followed = [
		f.followed_user for f in users.filter(user=request.user)
	]
	followers = [
		f.user for f in users.filter(followed_user=request.user)
	]

	return render(
		request,
		'litreview/follow.html',
		{'form': form, 'followed': followed, 'followers': followers}
	)

@login_required
def unfollow(request, user_id):
	f = (
		UserFollows.objects
		.filter(user=request.user)
		.filter(followed_user=user_id)
	)
	if f:
		f.delete()
	else:
		# relationship doesn't exist, can this happen ?
		pass
	return redirect('follow')
