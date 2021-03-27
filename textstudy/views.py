from django.shortcuts import render

# Create your views here.


"""

*total number of words
*total number of stop-words
*total number of adjectives
*total number of punctuation

all distances expressed in words

*minimal distance between two repeating words
*


*Definition of each word


*Search for antonymes in same text

"""

def main(request):
    
    if(request.method == "POST"):
        
        text = str(request.POST.get('text_area'))

        aa = analyze_text(text)

        context = {
            'aa' : aa,
            'nb' : len(aa
            )
        }

        return render(request,"textstudy/textstudy.html", context)
    return render(request,"textstudy/textstudy.html")
    


def analyze_text(text):
    import spacy

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text) 

    all_ent = []

    for en in doc:
        all_ent.append(en.text)

    return all_ent