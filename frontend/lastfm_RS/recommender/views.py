from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import RegisterForm
# Create your views here.


def index(request):
    """View function for home page of site."""

    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    """

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        # context={'num_books': num_books, 'num_instances': num_instances,
        #          'num_instances_available': num_instances_available, 'num_authors': num_authors,
        #          'num_visits': num_visits},
        context={'num_visits': num_visits},
    )


def register(request):
    """View function for registration form."""

    if request.method == 'POST':
        # Registration form instance
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                return render(request, 'registration/registration_complete.html')

    else:
        form = RegisterForm()
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'registration/registration_form.html',
        context={'form': form},
    )
