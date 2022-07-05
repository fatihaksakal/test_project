from django.shortcuts import render


# Create your views here.

def customerRegister(request, uu_id):
    # try:
    #     uid = force_text(urlsafe_base64_decode(uidb64))
    #     user = Newuser.objects.get(pk=uid)
    # except(TypeError, ValueError, OverflowError, Newuser.DoesNotExist):
    #     user = None
    # if user is not None and user.is_email_verified == 0 and account_activation_token.check_token(user, token):
    #     user.is_email_verified = True
    #     user.save()
    #     current_site = get_current_site(request)
    #     mail_subject = 'This account is awaiting your approval.'
    #     message = render_to_string('admin_active.html', {
    #         'user': user,
    #         'domain': current_site.domain,
    #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #         'token': account_activation_token.make_token(user),
    #     })
    #     to_email = settings.EMAIL_HOST_USER
    #     email = EmailMessage(
    #         mail_subject, message, to=[to_email]
    #     )
    #     email.send()
    #     messages.success(request,
    #                      "Email verification successfully completed. You can login after admin approval. We will send a notification e-mail after the admin approval.")
    #     return redirect(reverse('index'))
    # else:
    #     messages.info(request, "Activation link is invalid! Please wait for admin approval.")
    #     return redirect(reverse('index'))
    pass