from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy as rl, reverse
from django.views.generic import *
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from read.models import HistoryRecord
from backend.models import Book


def profile_ck(request):
    get_profile = UserProfile.objects.filter(user_id=int(request.user.id))
    if get_profile.exists():
        return HttpResponseRedirect(reverse('profile:home'))
    else:
        return HttpResponseRedirect(reverse('profile:create-profile'))


class ProfileHome(ListView):
    template_name = 'member/main.html'
    model = HistoryRecord
    context_object_name = 'history'
    ordering = ['-pk']
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileHome, self).get_context_data(*args, **kwargs)
        userprofile = UserProfile.objects.get(user_id=self.request.user.id)
        new_book = Book.objects.order_by('-pk')[:3]

        context['userprofile'] = userprofile
        context['new_book'] = new_book
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileHome, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
def profile_home(request):
    userprofile_ = UserProfile.objects.filter(user_id=request.user.id)
    if userprofile_.exists():
        userprofile = UserProfile.objects.get(user_id=request.user)
    else:
        return HttpResponseRedirect(reverse('profile:create-profile'))

    history = HistoryRecord.objects.filter(user_id=request.user.id)
    history = history.order_by('-pk')

    context = {
        'userprofile': userprofile,
        'user_': request.user,
        'history': history,
    }
    return render(request, 'member/main.html', context)


class CreateProfile(CreateView):
    model = UserProfile
    template_name = 'member/create.html'
    form_class = CreateProfileForm
    success_url = rl('profile:home')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        a = super(CreateProfile, self).form_valid(form)
        b = HttpResponseRedirect(self.get_success_url())
        return a and b

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        get_profile = UserProfile.objects.filter(user_id=self.request.user)
        if get_profile.exists():
            return redirect('profile:home')
        else:
            return super(CreateProfile, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return self.template_name


class UpdateProfile(UpdateView):
    model = UserProfile
    template_name = 'member/update.html'
    form_class = CreateProfileForm
    success_url = rl('profile:home')

    def form_valid(self, form):
        form.instance.profile_image = self.request.POST.get('profile_image')
        a = super(UpdateProfile, self).form_valid(form)
        b = HttpResponseRedirect(redirect(self.get_success_url()))
        return a, b

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateProfile, self).dispatch(request, *args, **kwargs)
