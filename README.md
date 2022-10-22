# Cyber-security-base-2022

This project is based on Django and presents five different security threats from the [OWASP top ten list](https://owasp.org/www-project-top-ten/). 
The application is a note app, which is essentially your private post-it note collection. 

## Using note app
Users need to register an account with a unique username, email and password. 
After that you can add notes to yourself, which are seen in the index page in chronological order. 
If you click on the note header, you’re taken to a page where you can see the details of that particular note.

### Flaw 1: Broken access control [A01:2021](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
Users are able to see each others notes by typing note id's to urls.
