from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .form import ImageForm , CreateUserForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.template.loader import get_template
from xhtml2pdf import pisa

from tensorflow.keras.models import load_model, model_from_json
import cv2
import json
import numpy as np
import os
import tensorflow as tf
from tensorflow import Graph
import keras

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.6

shape=(200,200)
with open('./models/labels.json','r') as f:
    label=f.read()
labels=json.loads(label)

model_graph=Graph()
with model_graph.as_default():
    tf_session=tf.compat.v1.Session()
    with tf_session.as_default():
        model = model_from_json(open("./models/fer.json", "r").read())
        model.load_weights("./models/fer_test.h5")

def index(request):
    if request.user.is_authenticated:
        return redirect('crop_detector:dashboard')
    else:
        form=CreateUserForm()
        if request.method=="POST":
            if request.POST.get('submit') == 'sign_in':
                # your sign in logic goes here
                username=request.POST.get('username')
                password=request.POST.get('password')

                user=authenticate(request,username=username,password=password)

                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('crop_detector:dashboard'))
                else:
                    messages.info(request, "Username or Password is incorrect")


            elif request.POST.get('submit') == 'sign_up':
                form=CreateUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request,"Account was created successfully")
                    context={}
                    return HttpResponseRedirect(reverse('crop_detector:index'))
                else:
                    messages.error(request,"Error !!!  Account was not created, please Sign Up with correct details")
                    context={'form':form}
                    return render(request,'crop_detector/index.html',context)

        context={'form':form}
        return render(request,'crop_detector/index.html',context)

def logoutUser(request):
    logout(request)
    return redirect('crop_detector:index')

@login_required(login_url='crop_detector:index')
def delete_image(request, pk):
    if request.method=="POST":
        obj=Image.objects.filter(user=request.user).get(id=pk)
        obj.delete()
        return HttpResponseRedirect(reverse('crop_detector:dashboard'))


@login_required(login_url='crop_detector:index')
def download(request):
    img=Image.objects.filter(user=request.user).order_by('-pub_date')

    template_path="crop_detector/download.html"
    context={"img":img}

    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='filename="report.pdf"'

    template=get_template(template_path)
    html=template.render(context)

    pisa_status=pisa.CreatePDF(html,dest=response)

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>"+html+"</pre>")
    return response


@login_required(login_url='crop_detector:index')
def dashboard(request):
    diseasedata={
    "Mango":{"Powdery mildew":"https://www.gardendesign.com/how-to/powdery-mildew.html","Anthracnose":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn7420.html","Die back":"https://www.britannica.com/science/dieback","Phoma blight":"https://www.gardeningknowhow.com/plant-problems/disease/phoma-blight-disease.htm","Bacterial canker":"https://www.planetnatural.com/pest-problem-solver/plant-disease/bacterial-canker/","Red rust":"https://www.vedantu.com/question-answer/red-rust-of-tea-is-caused- by-parasitic-aalgae-class-8-biology-cbse-5f550d903035db208c0dfa72","Sooty mould":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn74108.html","Mango malformation":"https://agritech.tnau.ac.in/crop_protection/mango_3.html","Others":"https://vikaspedia.in/agriculture/crop-production/integrated-pest-managment/ipm-for-fruit-crops/ipm-strategies-for-mango/mango-diseases-and-symptoms"},


    "Alstoni-Scholaris":{"Pauropsylla tuberculata":"https://www.ijcrt.org/papers/IJCRT1802217.pdf","Leaf gall":"https://www.ijcrt.org/papers/IJCRT1802217.pdf","Others":"https://vikaspedia.in/agriculture/crop-production/package-of-practices/medicinal-and-aromatic-plants/alstonia-scholaris"},


    "Arjun":{"Ascomycetes":"https://en.wikipedia.org/wiki/Ascomycota","Basidiomycetes":"https://www.cliffsnotes.com/study-guides/biology/biology/fungi/basidiomycetes","Leaf spot":"https://en.wikipedia.org/wiki/Pestalotiopsis_palmarum","Black nodal girdling":"http://silks.csb.gov.in/jhansi/diseases-and-pests-of-food-plants","Powdery mildew":"https://en.wikipedia.org/wiki/Phyllactinia_guttata","Leaf Curl":"https://en.wikipedia.org/wiki/Leaf_curl","Others":"http://silks.csb.gov.in/jhansi/diseases-and-pests-of-food-plants/"},


    "Gauva":{"Dieback and Anthracnose":"https://vikaspedia.in/agriculture/crop-production/integrated-pest-managment/ipm-for-spice-crops/ipm-strategies-for-chilli/chilli-description-of-plant-diseases","Guava wilt":"https://krishijagran.com/featured/guava-wilt-a-challenge-in-plant-pathology/","Algal leaf and fruit spot":"https://hgic.clemson.edu/factsheet/algal-leaf-spot/","Styler end rot ":"https://www.gardeningknowhow.com/edible/fruits/citrus/managing-fruit-with-stylar-end-rot.htm","Fruit canker ":"https://en.wikipedia.org/wiki/Citrus_canker","Others":"https://vikaspedia.in/agriculture/crop-production/integrated-pest-managment/ipm-for-fruit-crops/ipm-strategies-for-guava/guava-diseases-and-symptoms"},


    "Jamun":{"Anthracnose":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn7420.html","White fly":"https://en.wikipedia.org/wiki/Dialeurodes","Leaf eating caterpillar":"https://blogs.massaudubon.org/yourgreatoutdoors/the-leaf-eating-tree-damaging-little-green-caterpillar/","Others":"https://agritech.tnau.ac.in/horticulture/horti_fruits_jamun.html"},


    "Jatropha":{"Anthracnose":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn7420.html","Passiflora":"https://en.wikipedia.org/wiki/Passiflora","Pseudocercosporaleaf spot":"http://ipm.ucanr.edu/PMG/r735100511.html","Powdery mildew":"https://www.gardendesign.com/how-to/powdery-mildew.html","Rust":"https://www.planetnatural.com/pest-problem-solver/plant-disease/common-rust/","Stem canker and dieback":"http://ipm.illinois.edu/diseases/series600/rpd636/","Collar and root rot":"https://en.wikipedia.org/wiki/Collar_rot","Others":"https://www.intechopen.com/books/biodiesel-feedstocks-production-and-applications/major-diseases-of-the-biofuel-plant-physic-nut-jatropha-curcas-"},


    "Lemon":{"Citrus scab":"https://idtools.org/id/citrus/diseases/factsheet.php?name=Citrus%20scab","Citrus canker":"https://www.missouribotanicalgarden.org/gardens-gardening/your-garden/help-for-the-home-gardener/advice-tips-resources/pests-and-problems/diseases/cankers/gummosis-of-fruit-trees.aspx","Citrus tristeza":"https://en.wikipedia.org/wiki/Citrus_tristeza_virus","Huanglongbing":"https://www.frontiersin.org/articles/10.3389/fpls.2018.01976/full","Anthracnose":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn7420.html","Sooty mould":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn74108.html","Others":" https://vikaspedia.in/agriculture/crop-production/integrated-pest-managment/ipm-for-fruit-crops/ipm-strategies-for-citrus/diseases-and-symptoms"},


    "Pomegranate":{"Anthracnose":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn7420.html","Leaf and Fruit Spots":"https://idtools.org/id/citrus/diseases/factsheet.php?name=Pseudocercospora+fruit+and+leaf+spot","Dwiroopa punicae":"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7241677/","Fruit Rot and Mummification":"https://www2.ipm.ucanr.edu/agriculture/pomegranate/Alternaria-Fruit-Rot-Black-Heart/","Others":"https://edis.ifas.ufl.edu/publication/pp349"},


    "Pongamia-Pinnata":{"Leaf spot and blight":"https://idtools.org/id/palms/symptoms/factsheet.php?name=Leaf+Spots+and+Leaf+Blights","Leaf Rust":"https://cropwatch.unl.edu/plantdisease/wheat/leaf-rust","Powdery mildew":"https://www.gardendesign.com/how-to/powdery-mildew.html","Others":"https://agritech.tnau.ac.in/forestry/forest_disease_pungam.html"},


    "Chinar":{"Canker stain":"https://www.forestresearch.gov.uk/tools-and-resources/fthr/pest-and-disease-resources/canker-stain-plane-ceratocystis-platani/","Stem canker ":"https://cropwatch.unl.edu/plantdisease/soybean/stem-canker","Anthracnose ":"http://ipm.ucanr.edu/PMG/PESTNOTES/pn7420.html","Lace bugs":"https://en.wikipedia.org/wiki/Tingidae","Others":"https://balconygardenweb.com/everything-about-chinar-trees/"}
    }
    if request.method=="POST":
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.pub_date=timezone.now()
            profile.save()


            img=Image.objects.filter(user=request.user).latest('pub_date')
            # print(request.FILES)
            # print(img.images.url)
            #
            # print(profile.images.url)
            # print(profile.plant_name)
            # print(profile.plant_health)

            img=cv2.imread('.'+img.images.url)
            img=cv2.resize(img,shape)
            img=np.array(img)
            img = np.expand_dims(img, axis=0)
            img = tf.cast(img, tf.float32)
            with model_graph.as_default():
                with tf_session.as_default():
                    predict=model.predict(img,steps=1)

            #print(labels[str(np.argmax(predict))])
            plant_details=labels[str(np.argmax(predict))].split("_")
            print(plant_details)
            profile.plant_name=plant_details[0]
            profile.plant_health=plant_details[1]
            profile.save()

            # print(profile.images.url)
            # print(profile.plant_name)
            # print(profile.plant_health)

            obj=form.instance
            context={"obj":obj}
            #return render(request,'crop_detector/dashboard.html',context)
            return HttpResponseRedirect(reverse('crop_detector:dashboard'))
    else:
        form=ImageForm()
        img=Image.objects.filter(user=request.user).order_by('-pub_date')
        #img=Image.objects.filter(user=request.user)
        context={"form":form,"img":img,"diseasedata":diseasedata}
    return render(request,'crop_detector/dashboard.html',context)
