from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        # Admin sees all, User sees created by them
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(created_by=user).order_by('-created_at')

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        user = self.request.user
        ticket = self.object
        context['can_edit'] = (user == ticket.created_by or user == ticket.assigned_to or user.role == 'ADMIN' or user.is_superuser)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = self.object
            comment.author = request.user
            comment.save()
            return redirect('ticket_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(comment_form=form))

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

    def get_queryset(self):
        # Allow editing if Creator, Assignee, or Admin
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Ticket.objects.all()
        return Ticket.objects.filter(models.Q(created_by=user) | models.Q(assigned_to=user))

    def get_form_class(self):
        # Optional: Use a differnt form if we want to restrict fields for non-admins?
        # For now, we will use the same form and control field visibility in template or init
        return TicketForm
