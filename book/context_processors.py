from .models import Genre, Type, ReadingList

def get_genres(request):
    genres = Genre.objects.all()
    return dict(genres=genres)

def get_typies(request):
    typies = Type.objects.all()
    return dict(typies=typies)

def get_readinglist(request):
    reading_list = ReadingList.objects.all()
    return dict(reading_list=reading_list)