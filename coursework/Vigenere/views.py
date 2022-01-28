from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError

from .models import Person, UserAndMessage
from django.db.utils import IntegrityError
from django.contrib import messages
from .forms import CipherForm
from django.core.files import File
import os

def RegistrationTemplate(request):
    return render(request, 'Vigenere/registration.html')


def Registration(request):
    try:
        if request.method == 'POST':
            user = Person()
            checkLogin = request.POST.get('username')
            checkPassword = request.POST.get('pass')
            if len(checkLogin) > 7 and len(checkPassword) > 7:
                user.Login = request.POST.get('username')
                user.Password = request.POST.get('pass')
                user.save()
                return HttpResponseRedirect('encrypt')
            else:
                messages.error(request, 'Login and password must be over 7 letters')
                return redirect('/')
    except IntegrityError:
        messages.error(request, 'User with this login is already exist')
        return redirect('/')


def EncryptedTemplate(request):
    form = CipherForm()
    data = {
        'form': form
    }
    return render(request, 'Vigenere/encrypter.html', data)


def AuthEncMes(request):
    form = CipherForm(request.POST, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        username = request.POST.get("Log")
        password = request.POST.get("pass")
        try:
            checkUserLogin = Person.objects.get(Login=username, Password=password)
            rb = request.POST.get("RB", None)
            if rb in ["Decrypt", "Encrypt"]:
                if rb == "Encrypt":
                    try:
                        ChosenFile = request.FILES['chosenFile']
                        chosenFile = ChosenFile.name
                        path = os.path.abspath(chosenFile)
                        chsFile = open(path, 'a')
                        myfile = File(chsFile)
                        if checkUserLogin is not None:
                            msg = form.cleaned_data['Mess']
                            key = form.cleaned_data['Key']
                            EncMes = encrypt(msg, key)
                            if EncMes == '':
                                messages.error(request, 'Incorrect message or key')
                                return HttpResponseRedirect('encrypt')
                            else:
                                tmp = UserAndMessage.objects.create(EncryptMessage=EncMes, UserId=checkUserLogin.id)
                                myfile.write("\nYour encrypted message: " + EncMes)
                                myfile.closed
                                messages.success(request, "Your encrypted message: " + EncMes)
                                return HttpResponseRedirect('encrypt')
                    except MultiValueDictKeyError:
                        messages.error(request, 'You have not chosen file')
                        return HttpResponseRedirect('encrypt')
                elif rb == "Decrypt":
                    if checkUserLogin is not None:
                        msg = form.cleaned_data['Mess']
                        key = form.cleaned_data['Key']
                    try:
                        tmp = UserAndMessage.objects.get(EncryptMessage=msg, UserId=checkUserLogin.id)
                        if tmp is not None:
                            EncMes = decrypt(msg, key)
                            messages.success(request, "Your Decrypted message: " + EncMes)
                            return HttpResponseRedirect('encrypt')
                    except UserAndMessage.DoesNotExist:
                        messages.error(request, "Message is not found")
                        return HttpResponseRedirect('encrypt')
        except Person.DoesNotExist:
            messages.error(request, "Wrong login or password")
            return HttpResponseRedirect('encrypt')
    return HttpResponseRedirect('encrypt')

def showCheckMessages(request):
    return render(request, 'Vigenere/checkmessages.html')

def CheckMessagesInDB(request):
    if request.method == "POST":
        username = request.POST.get("Log")
        password = request.POST.get("pass")
        try:
            checkUserLogin = Person.objects.get(Login=username, Password=password)
            if checkUserLogin is not None:
                MesUser = UserAndMessage.objects.filter(UserId=checkUserLogin.id)
                return render(request, "Vigenere/checkmessages.html", {"MesUser": MesUser})
            else:
                messages.error(request, "Wrong login or password")
                return HttpResponseRedirect('CheckMessages')
        except Person.DoesNotExist:
            messages.error(request, "Wrong login or password")
            return HttpResponseRedirect('CheckMessages')
    return HttpResponseRedirect('CheckMessages')

def encrypt(message, key):
    symbols = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ,.!?1234567890@#$%&*^()+:;/[]{}~<>|"
    encrypted = ""
    for i in message:
        if i not in symbols:
            return encrypted
    for i in key:
        if i not in symbols:
            return encrypted
    if len(message) == 0 or len(key) == 0 or len(message) < len(key):
        encrypted = ""
        return encrypted
    else:
        letter_to_index = dict(zip(symbols, range(len(symbols))))
        index_to_letter = dict(zip(range(len(symbols)), symbols))
        encrypted = ""
        split_text = [
            message[i: i + len(key)] for i in range(0, len(message), len(key))
        ]

        for each_split in split_text:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(symbols)
                encrypted += index_to_letter[number]
                i += 1

        return encrypted


def decrypt(message, key):
    symbols = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ,.!?1234567890@#$%&*^()+:;/[]{}~<>|"
    decrypted = ""
    for i in message:
        if i not in symbols:
            return decrypted
    for i in key:
        if i not in symbols:
            return decrypted
    if len(message) == 0 or len(key) == 0 or len(message) < len(key):
        return decrypted
    else:
        letter_to_index = dict(zip(symbols, range(len(symbols))))
        index_to_letter = dict(zip(range(len(symbols)), symbols))
        split_encrypted = [
            message[i: i + len(key)] for i in range(0, len(message), len(key))
        ]

        for each_split in split_encrypted:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(symbols)
                decrypted += index_to_letter[number]
                i += 1

        return decrypted