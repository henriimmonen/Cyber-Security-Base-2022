# Cyber-security-base-2022

This project is based on Django and presents five different security threats from the [2021 OWASP top ten list](https://owasp.org/www-project-top-ten/). 
The application is a note app, which is essentially your private post-it note collection. 

## Using note app
Users need to register an account with a unique username, email and password. 
After that you can add notes to yourself, which are seen in the index page in chronological order. 
If you click on the note header, you’re taken to a page where you can see the details of that particular note.

### Flaw 1: Broken access control [A01:2021](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
##### Problem: Users are able to see each others notes by typing note id's to urls.
```note = get_object_or_404(Note, pk = note_id)```
[Link](https://github.com/henriimmonen/Cyber-security-base-2022/blob/2fd2073f18eb6ee22026fbac538b94715a2a9d92/pages/views.py#L69)
This problem is based on uncontrolled url-mapping. The app doesn't check whether the user has the right to view the requested note or not.

###### Fix:
Adding this block of code to one_note function provides checking of notes author and returns the note only if the author matches with request.user.
```    try:
        note = Note.objects.get(id = note_id)
        if note.author == request.user:
            return render(request, 'pages/text.html', {'note': note})
        return redirect('/')
    except Note.DoesNotExist:
        return redirect('/')
```

### Flaw 2: Cryptographic failures [A02:2021](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
### Flaw 3: Injection [A03:2021](https://owasp.org/Top10/A03_2021-Injection/)
### Flaw 4: Security misconfiguration [A05:2021](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
### Flaw 5: 
