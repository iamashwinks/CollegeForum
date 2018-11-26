from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from forum.models import Question, Solutions, Upvote, Comment
from mixpanel import Mixpanel

mp = Mixpanel("3ed3e1ba477dcd296e8989040bdd10c6 " )

def signup(request):
	if request.user.is_authenticated:
		return redirect("/signin/")

	if request.method == "POST":
		username = request.POST.get('name')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		full_name = request.POST.get('full_name')

		try:
			user = User.objects.get(name=username)
			return render(request, "forum/signup.html", {"error": "User with this email already exists."})
		except:
			if password1 == password2:
				#Register
				user = User.objects.create_user(username=username,
												full_name = full_name,
												password=password1,
												is_staff = True)
				login(request, user)
				mp.people_set(str(request.user.id), {'$full_name' : f'{user.full_name}',})
				mp.track(str(request.user.id), "New user signed up")
				mp.alias(request.user.id, user.username)
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
		mp.track(user.username, "User logged in")
		if user is not None:
			login(request, user)
		return redirect("/")

	return render(request, "forum/login.html")

def signout(request):
	mp.track(request.user.username, "User logged out!")
	logout(request)
	return redirect("/login/")

def post_question(request):
	if not request.user.is_authenticated:
		return redirect("/login/")

	if request.method=="POST":
		text = request.POST.get('editordata')
		question = Question(question = text, author=request.user)
		mp.track(request.user.username, 'New question',  {"Link":"http://127.0.0.1:8000/", "Question": f"{question.question}"})
		question.save()
		return redirect("/")

	question = Question.objects.all().order_by('-datetime')
	return render(request, "forum/home.html", {"question" : question})

def question_page(request, qid):
	q = Question.objects.get(pk=qid)
	if request.method == "POST":
		answer = request.POST.get('answer', 'Left empty!')
		ans = Solutions.objects.create(answer=answer, question=q, upvotes=1, author=request.user)
		answers = Solutions.objects.filter(question = q)
		mp.track(request.user.username, 'New answer', {"Question ID": str(q.id), "Link":f"http://127.0.0.1:8000/question/{q.id}/", "Answer" : f"{ans.answer}"})
		return render(request, 'forum/question.html', {"question":q, "answer":answers})

	answers = Solutions.objects.filter(question = q)
	mp.track(request.user.username, 'Clicked on question', {"Question ID": str(q.id), "Link":f"http://127.0.0.1:8000/question/{q.id}/"})
	return render(request, 'forum/question.html', {"question":q, "answer":answers})

def upvote(request, aid):
	a = Solutions.objects.get(pk=aid)
	upvotes = Upvote.objects.filter(author=request.user, answer=a)
	if len(upvotes) == 0:
		a.upvotes +=1
		a.save()
		u = Upvote(author=request.user, answer=a)
		mp.track(a.answer, 'New upvote')
		u.save()
	return redirect("/question/{}/".format(a.question.id))

def comment(request, aid):
	a = Solutions.objects.get(pk=aid)
	if request.method == "POST":
		text = request.POST.get('comment')
		comment = Comment(answer=a, comment=text, author=request.user)
		mp.track(comment.comment, "New comment")
		comment.save()
		return redirect("/question/{}/".format(a.question.id))

	reply = Comment.objects.filter(answer = a)
	return render(request, 'forum/question.html', {"answer":a, "reply" : reply})


