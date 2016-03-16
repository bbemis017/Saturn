from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def create_summary(request):
	# TODO: Here read request.POST for necessary informations
	print request.POST


@login_required
def edit_summary(request):
	# TODO: edit
	print request.POST