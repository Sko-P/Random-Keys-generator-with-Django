from django.shortcuts import render
from .forms import Choices
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.



def get_key(request):
    #form = Choices(request.POST)
    
    text_file = "/files.txt"
    qr_path = ""
    if(request.method == "POST"):
        
        if('myfile' in request.FILES):
            try:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage(location=settings.FILES_ROOT)
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                print(uploaded_file_url)
                print(myfile)
                
            except:
                print("Dict ")
        multiple = False
        nb_keys = int(request.POST.get('keys'))
        nb_fields = int(request.POST.get('fields'))
        nb_chara = int(request.POST.get('length'))
        radio_letters = str(request.POST.get('drone'))
        radio_upper = str(request.POST.get('drone1'))
        qr = str(request.POST.get('qr'))
        
        
        # this is my file
        
        if(nb_keys != 0):
            if(nb_keys != 1) :
                multiple = True
                all_keys = []
                for i in range(0,nb_keys):
                    key = generate_rand(nb_fields, nb_chara, radio_letters, radio_upper)
                    all_keys.append(key)
                
                context = {
                'multiple' : multiple,
                'all_keys' :  all_keys,
                'image_path' : qr_path,
                
                }

                return render(request, "rand/getrandom.html", context)

            else:

                print("RADIO 1 : ",radio_letters)
                print("RADIO 2 : ", radio_upper)
                
                key = generate_rand(nb_fields, nb_chara, radio_letters, radio_upper)
                
                if(qr == "yes"):
                    qr_path = generate_qr(key)
                    print(qr_path)

                context = {
                'multiple' : multiple,
                'key' :  key,
                'image_path' : qr_path,
                
                }

                return render(request, "rand/getrandom.html", context)
        else:
            return render(request, "rand/getrandom.html")
    

    context = {
        'image_path' : qr_path,
        
    }

    return render(request, "rand/getrandom.html",context)



def generate_rand(nb_fields, nb_chara, r_l, r_u):
    import math
    from random import randrange
    import random
    import string
    key =""
    
    for j in range(0,nb_fields):
        for i in range(0,nb_chara):
            if(r_l == "both"): 
                choic = randrange(0,2)
                if(choic == 0):
                    #letter case
                    if(r_u == "both"):
                        key +=random.choice(string.ascii_letters)
                    else:
                        if(r_u == "lower"):
                            key +=random.choice(string.ascii_lowercase)
                        else:
                            key +=random.choice(string.ascii_uppercase)
                else: 
                    #number case
                    key +=str(randrange(0,9))
            else:
                if(r_l == "letters"):
                    if(r_u == "both"):
                        key +=random.choice(string.ascii_letters)
                    else:
                        if(r_u == "lower"):
                            key +=random.choice(string.ascii_lowercase)
                        else:
                            key +=random.choice(string.ascii_uppercase)
                else:
                    key +=str(randrange(0,9))

        if(j != nb_fields - 1):
            key +="-"
    print(key)
    return key


def generate_qr(key):
    import qrcode
    from random import randrange
    from qrcode.image.pure import PymagingImage

    qr_name = "/oo"+str(randrange(0,90))+".png"
    path = settings.MEDIA_ROOT+qr_name
    print(path)
    img = qrcode.make(key)
    img.save(path)
    mini_path = "/images"+qr_name
    print(mini_path)
    return mini_path