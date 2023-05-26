import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DeleteView
from booklet.models import Booklet
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.views import LogoutView

class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('booklet_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})


class SignupPageView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists.'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')


class BookletListView(LoginRequiredMixin, ListView):
    model = Booklet
    template_name = 'booklet_list.html'
    context_object_name = 'booklets'

    def get_queryset(self):
        
        return Booklet.objects.all()
        


class BookletUploadView(LoginRequiredMixin, CreateView):
    model = Booklet
    fields = ['title', 'file']
    template_name = 'booklet_upload.html'
    success_url = reverse_lazy('booklet_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class BookletDeleteView(LoginRequiredMixin, DeleteView):
    model = Booklet
    template_name = 'booklet_confirm_delete.html'
    success_url = reverse_lazy('booklet_list')


class CustomLogoutView(LogoutView):
    next_page = '/login/'  
    def dispatch(self, request, *args, **kwargs):
        return redirect('login')

def download_booklet(request, pk):
    booklet = get_object_or_404(Booklet, pk=pk)
    file_path = booklet.pdf_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

class ViewBookletView(View):
    def get(self, request, pk):
        booklet = get_object_or_404(Booklet, pk=pk)
        return render(request, 'view_booklet.html', {'booklet': booklet})