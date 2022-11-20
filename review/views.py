from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from forms import TicketForm, ReviewForm, SubsForm
from models import Ticket, Review, UserFollows
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
import itertools


# Create your views here.


@login_required
def flux(requests):
    return render(requests, "review/flux.html")


class CreateTicket(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "review/create_ticket.html"
    success_url = reverse_lazy("flux")

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        return super().form_valid(form_class)


class UpdateTicket(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "review/update_ticket.html"
    success_url = reverse_lazy("posts")


class DeleteTicket(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "review/delete_object.html"
    success_url = reverse_lazy("posts")


@login_required
def create_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
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


class UpdateReview(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review/update_review.html"
    success_url = reverse_lazy("posts")


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "review/delete_object.html"
    success_url = reverse_lazy("posts")


class ViewPosts(LoginRequiredMixin, ListView):
    template_name = "review/posts.html"
    paginate_by = 10

    def get_queryset(self):
        tickets = Ticket.objects.filter(user=self.request.user)
        reviews = Review.objects.filter(user=self.request.user)
        return sorted(
            itertools.chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True,
        )


class Subscription(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = SubsForm
    template_name = "review/subscription.html"
    success_url = reverse_lazy("flux")

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        return super().form_valid(form_class)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["follows"] = UserFollows.objects.filter(user=self.request.user)
        return context



class ViewFlux(LoginRequiredMixin, ListView):
    template_name = "review/flux.html"
    paginate_by = 10

    def get_queryset(self):
        tickets = Ticket.objects.filter(
            user__in=UserFollows.objects.filter(user=self.request.user).values_list(
                "followed_user"
            )
        )
        reviews = Review.objects.filter(
            user__in=UserFollows.objects.filter(user=self.request.user).values_list(
                "followed_user"
            )
        )
        return sorted(
            itertools.chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True,
        )
