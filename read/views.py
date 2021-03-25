from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from backend.models import Book, Category
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404, FileResponse
from django.urls import reverse, reverse_lazy
from .forms import *
from django.db.models import Count, Q
from members.models import UserProfile
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
from django.core.files.storage import FileSystemStorage
from django.views.decorators.clickjacking import xframe_options_sameorigin


class AllBooksList(TemplateView):
    template_name = 'read/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AllBooksList, self).get_context_data(*args, **kwargs)
        fav_book = Book.objects.all().order_by('likes')[:6]
        book_total = Book.objects.all().count()
        member = User.objects.all().count()
        category = Category.objects.all().count()

        context['fav_books'] = fav_book
        context['book_total'] = book_total
        context['member'] = member
        context['category'] = category
        return context


# def like_view(request, pk):
#     book = get_object_or_404(Book, id=request.POST.get('book_id'))
#     current_score = book.current_rate()
#     rated = False
#     # Delete rating the book
#     if book.user_rating.filter(id=request.user.id).exists():
#         pass
#     else:
#         book.user_rating.add(request.user)
#         current_score += int(request.POST.get('rating_point'))
#         rated = True
#
#     return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))


class BookDetailView(DetailView):
    template_name = 'read/details.html'
    # template_name = 'read/base1.html'
    query_pk_and_slug = True
    slug_url_kwarg = 'link'
    slug_field = 'link'
    model = Book

    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)
        category = Category.objects.all()
        tile = Book.objects.get(link=self.kwargs['link'])
        profile_ = UserProfile.objects.filter(user_id=Book.objects.get(pk=tile.pk).uploader)
        if profile_ is not None:
            profile = UserProfile.objects.get(user_id=Book.objects.get(pk=tile.pk).uploader)
            context['profile'] = profile
        else:
            pass
        stuff = get_object_or_404(Book, link=self.kwargs['link'])
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['category'] = category
        context['liked'] = liked
        return context


class AddComment(CreateView):
    model = Comment
    form_class = AddCommentForms
    template_name = 'read/add-comment.html'
    query_pk_and_slug = True
    slug_field = 'link'
    slug_url_kwarg = 'link'

    def get_success_url(self):
        return reverse('read:detail', args=[str(self.kwargs['link'])])

    def form_valid(self, form):
        pk = Book.objects.get(link=self.kwargs['link'])
        form.instance.book_id = pk.pk
        form.instance.name_id = self.request.user.id
        return super().form_valid(form) and HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required(login_url="/accounts/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(AddComment, self).dispatch(request, *args, **kwargs)


# def CategorySearch(req, cats):
#     cate = Book.objects.filter(category=cats.replace('-', ' '))
#     con = {
#         'cats': cats.replace('-', ' ').title(),
#         'category_posts': cate
#     }
#     return render(req, '', con)


class AllBookList(ListView):
    model = Book
    template_name = 'read/list.html'
    paginate_by = 6
    ordering = ['-pk']

    def get_queryset(self):
        qq = self.request.GET.get('q')
        ss = self.request.GET.get('s')
        if qq is not None:
            if ss is not None:
                object_list = Book.objects.filter(
                    Q(title__icontains=qq) | Q(link__icontains=qq) | Q(description__icontains=qq), category__in=ss
                )
            else:
                object_list = Book.objects.filter(
                    Q(title__icontains=qq) | Q(link__icontains=qq) | Q(description__icontains=qq)
                ).order_by('-pk')
        else:
            object_list = Book.objects.all().order_by('-pk')

        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super(AllBookList, self).get_context_data(*args, **kwargs)
        fav_book = Book.objects.all().order_by('likes')[:4]
        new_book = Book.objects.all().order_by('-pk')[:1]
        cat = Category.objects.all()

        context['category'] = cat
        context['new_book'] = new_book
        context['fav_books'] = fav_book
        return context


def like_view(request, link):
    book = get_object_or_404(Book, link=link)
    like = book.likes.filter(id=request.user.id)
    liked = False
    print(book)

    if like.exists():
        book.likes.remove(request.user)
        liked = False
    else:
        book.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('read:detail', args=[link]))


class PdfView(DetailView):
    template_name = 'read/pdf_viewer.html'
    model = Book
    query_pk_and_slug = True
    slug_url_kwarg = 'link'
    slug_field = 'link'

    def get_context_data(self, *args, **kwargs):
        context = super(PdfView, self).get_context_data(*args, **kwargs)
        book = Book.objects.get(link=self.kwargs['link'])

        context['book'] = book
        return context

    @method_decorator(xframe_options_sameorigin)
    def dispatch(self, request, *args, **kwargs):
        return super(PdfView, self).dispatch(request, *args, **kwargs)


def insert_to_history(request, link):
    user_ = request.user
    get_book = get_object_or_404(Book, link=link)
    if user_.is_authenticated:
        history = HistoryRecord(user_id=request.user.id, url=str(link), book_id=get_book.id)
        history.save()
    link = str(link)
    return HttpResponseRedirect(reverse('read:book-view', args=[link]))


# class PdfView(PDFTemplateResponseMixin, DetailView):
#     template_name = 'read/pdf_viewer.html'
#     model = Book
#     context_object_name = 'book'
#     query_pk_and_slug = True
#     slug_url_kwarg = 'link'
#     slug_field = 'link'


# def url(request, path):
#     fs = FileSystemStorage()
#     filename = str(file)
#     if fs.exists(filename):
#         with fs.open(filename) as pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename=' + filename
#             return response
#     else:
#         return HttpResponseNotFound("sorry we couldn find the pdf that you looking for")
#     path = str(path)
#     try:
#         return FileResponse(open(path, 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise
#
#
# def pdf_view(request, link):
#     book = get_object_or_404(Book, link=link)
#     context = {
#         'book': book,
#     }
#     return render(request, 'read/pdf_viewer.html', context)


def maps_view(request):
    return render(request, 'read/maps.html')


class ShowProfileUploaderProfile(TemplateView):
    template_name = 'read/profile_viewer.html'
    query_pk_and_slug = True
    slug_url_kwarg = 'link'
    slug_field = 'link'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfileUploaderProfile, self).get_context_data(*args, **kwargs)
        get_from_link = get_object_or_404(Book, link=self.kwargs['link'])
        userprofile = get_object_or_404(UserProfile, user_id=get_from_link.uploader)
        books = Book.objects.filter(uploader_id=userprofile.user)

        context['book'] = books
        context['userprofile'] = userprofile
        return context
