from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.conf import settings
from itertools import chain
from . import models
from . import forms


class BlockOtherUsers(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        if self.request.user:
            return obj.user == self.request.user
        return False


class CreateTicket(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketForm
    template_name = "review/create_ticket.jinja2"
    success_url = reverse_lazy("flux")

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        return super().form_valid(form_class)


@login_required
def ticket_response(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review = forms.ReviewForm()
    follows = models.UserFollows.objects.filter(user=request.user, followed_user= ticket.user)
    ticket_reviews = models.Review.objects.filter(ticket_id= ticket_id)
    if follows.exists() and not ticket_reviews.exists():
        if request.method == "POST":
            review = forms.ReviewForm(request.POST)
            if review.is_valid():
                review = review.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                ticket.answered = True
                review.save()
                ticket.save()
                return redirect(settings.LOGIN_REDIRECT_URL)
        context = {
            "ticket": ticket,
            "review": review,
        }
        return render(
            request,
            "review/partials/ticket_response_snippet.jinja2",
            context=context)
    else:
        return redirect(settings.LOGIN_REDIRECT_URL)


class UpdateTicket(LoginRequiredMixin, BlockOtherUsers, UpdateView):
    model = models.Ticket
    form_class = forms.TicketForm
    template_name = "review/update_ticket.jinja2"
    success_url = reverse_lazy("posts")


class DeleteTicket(LoginRequiredMixin, BlockOtherUsers, DeleteView):
    model = models.Ticket
    template_name = "review/delete_object.jinja2"
    success_url = reverse_lazy("posts")


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
            ticket.answered = True
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
    return render(request, "review/create_review.jinja2", context=context)


class UpdateReview(LoginRequiredMixin, BlockOtherUsers, UpdateView):
    model = models.Review
    form_class = forms.ReviewForm
    template_name = "review/update_review.jinja2"
    success_url = reverse_lazy("posts")


class DeleteReview(LoginRequiredMixin, BlockOtherUsers, DeleteView):
    model = models.Review
    template_name = "review/delete_object.jinja2"
    success_url = reverse_lazy("posts")


class ViewPosts(LoginRequiredMixin, ListView):
    template_name = "review/posts.jinja2"
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.select_related("user").filter(
            user=self.request.user
        )

        reviews = models.Review.objects.select_related("user").filter(
            user=self.request.user
        )

        return sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True,
        )


class Subscription(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.SubsForm
    template_name = "review/subscription.jinja2"
    success_url = reverse_lazy("subscription")

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        return super().form_valid(form_class)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["follows"] = (
            models.UserFollows.objects.select_related("followed_user")
            .filter(user=self.request.user)
            .order_by("followed_user__username")
        )
        context["followers"] = (
            models.UserFollows.objects.select_related("followed_user")
            .filter(followed_user=self.request.user)
            .order_by("user__username")
        )

        return context

    def get_form_kwargs(self, *args, **kwargs):
        return {**super().get_form_kwargs(*args, **kwargs),
                "user": self.request.user}


class DeleteSuscription(LoginRequiredMixin, BlockOtherUsers, DeleteView):
    model = models.UserFollows
    template_name = "review/delete_object.jinja2"
    success_url = reverse_lazy("subscription")


class ViewFlux(LoginRequiredMixin, ListView):
    template_name = "review/flux.jinja2"
    paginate_by = 10

    def get_queryset(self):
        followed_users = models.UserFollows.objects.filter(
            user=self.request.user
        ).values_list("followed_user")
        followed_user_tickets = models.Ticket.objects.select_related(
            "user").filter(user__in=followed_users)

        followed_user_reviews = models.Review.objects.select_related(
            "user").filter(user__in=followed_users)

        my_tickets = models.Ticket.objects.select_related("user").filter(
            user=self.request.user
        )
        my_reviews = models.Review.objects.select_related("user").filter(
            user=self.request.user
        )

        reviews_user_tickets = (
            models.Review.objects.filter(ticket__in=my_tickets)
            .select_related("user")
            .exclude(user=self.request.user)
        )
        return sorted(
            chain(
                followed_user_tickets,
                followed_user_reviews,
                my_tickets,
                my_reviews,
                reviews_user_tickets,
            ),
            key=lambda post: post.time_created,
            reverse=True,
        )
