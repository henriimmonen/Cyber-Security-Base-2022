# Cyber-security-base-2022

This project is based on Django and presents five different security threats from the [2021 OWASP top ten list](https://owasp.org/www-project-top-ten/). 
The application is a note app, which is essentially your private post-it note collection. 

## Using note app
Users need to register an account with a unique username, email and password. 
After that you can add notes to yourself, which are seen in the index page in chronological order. 
If you click on the note header, you’re taken to a page where you can see the details of that particular note.

### Flaw 1: Broken access control [A01:2021](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
#### Problem: Users are able to see each others notes by typing note id's to urls.
[Link to the problem](https://github.com/henriimmonen/Cyber-security-base-2022/blob/2fd2073f18eb6ee22026fbac538b94715a2a9d92/pages/views.py#L69)

```
def one_note(request, note_id):
    note = get_object_or_404(Note, pk = note_id)
    return render(request, 'pages/text.html', {'note': note})
```
This problem is based on uncontrolled url-mapping. The app doesn't check whether the user has a right to view the requested note or not.

##### Fix:
Add this block of code to one_note function. It checks requested note's author and returns the note only if the author matches with ```request.user```.
Otherwise it redirects to index page.
```
def one_note(request, note_id):
    try:
        note = Note.objects.get(id = note_id)
        if note.author == request.user:
            return render(request, 'pages/text.html', {'note': note})
        return redirect('/')
    except Note.DoesNotExist:
        return redirect('/')
```

### Flaw 2: Cryptographic failures [A02:2021](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
#### Problem: Plain text data in database isn't encrypted.
[Link to the problem](https://github.com/henriimmonen/Cyber-security-base-2022/blob/93fd981b8b33f276506d0cb1fca60cf25190493d/pages/models.py#L15)
In todays world data safety and integrity gets more attention through GDPR and other regulations. This is a welcome change and it affects how we use, store and handle data. Because of this, every step that is possible in order to cover sensitive data, should be taken.

Noteapp has a model called UserProfile, which stores an address for the user. This model could hold other sensitive user information with a small modification. So in case of database theft or other similar attack directed towards the database, all address information would be in plain text for the attacker to use as they wish. Something should be done about this.

```
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField('username', max_length=50)
    address = models.CharField('address', max_length=200, null=True)
```

#### Fix:
To fix this, we use django-cryptography module and import encryption function to our aid. 
If the module is not installed, you can install it by running the following command in the projects root folder ```pip install django-cryptography```.

Then we import encrypt.
```
from django_cryptography.fields import encrypt
```
After this, the encryption is quite simple:
```address = encrypt(models.CharField('address', max_length=200, null=True))```
This can be added to every field that you want to encrypt. This is enough for us at the moment.

### Flaw 3: Injection [A03:2021](https://owasp.org/Top10/A03_2021-Injection/)
### Flaw 4: Security misconfiguration [A05:2021](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
### Flaw 5: 
