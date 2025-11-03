from django.http import HttpResponse
from django.shortcuts import render
from .models import Book,Student
from django.db.models import Q,Count,Sum,Min,Max,Avg
def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]


def index(request):
      return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links(request):
     return render(request , "bookmodule/links.html")

def formatting(request):
    return render(request, "bookmodule/formatting.html")

def listing(request):
    return render(request, "bookmodule/listing.html")

def tables(request):
    return render(request, "bookmodule/tables.html")

#def search(request):
#    return render(request,"bookmodule/search.html")

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})
    return render(request,"bookmodule/search.html")
         
def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='a') 
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})


def lookup_query(request):
    mybooks=books=Book.objects.filter(author__isnull =
False).filter(title__icontains='and').filter(edition__gte = 2).exclude(price__lte = 10)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task1(request):
    mybooks = Book.objects.filter(Q(price__lte = 80))
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def task2(request):
    mybooks = Book.objects.filter(Q(edition__gt = 3)& (Q(title__contains = "Qu")|Q(author__contains = "Qu")))
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def task3(request):
    mybooks = Book.objects.filter(~Q(edition__gt = 3)& (~Q(title__contains = "qu")|~Q(author__contains = "qu")))
    return render(request , "bookmodule/bookList.html", {'books': mybooks})


def task4(request):
    mybooks = Book.objects.filter().order_by('title')
    return render(request , "bookmodule/bookList.html", {'books': mybooks})

def task5(request):
    stat =  Book.objects.aggregate(count = Count("id"),total = Sum('price',default=0),avg = Avg('price',default=0),min= Min('price',default=0),max=Max('price',default=0))
    print(stat)
    return render(request,"bookmodule/book_Stat.html",{'stat':stat})

def task7(request):
    data = Student.objects.values('address__city').annotate(count=Count('id'))
    return render(request, "bookmodule/student_city.html", {'data': data})

# def index(request):
#     name = request.GET.get("name") or "world!"
#     return render(request,"bookmodule/index.html", {"name": name})


# def index2(request, val1):
#     if not isinstance(val1, (int, float)):
#         return HttpResponse("error, expected val1 to be integer")
#     return HttpResponse(f"value1 = {val1}")


# def viewbook(request, bookId):
# # assume that we have the following books somewhere (e.g. database)
#     book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
#     book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
#     targetBook = None
#     if book1['id'] == bookId: targetBook = book1
#     if book2['id'] == bookId: targetBook = book2
#     context = {'book':targetBook} # book is the variable name accessible by the template
#     return render(request, 'bookmodule/show.html', context)