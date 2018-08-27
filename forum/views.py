from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from forum.models import Question, Solutions, Upvote

def signup(request):
	if request.user.is_authenticated:
		return redirect("/signin/")

	if request.method == "POST":
		username = request.POST.get('name')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')

		try:
			user = User.objects.get(name=username)
			return render(request, "forum/signup.html", {"error": "User with this email already exists."})
		except:
			if password1 == password2:
				#Register
				user = User.objects.create_user(username=username,
												password=password1,
												is_staff = True)
				login(request, user)
				return redirect('/home/')
			else:
				return render(request, "forum/signup.html", {"error": "The passwords do not match."})

	return render(request, "forum/signup.html")

def signin(request):
	if request.user.is_authenticated:
		return redirect("/home/")
	
	if request.method == "POST":
		username = request.POST.get('name')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
		return redirect("/home/")

	return render(request, "forum/login.html")

def signout(request):
	logout(request)
	return redirect("/login/")

def post_question(request):
	if not request.user.is_authenticated:
		return redirect("/login/")

	if request.method=="POST":
		
		text = request.POST.get('question')
		question = Question(question = text, author=request.user)
		question.save()
		return redirect("/home/")

	question = Question.objects.all().order_by('-datetime')
	return render(request, "forum/home.html", {"question" : question})

def question_page(request, qid):
	q = Question.objects.get(pk=qid)
	if request.method == "POST":
		answer = request.POST.get('answer', 'Left empty!')
		ans = Solutions.objects.create(answer=answer, question=q, upvotes=1, author=request.user)
		return redirect("/question/{}/".format(q.id))

	answers = Solutions.objects.filter(question = q)
	return render(request, 'forum/question.html', {"question":q, "answer":answers})

def upvote(request, aid):
	a = Solutions.objects.get(pk=aid)
	upvotes = Upvote.objects.filter(author=request.user, answer=a)
	if len(upvotes) == 0:
		a.upvotes +=1
		a.save()
		u = Upvote(author=request.user, answer=a)
		u.save()
	return redirect("/question/{}/".format(a.question.id))

