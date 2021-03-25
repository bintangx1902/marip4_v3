from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from .models import Book
from .forms import UploadBookForm, UpdateUploadedBook
from django.db.models import Q as __
import os
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from members.models import UserProfile
from .utils import staff_required

link = 'link'


@login_required(login_url="/accounts/login/")
def upload_check(request):
    profile_ = UserProfile.objects.filter(user_id=request.user.id)
    # print(profile_)
    if not profile_:
        # if user had create their profile
        return redirect('profile:create-profile')
    else:
        # if not create
        return redirect('my:upload-a-book')


def redirect_check(request):
    book = Book.objects.filter(uploader_id=request.user.id).count()
    if book != 0:
        return redirect('my:book-list')
    else:
        return redirect('my:book-check')


class BookListUploaded(ListView):
    model = Book
    template_name = 'backend/book-list.html'
    paginate_by = 10
    ordering = ['-id']

    def get_queryset(self):
        qq = self.request.GET.get('q')
        book_total = Book.objects.filter(uploader=self.request.user.id)

        if book_total is not 0:
            if qq is not None:
                object_list = Book.objects.filter(
                    __(title__icontains=qq) | __(author__icontains=qq) |
                    __(description__icontains=qq) | __(link__icontains=qq)
                )
                object_list.filter(uploader=self.request.user.id)
            else:
                object_list = Book.objects.filter(uploader=self.request.user.id)
        else:
            return redirect('my:book-check')

        return object_list

    @method_decorator(login_required(login_url="/accounts/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(BookListUploaded, self).dispatch(request, *args, **kwargs)


class BookDetail(DetailView):
    model = Book
    template_name = 'backend/book-detail.html'
    query_pk_and_slug = True
    slug_field = link
    slug_url_kwarg = link

    def get_context_data(self, *args, **kwargs):
        context = super(BookDetail, self).get_context_data(*args, **kwargs)

        return context

    @method_decorator(login_required(login_url="/accounts/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(BookDetail, self).dispatch(request, *args, **kwargs)


@login_required(login_url="/accounts/login/")
def download(req, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/file')
            response['Content-Dispotition'] = 'inline;filenam=' + os.path.basename(file_path)
            return response
    raise Http404


class UploadBook(CreateView):
    model = Book
    form_class = UploadBookForm
    template_name = 'backend/upload.html'
    success_url = reverse_lazy('my:book-list')

    def form_valid(self, form):
        form.instance.uploader_id = self.request.user.id
        link_ = str(self.request.POST.get('title'))
        str_id = str(self.request.user.id)
        link_ = str_id + '_' + link_
        link_ = link_.replace(" ", "-")
        form.instance.link = link_

        return super(UploadBook, self).form_valid(form) and HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required(login_url="/accounts/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(UploadBook, self).dispatch(request, *args, **kwargs)


class UpdateBook(UpdateView):
    model = Book
    form_class = UpdateUploadedBook
    template_name = 'backend/update.html'
    query_pk_and_slug = True
    slug_field = link
    slug_url_kwarg = link

    def get_success_url(self):
        return reverse('my:book-detail', args=[str(self.kwargs['link'])])

    def form_valid(self, form):
        a = super().form_valid(form)
        return a

    @method_decorator(login_required(login_url="/accounts/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBook, self).dispatch(request, *args, **kwargs)


class BookDelete(DeleteView):
    model = Book
    template_name = 'backend/delete.html'
    query_pk_and_slug = True
    slug_field = link
    slug_url_kwarg = link
    success_url = reverse_lazy('my:book-list')

    def get_success_url(self):
        return self.success_url.format(**self.object.__dict__)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(BookDelete, self).dispatch(request, *args, **kwargs)
