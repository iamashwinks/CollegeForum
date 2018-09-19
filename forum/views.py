from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from forum.models import Question, Solutions, Upvote, Comment
from mixpanel import Mixpanel

mp = Mixpanel("Your Token Id" )

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
				mp.track(user.username, f"New user Signed up {user.username}")
				login(request, user)
				return redirect('/')
			else:
				return render(request, "forum/signup.html", {"error": "The passwords do not match."})

	return render(request, "forum/signup.html")

def signin(request):
	if request.user.is_authenticated:
		return redirect("/")
	
	if request.method == "POST":
		username = request.POST.get('name')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		mp.track(user.username, f"User logged in {user.username}")
		if user is not None:
			login(request, user)
		return redirect("/")

	return render(request, "forum/login.html")

def signout(request):
	mp.track(str(request.user), f"{request.user} logged out!")
	logout(request)
	return redirect("/login/")

def post_question(request):
	if not request.user.is_authenticated:
		return redirect("/login/")

	if request.method=="POST":
		text = request.POST.get('question')
		question = Question(question = text, author=request.user)
		mp.track(question.question, f'New Question by {question.author}')
		question.save()
		return redirect("/")

	question = Question.objects.all().order_by('-datetime')
	return render(request, "forum/home.html", {"question" : question})

def question_page(request, qid):
	q = Question.objects.get(pk=qid)
	if request.method == "POST":
		answer = request.POST.get('answer', 'Left empty!')
		ans = Solutions.objects.create(answer=answer, question=q, upvotes=1, author=request.user)
		mp.track(ans.answer, f'New Answer by {ans.author}')
		return redirect("/question/{}/".format(q.id))

	answers = Solutions.objects.filter(question = q)
	mp.track(q.question, f'Clicked on question by {request.user}')
	return render(request, 'forum/question.html', {"question":q, "answer":answers})

def upvote(request, aid):
	a = Solutions.objects.get(pk=aid)
	upvotes = Upvote.objects.filter(author=request.user, answer=a)
	if len(upvotes) == 0:
		a.upvotes +=1
		a.save()
		u = Upvote(author=request.user, answer=a)
		mp.track(a.answer, f'New Upvote by {request.user}')
		u.save()
	return redirect("/question/{}/".format(a.question.id))

def comment(request, aid):
	a = Solutions.objects.get(pk=aid)
	if request.method == "POST":
		text = request.POST.get('comment')
		comment = Comment(answer=a, comment=text, author=request.user)
		comment.save()
		return redirect("/question/{}/".format(a.question.id))

	reply = Comment.objects.filter(answer = a)
	return render(request, 'forum/question.html', {"answer":a, "reply" : reply})


