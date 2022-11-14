from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings
from . import forms, models
from django.views.generic import View, FormView, ListView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
# Create your views here.


@login_required
def flux(requests):
    return render(requests, "review/flux.html")


class CreateTicket(LoginRequiredMixin, FormView):
    template_name = "review/create_ticket.html"
    form_class = forms.TicketForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        return super().form_valid(form)


@login_required
def create_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "review/create_review.html", context=context)


class ViewPosts(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = "review/posts.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class UpdateTicket(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    fields = ["title", "description", "image"]
    template_name = "review/update_ticket.html"
    success_url = reverse_lazy("posts")


class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = models.Ticket
    template_name = "review/delete_object.html"
    success_url = reverse_lazy("posts")
