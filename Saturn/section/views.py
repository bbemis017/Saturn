from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
#from section.forms import summaryForm


@login_required
def create_summary(request):
    # TODO: Here read request.POST for necessary informations
    if not request.is_ajax():
        content = request.GET('content')
        template = request.GET('template')

        if not Section.objects.filter(content=content, template=template).exists():
            #create summary
            summaries = Summary.objects.create(user=request.user, template=template)
            summaries.content = content
            summaries.save()
            return JsonResponse({"id": summaries.id, "content": summaries.content, 
                                "template": template, "user": request.user})
        else:
            return HttpResponseRedirect("/Section/edit_summary")
    else:
        create_summary_err = True
        return render(request,"website/sites.html",locals())


@login_required
def edit_summary(request):
    # TODO: edit
    print request.POST
