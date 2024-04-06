from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    DetailView,
    RedirectView,
    UpdateView,
)

from django.shortcuts import render
from django.core.mail import EmailMessage
from .formss import ContactForm


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These Next Two Lines Tell the View to Index
    #   Lookups by Username
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name",
    ]

    # We already imported user in the View code above,
    #   remember?
    model = User

    # Send the User Back to Their Own Page after a
    #   successful Update
    def get_success_url(self):
        return reverse(
            "users:detail",
            kwargs={'username': self.request.user.username},
        )

    def get_object(self):
        # Only Get the User Record for the
        #   User Making the Request
        return User.objects.get(
            username=self.request.user.username
        )


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse(
            "users:detail",
            kwargs={"username": self.request.user.username},
        )


user_redirect_view = UserRedirectView.as_view()


def contact(request):
    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data['name']
    #         email = form.cleaned_data['email']
    #         message = form.cleaned_data['message']
    #         email_subject = f'Contact Form Submission from {name}'
    #         email_body = f'Name: {name}\nEmail: {email}\n\n{message}'
    #         email = EmailMessage(
    #             subject=email_subject,
    #             body=email_body,
    #             from_email=email, # use the user's email address entered in the form
    #             to=['2f299c540e-da0fe5@inbox.mailtrap.io'], # replace with your Mailtrap inbox email address
    #             reply_to=[email],
    #             headers={'Content-Type': 'text/plain'},
    #         )
    #         request.session['name'] = name
    #         email.send()
    #         context = {'name':name}
    #         return render(request, 'pages/contact_success.html', context)
    # else:
    form = ContactForm()
    context = {'form': form}
    return render(request, 'pages/contact.html', context )
