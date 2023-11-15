from django.core.files.storage import FileSystemStorage

class CustomStorage(FileSystemStorage):
    def url(self, name):
        return 'https://i.ibb.co/' + name
    
    def _save(self, name, content):
        return name