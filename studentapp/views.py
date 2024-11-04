from django.shortcuts import render

# Create your views here.
def StudentHomePage(request):
     return render(request,'studentapp/StudentHomePage.html')


from django.shortcuts import render, redirect
from .forms import FeedbackForm


def feedback(request):
     if request.method == 'POST':
          form = FeedbackForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('studentapp:feedback_success')  # Redirect to the success page
     else:
          form = FeedbackForm()

     return render(request, 'studentapp/feedback.html', {'form': form})


def feedback_success(request):
     return render(request, 'studentapp/feedback_success.html')  # Render success template
