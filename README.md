# Cyber-security-base-2022

This project is based on Django and presents five different security threats from the [2021 OWASP top ten list](https://owasp.org/www-project-top-ten/). 
The application is a note app, which is essentially your private post-it note collection. 

## Using note app
Users need to register an account with a unique username, email and password. 
After that you can add notes to yourself, which are seen in the index page in chronological order. 
If you click on the note header, you’re taken to a page where you can see the details of that particular note.

### Flaw 1: Broken access control [A01:2021](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
#### Problem: Users are able to see each others notes by typing note id's to urls.
[Link to the problem](https://github.com/henriimmonen/Cyber-security-base-2022/blob/394702848a32385ff6c9a670ada751feb6d99fd9/pages/views.py#L71)

```
def one_note(request, note_id):
    try:
        note = Note.objects.get(pk = note_id)
        return render(request, 'pages/text.html', {'note': note})
    except Note.DoesNotExist:
        return redirect('/')
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

In todays world, data safety and integrity get more attention through GDPR and other regulations. This is a welcome change and it affects how we use, store and handle data. Because of this every step that is possible to make, in order to cover sensitive data, should be taken.

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
#### Problem: Noteapp accepts unsanitized user input without HTML escaping.  
[Link to the problem](https://github.com/henriimmonen/Cyber-security-base-2022/blob/1aed5f3f6b4320e2ede6d6e462b5a699d0778e4b/pages/templates/pages/profile.html#L7)  
Django uses automatic HTML escaping as a security feature. You can avoid using this by marking certain inputs as safe in the HTML template ```<h2>Address: {{ address | safe }}</h2>```  
This allows potential cross site scripting attacks, for example if one would enter ```<script>alert(document.cookie);</script> you would be able to see the cookie used. This itself is not a very harmful attack, but it could be developed further.  

#### Fix: 
By not marking user input as safe we can avoid some of the problems. In this case the address is not used in anything other than showing it to the user so it's simple. Instead of marking the input as safe, we write ```<h2>Address: {{ address }}</h2>```.

### Flaw 4: Identification and authentication failures [A07:2021](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
#### Problem: Noteapp admin is run on generic username/password combination that is easy to predict.
#### Fix: 
This problem is quite easy to fix. Administrator password provided in the database is admin123 (username is admin). By changing this, the security of the app is instantly better. Admin passwords are sought after by cyber criminals and by simple and fast password change you make their job more difficult. It is considered a good practice to change administrator and admin passwords from time to time and not use the same password on multiple accounts/servers/etc. [Why administrators should change passwords from time to time](https://blog.netwrix.com/2014/06/17/why-you-need-to-ensure-administrators-change-passwords-regularly/).

### Flaw 5: Security logging and monitoring failures [A09:2021](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
#### Problem: Noteapp doesn't log any critical information that could be useful to detect and respond to breaches.
Major advantage of security logging and monitoring is that it gives tools to respond to breaches. It also gives us documentation about possible attacks for forensics. This is very important in order to safely manage an app. On the other hand, you need to be aware what kind of information is logged and how it is stored, who has access to it and so on.  

#### Fix:  
This logging is a simple start, which gives us some type of information of possible attacks and suspicious activity. By setting logger level to 'WARNING' we get information describing minor problems and higher. Other way to go would have been to set it to 'DEBUG' or 'INFO' but as 'DEBUG' shows information about database queries etc so we compromise between less logging and dealing with more sensitive data.

Insert this to the end of settings.py file 
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```
#### Important
If you can't get anything logged as the level is 'WARNING', change it to 'DEBUG' and you get more logging information. To view the logging information, you can print the text inside the file to terminal from the project root by typing ```cat debug.log```.
