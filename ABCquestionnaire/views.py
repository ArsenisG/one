from django.shortcuts import render, redirect
from ABCquestionnaire.forms import ValueForm
from ABCquestionnaire.models import Value
from django.template.defaulttags import register
from django.http import HttpResponse
from django.contrib.auth.models import User
from ABCquestionnaire.singlestudent import graphs
import matplotlib
matplotlib.use('Agg')
from io import BytesIO, StringIO
import six
from django.template import Context
from django.template import loader
from django.contrib.auth.decorators import login_required

def question_values(request):
    form = ValueForm()
    ABCQuestions = {'Q1':'1. Study effectively on your own in independent private study',
        'Q2':'2. Produce your best work under examination conditions',
	    'Q3':'3. Respond to questions asked by a lecturer in front of a full lecture theatre',
	    'Q4':'4. Manage your workload to meet coursework deadlines',
	    'Q5':'5. Give a presentation to a small group of fellow students',
	    'Q6':'6. Attend most taught sessions',
	    'Q7':'7. Attain good grades in your work',
	    'Q8':'8. Engage in profitable academic debate with your peers',
	    'Q9':'9. Ask lecturers questions about the material they are teaching, during a lecture',
	    'Q10':'10. Produce coursework at the required standard',
	    'Q11':'11. Write in an appropriate academic style',
	    'Q12':'12. Be on time for lectures',
	    'Q13':'13. Pass assessments at the first attempt',
	    'Q14':'14. Plan appropriate revision schedules',
	    'Q15':'15. Remain adequately motivated throughout',
	    'Q16':'16. Produce your best work in coursework assignments',
	    'Q17':'17. Attend tutorials',
      }  
    return render(request,'ABCquestionnaire/index.html', {'form':form, 'ABCQuestions':ABCQuestions})

@register.filter
# @login_required
    # def get_item(dictionary, key):
    #     return dictionary.get(key)
def create_survey(request):
        # value=Value(user=request.user)
        if request.method=='POST':
            form=ValueForm(request.POST)
            if form.is_valid():
                answers=form.save(commit=False)
                answers.user=request.user
                answers.save()
                return redirect('/result')
        values=Value.objects.order_by('-id')[0]
        datas=[values.SN,values.choice1,values.choice2,values.choice3,values.choice4,
            values.choice5,values.choice6,values.choice7,values.choice8,values.choice9,
            values.choice10,values.choice11,values.choice12,values.choice13,values.choice14,
            values.choice15,values.choice16,values.choice17 
        ]       
        return render(request, 'ABCquestionnaire/result.html', {'values':values, 'datas':datas})

    #     request.session['StudentNo'] = request.POST.get('StudentNo')
    #     request.session['Q1'] = request.POST.get('choice1')
    #     request.session['Q2'] = request.POST.get('choice2')
    #     request.session['Q3'] = request.POST.get('choice3')
    #     request.session['Q4'] = request.POST.get('choice4')
    #     request.session['Q5'] = request.POST.get('choice5')
    #     request.session['Q6'] = request.POST.get('choice6')
    #     request.session['Q7'] = request.POST.get('choice7')
    #     request.session['Q8'] = request.POST.get('choice8')
    #     request.session['Q9'] = request.POST.get('choice9')
    #     request.session['Q10'] = request.POST.get('choice10')
    #     request.session['Q11'] = request.POST.get('choice11')
    #     request.session['Q12'] = request.POST.get('choice12')
    #     request.session['Q13'] = request.POST.get('choice13')
    #     request.session['Q14'] = request.POST.get('choice14')
    #     request.session['Q15'] = request.POST.get('choice15')
    #     request.session['Q16'] = request.POST.get('choice16')
    #     request.session['Q17'] = request.POST.get('choice17')                       
    #     return redirect('/result')
    # else:
    #     return redirect('/')



def submitted_info(request):
    if 'count' not in request.session:
        request.session['count'] = 0
    request.session['count'] += 1
    return render (request, 'ABCquestionnaire/result.html')


def python_code(request):   
    values=Value.objects.order_by('-id')[0]
    datas=[values.SN,values.choice1,values.choice2,values.choice3,values.choice4,
            values.choice5,values.choice6,values.choice7,values.choice8,values.choice9,
            values.choice10,values.choice11,values.choice12,values.choice13,values.choice14,
            values.choice15,values.choice16,values.choice17 
        ]
    fig1,fig2,fig3,fig4,fig5=graphs.python(datas)
    template=loader.get_template('ABCquestionnaire/final.html')
    tmp1=six.StringIO()
    fig1.savefig(tmp1, format='svg', bbox_inches='tight')    
    c1={'svg1':tmp1.getvalue()}
    tmp2=six.StringIO()
    fig2.savefig(tmp2, format='svg', bbox_inches='tight')
    c2={'svg2':tmp2.getvalue()}
    tmp3=six.StringIO()
    fig3.savefig(tmp3, format='svg', bbox_inches='tight')
    c3={'svg3':tmp3.getvalue()}
    tmp4=six.StringIO()
    fig4.savefig(tmp4, format='svg', bbox_inches='tight')
    c4={'svg4':tmp4.getvalue()}
    tmp5=six.StringIO()
    fig5.savefig(tmp5, format='svg', bbox_inches='tight')
    c5={'svg5':tmp5.getvalue()}
    global c
    c={'svg1':tmp1.getvalue(),'svg2':tmp2.getvalue(),'svg3':tmp3.getvalue(),'svg4':tmp4.getvalue(),'svg5':tmp5.getvalue()}
    #return HttpResponse((template.render(c1),template.render(c2),template.render(c3),template.render(c4),template.render(c5)))
    return render(request, 'ABCquestionnaire/final.html', c)


def download_figs(request):
    global c
    return render(request, "ABCquestionnaire/download1.html", c)











