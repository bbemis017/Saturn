from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
#from section.forms import summaryForm


@login_required
def create_summary(request):
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
    if request.is_ajax();
        content = request.POST('content')
        template = request.POST('template')
        summary = Summary.objects.get(id=request.POST['summary_id'])
        if summary.user == request.user:
            #do edit operations
            summary.content = request.POST['summary']
            summary.save()
            return render(request, "website/sites.html",locals())
        else:
            #return to somewhere else
            return render(request, "website/sites.html",locals())
    return render(request, "website/sites.html",locals())