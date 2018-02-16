from __future__ import unicode_literals
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy , reverse
from django.core.mail import send_mail
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login
from django.http import JsonResponse
from .forms import Signin , Signup , CommentTemplate , ReplyTemplate , ThreadTemplate , ProfileTemplate , FeedbackTemplate, FeedbackNewTemplate, ForgotPasswordTemplate
from .models import Account , State , Lga , Position , Thread ,Media , Zone , Comment , Reply , ThreadFavoriter, CommentFavoriter, ReplyFavoriter , Feedback

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
VIDEO_FILE_TYPES = ['webm', 'mp4', 'ogg']



def index(request):

    thread_list = Thread.objects.filter(namespace = 1) | Thread.objects.filter(namespace = 2)

    content_cache = []
    content = {}

    for thread in thread_list:

        thread_post = thread.thread

        if len(thread_post.split()) >= 50:
            is_long = 1

        else:
            is_long = 0


        id = thread.id
        date = thread.date
        account_id = thread.account_id
        account = Account.objects.get(id=account_id)

        firstname = account.firstname
        lastname = account.lastname
        position_id = account.position_id
        display_pic = account.display_pic

        get_position = Position.objects.get(id = position_id)

        position = get_position.position

        thread_media = Media.objects.filter(thread_id = id)[:1]

        context_list = {
            'id' : id ,
            'thread_post' : thread_post,
            'date' : date,
            'is_long' : is_long,
            'thread_media': thread_media,
            'firstname' : firstname,
            'lastname' : lastname,
            'position' : position,
            'display_pic' : display_pic
        }

        content_cache.append(context_list)

    content = {
        'content_cache':content_cache
    }


    return render(request ,'federal/index.html',content)






class HomeView(FormView):

    form_class = ThreadTemplate
    template_name ='federal/home.html'
    is_logged_in = False
    show_form = False


    #audio_file = forms.FileField( label = _(u"Audio File" ))
    #video_file = forms.FileField( label = _(u"Video File" ))


    def get(self,request):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        account = Account.objects.get(username=username)

        a_position = account.position_id

        b_position = Position.objects.get(id = a_position)

        c_position = b_position.position

        if c_position == 'Citizen':
            show_form = False

        else :
            show_form = True

        zone_id = account.zone_id
        lga_id = account.lga_id
        state_id = account.state_id

        state = State.objects.get(id=state_id)
        state_code = state.state_code

        zone = Zone.objects.get(id=zone_id)
        zone_code = zone.zone_code

        lga = Lga.objects.get(id=lga_id)
        lga_code = lga.lga_code

        thread_list = Thread.objects.filter(namespace=1) | Thread.objects.filter(namespace=2) | \
                        Thread.objects.filter(state = state_code) | Thread.objects.filter(zone = zone_code) | \
                            Thread.objects.filter(lga = lga_code)



        content_cache = []
        content = {}

        for thread in thread_list:


            thread_post = thread.thread

            if len(thread_post.split()) >= 50:
                is_long = 1

            else:
                is_long = 0


            id = thread.id
            date = thread.date

            account_id = thread.account_id
            account = Account.objects.get(id=account_id)

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)
            position = get_position.position

            my_id = Account.objects.get(username = username);
            my_id = my_id.id

            if_favorited = ThreadFavoriter.objects.filter(thread_id = id , account_id = my_id).exists()

            favorite_count = ThreadFavoriter.objects.filter(id = id).count()

            thread_media = Media.objects.filter(thread_id = id)[:1]

            context_list = {
                'id' : id,
                'thread_post' : thread_post,
                'date' : date,
                'is_long' : is_long,
                'thread_media' : thread_media,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'if_favorited' : if_favorited,
                'favorite_count' : favorite_count
            }

            content_cache.append(context_list)

        form=self.form_class(None)

        content = {
            'form' : form,
            'content_cache':content_cache,
            'show_form' : show_form,
            'is_logged_in' : is_logged_in
        }


        return render(request ,self.template_name,content)



    def post(self,request , *args, **kwargs):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        err_msg = ''

        #form=self.form_class(request)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        media = request.FILES.getlist('media')

        if form.is_valid():


            thread = form.cleaned_data['thread']

            new_thread = Thread()

            account = Account.objects.get(username=username)

            state_id = account.state_id
            zone_id = account.zone_id
            lga_id = account.lga_id

            account_id = account.id
            position_id = account.position_id
            a_position = position_id


            b_position = Position.objects.get(id = a_position)

            c_position = b_position.position

            if c_position == 'Citizen':
                show_form = False

            else :
                show_form = True

            position = Position.objects.get(id=position_id)

            namespace = 0
            state = 0
            zone = 0
            lga = 0

            if position.namespace != 0:
                namespace = position.namespace

            elif position.state != 0:
                state = position.state

            elif position.zone != 0:
                zone = position.zone

            elif position.lga != 0:
                lga = position.lga

            else:
                pass

            new_thread.thread = thread
            new_thread.account = account
            new_thread.namespace = namespace
            new_thread.state = state
            new_thread.zone = zone
            new_thread.lga = lga

            new_thread.save()

            thread_id = new_thread.id

            thread = Thread.objects.get(id=thread_id)

            for m in media :

                media_register = Media()
                media_register.thread = thread

                media_register.image = m
                media_register.audio = m
                media_register.video = m

                file_type = media_register.image.url.split('.')[-1]
                file_type = file_type.lower()

                if file_type in IMAGE_FILE_TYPES:

                    media_register.audio = 0
                    media_register.video = 0

                else:

                    file_type = media_register.audio.url.split('.')[-1]
                    file_type = file_type.lower()

                    if file_type in AUDIO_FILE_TYPES:

                        media_register.image = 0
                        media_register.video = 0

                    else:

                        file_type = media_register.video.url.split('.')[-1]
                        file_type = file_type.lower()

                        if file_type in VIDEO_FILE_TYPES:

                            media_register.image = 0
                            media_register.audio = 0

                        else:
                            err_msg = 'Unsupported file format, file should be valid image, audio or/and video files'




                media_register.save()








            state = State.objects.get(id=state_id)
            state_code = state.state_code

            zone = Zone.objects.get(id=zone_id)
            zone_code = zone.zone_code

            lga = Lga.objects.get(id=lga_id)
            lga_code = lga.lga_code

            thread_list = Thread.objects.filter(namespace=1) | Thread.objects.filter(namespace=2) | \
                            Thread.objects.filter(state = state_code) | Thread.objects.filter(zone = zone_code) | \
                                Thread.objects.filter(lga = lga_code)



            content_cache = []
            content = {}

            for thread in thread_list:



                thread_post = thread.thread

                is_long = 0

                if len(thread_post.split()) >= 50:
                    is_long = 1

                else:
                    is_long = 0





                id = thread.id
                account_id = thread.account_id
                account = Account.objects.get(id=account_id)

                firstname = account.firstname
                lastname = account.lastname
                position_id = account.position_id

                get_position = Position.objects.get(id = position_id)

                position = get_position.position

                my_id = Account.objects.get(username = username);
                my_id = my_id.id

                if_favorited = ThreadFavoriter.objects.filter(thread_id = id , account_id = my_id).exists()

                favorite_count = ThreadFavoriter.objects.filter(id = id).count()

                thread_media = Media.objects.filter(thread_id = id)[:1]

                context_list = {
                    'id' : id,
                    'thread_post' : thread_post,
                    'is_long' : is_long,
                    'thread_media' :  thread_media,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'position' : position,
                    'if_favorited' : if_favorited,
                    'favorite_count' : favorite_count
                }

                content_cache.append(context_list)

            form=self.form_class(None)

            content = {
                'form' : form,
                'err_msg': err_msg,
                'content_cache':content_cache,
                'show_form' : show_form,
                'is_logged_in' : is_logged_in
            }


            return render(request ,self.template_name,content)


        else:
            pass









class SignupView(View):

    form_class = Signup
    template_name ='federal/sign_up.html'

    def get(self, request):

         # if request.session.has_key('username'):
       #    return redirect('reminder:index')

        state_list = State.objects.all()

        lga_list = Lga.objects.all()

       # if request.session.has_key('username'):
       #    return redirect('federal:home')

        form=self.form_class(None)
        return render(request, self.template_name , {
        'form':form ,
        'state_list':state_list ,
        'lga_list':lga_list
        })


    def post(self, request):

        form=self.form_class(request.POST)

        if form.is_valid():

            state_list = State.objects.all()
            lga_list = Lga.objects.all()

            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            state = request.POST['state']
            lga = request.POST['lga']

            lga_in_state = Lga.objects.filter(id = lga , state_id = state).exists()

            if lga_in_state :

                state = State.objects.get(id=state)
                lga = Lga.objects.get(id=lga)

                lga_zone = lga.zone_id

                zone = Zone.objects.get(id = lga_zone)

                default = "Citizen"
                position = Position.objects.get(position=default)



                try:
                    acc = Account.objects.get(username = username)

                    err_msg = "An account with this email already exist"

                    if acc:
                        return render(request, self.template_name , {
                        'form':form ,
                        'err_msg':err_msg ,
                        'state_list' : state_list,
                        'lga_list' : lga_list,
                        'username':username
                        })

                except:
                    new_user = Account()

                    #set_password(password)

                    new_user.firstname = firstname
                    new_user.lastname = lastname
                    new_user.password = password
                    new_user.username = username
                    new_user.state = state
                    new_user.lga = lga
                    new_user.position = position
                    new_user.zone = zone
                    new_user.save()

                    request.session['username'] = username

                    return redirect('federal:home')

                else:
                    err_msg = "All fields are required"
                    name = acc.name

                    form=self.form_class(None)
                    return render(request, self.template_name , {
                    'form':form ,
                    'state_list':state_list,
                    'lga_list':lga_list,
                    'err_msg':err_msg
                    })


            else:

                err_msg = "Oops the Lga you chose is not in the state, try again"

                return render(request, self.template_name , {
                'form':form ,
                'err_msg':err_msg ,
                'state_list' : state_list,
                'lga_list' : lga_list
                })

        else:
            pass



class SigninView(View):

    form_class = Signin
    template_name ='federal/sign_in.html'

    def get(self, request):
       # if request.session.has_key('username'):
       #    return redirect('federal:home')

        form=self.form_class(None)
        return render(request, self.template_name , {
        'form':form
        })


    def post(self, request):
        form=self.form_class(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']



            try:
                acc = Account.objects.get(username = username)

                if password == acc.password:

                    request.session['username'] = username
                    return redirect('federal:home')

            except:

                err_msg = "Username and password did not match"
                name = acc.name

                form=self.form_class(None)
                return render(request, self.template_name , {
                'form':form ,
                'err_msg':err_msg
                })

            else:
                err_msg = "All fields are required"
                name = acc.name

                form=self.form_class(None)
                return render(request, self.template_name , {
                'form':form ,
                'err_msg':err_msg
                })
        else:
            pass






class CommentView(View):

    form_class = CommentTemplate
    template_name = 'federal/comment.html'
    is_logged_in = False

    def get(self, request , context_id):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        thread = Thread.objects.get(id=context_id)
        id = thread.id
        date = thread.date

        account_id = thread.account_id
        account = Account.objects.get(id=account_id)

        firstname = account.firstname
        lastname = account.lastname
        position_id = account.position_id
        display_pic = account.display_pic

        get_position = Position.objects.get(id = position_id)

        position = get_position.position


        comment_list = Comment.objects.filter(thread_id = context_id)

        thread_media = Media.objects.filter(thread_id = context_id)

        content_cache = []
        content = {}

        for comment in comment_list:

            comment_post = comment.comment
            id = comment.id
            account_id = thread.account_id
            account = Account.objects.get(id=account_id)

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)

            position = get_position.position

            my_id = Account.objects.get(username = username);
            my_id = my_id.id

            if_favorited = CommentFavoriter.objects.filter(comment_id = id , account_id = my_id).exists()

            favorite_count = CommentFavoriter.objects.filter(id = id).count()

            context_list = {
                'id' : id,
                'comment_post' : comment_post,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'if_favorited' : if_favorited,
                'favorite_count' : favorite_count
            }

            content_cache.append(context_list)

        content = {
            'thread' : thread ,
            'date' : date,
            'firstname' : firstname,
            'lastname' : lastname,
            'position' : position,
            'display_pic' : display_pic,
            'thread_media' : thread_media,
            'content_cache':content_cache,
            'is_logged_in' : is_logged_in
        }


        return render(request, self.template_name, content)



    def post(self, request , context_id):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        account = Account.objects.get(username=username)


        form=self.form_class(request.POST)

        if form.is_valid():


            post_comment = Comment()

            comment = form.cleaned_data['comment']

            thread = Thread.objects.get(id=context_id)


            post_comment.comment = comment
            post_comment.thread = thread
            post_comment.account = account
            post_comment.save()


        thread = Thread.objects.get(id=context_id)

        thread = Thread.objects.get(id=context_id)
        id = thread.id
        date = thread.date

        account_id = thread.account_id
        account = Account.objects.get(id=account_id)

        firstname = account.firstname
        lastname = account.lastname
        position_id = account.position_id
        display_pic = account.display_pic

        get_position = Position.objects.get(id = position_id)

        position = get_position.position

        thread_media = Media.objects.filter(thread_id = context_id)

        comment_list = Comment.objects.filter(thread_id = context_id)

        content_cache = []
        content = {}

        for comment in comment_list:

            comment_post = comment.comment
            id = comment.id
            account_id = thread.account_id
            account = Account.objects.get(id=account_id)

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)

            position = get_position.position

            my_id = Account.objects.get(username = username);
            my_id = my_id.id

            if_favorited = CommentFavoriter.objects.filter(comment_id = id , account_id = my_id).exists()

            favorite_count = CommentFavoriter.objects.filter(id = id).count()

            context_list = {
                'id' : id,
                'comment_post' : comment_post,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'if_favorited' : if_favorited,
                'favorite_count' : favorite_count
            }

            content_cache.append(context_list)

        content = {
            'thread' : thread,
            'date' : date,
            'firstname' : firstname,
            'lastname' : lastname,
            'position' : position,
            'display_pic' : display_pic,
            'thread_media': thread_media,
            'content_cache':content_cache,
            'is_logged_in' : is_logged_in
        }


        return render(request, self.template_name, content)




class ReplyView(View):

    form_class = ReplyTemplate
    template_name = 'federal/reply.html'
    is_logged_in = False

    def get(self, request , context_id):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        comment = Comment.objects.get(id=context_id)
        id = comment.id
        date = comment.date

        account_id = comment.account_id
        account = Account.objects.get(id=account_id)

        firstname = account.firstname
        lastname = account.lastname
        position_id = account.position_id
        display_pic = account.display_pic

        get_position = Position.objects.get(id = position_id)

        position = get_position.position

        reply_list = Reply.objects.filter(comment_id = context_id)

        content_cache = []
        content = {}

        for reply in reply_list:

            reply_post = reply.reply
            id = reply.id
            account_id = reply.account_id
            account = Account.objects.get(id=account_id)

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)

            position = get_position.position

            my_id = Account.objects.get(username = username);
            my_id = my_id.id

            if_favorited = ReplyFavoriter.objects.filter(reply_id = id , account_id = my_id).exists()

            favorite_count = ReplyFavoriter.objects.filter(id = id).count()

            context_list = {
                'id' : id,
                'reply_post' : reply_post,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'if_favorited' : if_favorited,
                'favorite_count' : favorite_count
            }

            content_cache.append(context_list)

        content = {
            'comment' : comment ,
            'date' : date,
            'firstname' : firstname,
            'lastname' : lastname,
            'position' : position,
            'display_pic' : display_pic,
            'content_cache':content_cache,
            'is_logged_in' : is_logged_in
        }


        return render(request, self.template_name, content)



    def post(self, request , context_id):


        if request.session.has_key('username'):
                username = request.session['username']
                is_logged_in = True

                account = Account.objects.get(username=username)

                form=self.form_class(request.POST)

                if form.is_valid():


                    post_reply = Reply()

                    reply = form.cleaned_data['reply']

                    comment = Comment.objects.get(id=context_id)


                    post_reply.reply = reply
                    post_reply.comment = comment
                    post_reply.account = account
                    post_reply.save()


                comment = Comment.objects.get(id=context_id)

                id = comment.id
                date = comment.date

                account_id = comment.account_id
                account = Account.objects.get(id=account_id)

                firstname = account.firstname
                lastname = account.lastname
                position_id = account.position_id
                display_pic = account.display_pic

                get_position = Position.objects.get(id = position_id)

                position = get_position.position

                reply_list = Reply.objects.filter(comment_id = context_id)

                content_cache = []
                content = {}

                for reply in reply_list:

                    reply_post = reply.reply
                    id = reply.id
                    account_id = reply.account_id
                    account = Account.objects.get(id=account_id)

                    firstname = account.firstname
                    lastname = account.lastname
                    position_id = account.position_id
                    display_pic = account.display_pic

                    get_position = Position.objects.get(id = position_id)

                    position = get_position.position

                    my_id = Account.objects.get(username = username);
                    my_id = my_id.id

                    if_favorited = ReplyFavoriter.objects.filter(reply_id = id , account_id = my_id).exists()

                    favorite_count = ReplyFavoriter.objects.filter(id = id).count()

                    context_list = {
                        'id' : id,
                        'reply_post' : reply_post,
                        'firstname' : firstname,
                        'lastname' : lastname,
                        'position' : position,
                        'display_pic' : display_pic,
                        'if_favorited' : if_favorited,
                        'favorite_count' : favorite_count
                    }

                    content_cache.append(context_list)

                content = {
                    'comment' : comment,
                    'date' : date,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'position' : position,
                    'display_pic' : display_pic,
                    'content_cache':content_cache,
                    'is_logged_in' : is_logged_in
                }


                return render(request, self.template_name, content)

        else:
            is_logged_in = False

            comment = Comment.objects.get(id=context_id)

            id = comment.id
            date = comment.date

            account_id = comment.account_id
            account = Account.objects.get(id=account_id)

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)

            position = get_position.position

            reply_list = Reply.objects.filter(comment_id = context_id)

            content_cache = []
            content = {}

            for reply in reply_list:

                reply_post = reply.reply
                id = reply.id
                account_id = reply.account_id
                account = Account.objects.get(id=account_id)

                firstname = account.firstname
                lastname = account.lastname
                position_id = account.position_id
                display_pic = account.display_pic

                get_position = Position.objects.get(id = position_id)

                position = get_position.position

                my_id = Account.objects.get(username = username);
                my_id = my_id.id

                if_favorited = ReplyFavoriter.objects.filter(reply_id = id , account_id = my_id).exists()

                favorite_count = ReplyFavoriter.objects.filter(id = id).count()

                context_list = {
                    'id' : id,
                    'reply_post' : reply_post,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'position' : position,
                    'display_pic' : display_pic,
                    'if_favorited' : if_favorited,
                    'favorite_count' : favorite_count
                }

                content_cache.append(context_list)

            content = {
                'comment' : comment,
                'date' : date,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'content_cache':content_cache,
                'is_logged_in' : is_logged_in
            }


            return render(request, self.template_name, content)




def validate_username(request):

    username = request.GET.get('username', None)

    data = {
        'is_taken': Account.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def t_unfavorited(request):

    if request.session.has_key('username'):
        username = request.session['username']

        thread_id = request.GET.get('thread_id', None)

        account = Account.objects.get(username = username)
        account_id = account.id

        d = ThreadFavoriter.objects.get(thread_id = thread_id , account_id = account_id)
        d.delete()

        is_unfavorited= ThreadFavoriter.objects.filter(thread_id = thread_id , account_id = account_id).exists()

        counter = ThreadFavoriter.objects.filter(thread_id = thread_id).count()

        data = {
           'is_unfavorited' : is_unfavorited,
           'counter' : counter
        }

        return JsonResponse(data)

def t_favorited(request):

    if request.session.has_key('username'):
        username = request.session['username']

        thread_id = request.GET.get('thread_id', None)

        thread = Thread.objects.get(id = thread_id)
        account = Account.objects.get(username = username)
        account_id = account.id

        s = ThreadFavoriter()
        s.thread = thread
        s.account = account
        s.save()


        is_favorited = ThreadFavoriter.objects.filter(thread_id = thread_id , account_id = account_id).exists()

        counter = ThreadFavoriter.objects.filter(thread_id = thread_id).count()

        data = {
           'is_favorited' : is_favorited,
           'counter' : counter
        }

        return JsonResponse(data)



def c_unfavorited(request):

    if request.session.has_key('username'):
        username = request.session['username']

        comment_id = request.GET.get('comment_id', None)

        account = Account.objects.get(username = username)
        account_id = account.id

        d = CommentFavoriter.objects.get(comment_id = comment_id , account_id = account_id)
        d.delete()

        is_unfavorited= CommentFavoriter.objects.filter(comment_id = comment_id , account_id = account_id).exists()

        counter = CommentFavoriter.objects.filter(comment_id = comment_id).count()

        data = {
           'is_unfavorited' : is_unfavorited,
           'counter' : counter
        }

        return JsonResponse(data)

def c_favorited(request):

    if request.session.has_key('username'):
        username = request.session['username']

        comment_id = request.GET.get('comment_id', None)

        comment = Comment.objects.get(id = comment_id)
        account = Account.objects.get(username = username)
        account_id = account.id

        s = CommentFavoriter()
        s.comment = comment
        s.account = account
        s.save()


        is_favorited = CommentFavoriter.objects.filter(comment_id = comment_id , account_id = account_id).exists()

        counter = CommentFavoriter.objects.filter(comment_id = comment_id).count()

        data = {
           'is_favorited' : is_favorited,
           'counter' : counter
        }

        return JsonResponse(data)






def r_unfavorited(request):

    if request.session.has_key('username'):
        username = request.session['username']

        reply_id = request.GET.get('reply_id', None)

        account = Account.objects.get(username = username)
        account_id = account.id

        d = ReplyFavoriter.objects.get(reply_id = reply_id , account_id = account_id)
        d.delete()

        is_unfavorited= ReplyFavoriter.objects.filter(reply_id = reply_id , account_id = account_id).exists()

        counter = ReplyFavoriter.objects.filter(reply_id = reply_id).count()

        data = {
           'is_unfavorited' : is_unfavorited,
           'counter' : counter
        }

        return JsonResponse(data)

def r_favorited(request):

    if request.session.has_key('username'):
        username = request.session['username']

        reply_id = request.GET.get('reply_id', None)

        reply = Reply.objects.get(id = reply_id)
        account = Account.objects.get(username = username)
        account_id = account.id

        s = ReplyFavoriter()
        s.reply = reply
        s.account = account
        s.save()


        is_favorited = ReplyFavoriter.objects.filter(reply_id = reply_id , account_id = account_id).exists()

        counter = ReplyFavoriter.objects.filter(reply_id = reply_id).count()

        data = {
           'is_favorited' : is_favorited,
           'counter' : counter
        }

        return JsonResponse(data)


def favorites(request):

    if request.session.has_key('username'):
        username = request.session['username']

        template_name = 'federal/favorites.html'

        account = Account.objects.get(username = username)
        account_id = account.id

        thread_cache = []
        comment_cache = []
        reply_cache = []

        thread_favorites = ThreadFavoriter.objects.filter(account_id = account_id)[:3]

        for thread in thread_favorites:

            thread_id = thread.thread_id
            thread_post = Thread.objects.get(id = thread_id)

            thread_cache.append(thread_post)


        comment_favorites = CommentFavoriter.objects.filter(account_id = account_id)[:3]

        for comment in comment_favorites:

            comment_id = comment.comment_id
            comment_post = Comment.objects.get(id = comment_id)

            comment_cache.append(comment_post)


        reply_favorites = ReplyFavoriter.objects.filter(account_id = account_id)[:3]

        for reply in reply_favorites:

            reply_id = reply.reply_id
            reply_post = Reply.objects.get(id = reply_id)

            reply_cache.append(reply_post)

        context = {
            'thread_cache': thread_cache,
            'comment_cache': comment_cache,
            'reply_cache' : reply_cache
        }

        return render(request, template_name, context)



class ThreadfavoriteView(View):

    template_name ='federal/threadfavorite.html'
    is_logged_in = False

    def get(self,request):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        account = Account.objects.get(username=username)

        account_id = account.id
        favorite_register = ThreadFavoriter.objects.filter(account_id = account_id)

        thread_cache = []

        for favorite in favorite_register:

            thread_id = favorite.thread_id
            thread_register = Thread.objects.get(id = thread_id)

            thread_cache.append(thread_register)




        content_cache = []
        content = {}

        for thread in thread_cache:


            thread_post = thread.thread
            id = thread.id
            date = thread.date

            account_id = thread.account_id
            account = Account.objects.get(id=account_id)

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)
            position = get_position.position

            my_id = Account.objects.get(username = username);
            my_id = my_id.id

            if_favorited = ThreadFavoriter.objects.filter(thread_id = id , account_id = my_id).exists()

            favorite_count = ThreadFavoriter.objects.filter(thread_id = id).count()

            context_list = {
                'id' : id,
                'thread_post' : thread_post,
                'date' : date,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'if_favorited' : if_favorited,
                'favorite_count' : favorite_count
            }

            content_cache.append(context_list)

        content = {
            'content_cache':content_cache,
            'is_logged_in' : is_logged_in
        }


        return render(request ,self.template_name,content)






class CommentfavoriteView(View):

        template_name = 'federal/commentfavorite.html'
        is_logged_in = False

        def get(self, request):

            if request.session.has_key('username'):
                username = request.session['username']
                is_logged_in = True
            else :
                is_logged_in = False

            account = Account.objects.get(username=username)

            account_id = account.id
            favorite_register = CommentFavoriter.objects.filter(account_id = account_id)

            comment_cache = []

            for favorite in favorite_register:

                comment_id = favorite.comment_id
                comment_register = Comment.objects.get(id = comment_id)

                comment_cache.append(comment_register)

            content_cache = []
            content = {}

            for comment in comment_cache:

                comment_post = comment.comment
                id = comment.id
                account_id = comment.account_id
                date = comment.date
                account = Account.objects.get(id=account_id)

                thread_id =  comment.thread_id
                thread = Thread.objects.get(id = thread_id)
                thread_id = thread.id
                thread_post = thread.thread

                firstname = account.firstname
                lastname = account.lastname
                position_id = account.position_id
                display_pic = account.display_pic

                get_position = Position.objects.get(id = position_id)

                position = get_position.position

                my_id = Account.objects.get(username = username);
                my_id = my_id.id

                if_favorited = CommentFavoriter.objects.filter(comment_id = id , account_id = my_id).exists()

                favorite_count = CommentFavoriter.objects.filter(comment_id = id).count()

                context_list = {
                    'id' : id,
                    'comment_post' : comment_post,
                    'date' : date,
                    'thread_id' : thread_id,
                    'thread_post' : thread_post,
                    'display_pic' : display_pic,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'position' : position,
                    'if_favorited' : if_favorited,
                    'favorite_count' : favorite_count
                }

                content_cache.append(context_list)

            content = {
                'content_cache':content_cache,
                'is_logged_in' : is_logged_in
            }


            return render(request, self.template_name, content)


class ReplyfavoriteView(View):

    template_name = 'federal/replyfavorite.html'
    is_logged_in = False

    def get(self, request):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        account = Account.objects.get(username=username)

        account_id = account.id
        favorite_register = ReplyFavoriter.objects.filter(account_id = account_id)

        reply_cache = []

        for favorite in favorite_register:

            reply_id = favorite.reply_id
            reply_register = Reply.objects.get(id = reply_id)

            reply_cache.append(reply_register)

        content_cache = []
        content = {}

        for reply in reply_cache:

            reply_post = reply.reply
            id = reply.id
            date = reply.date
            account_id = reply.account_id
            account = Account.objects.get(id=account_id)

            comment_id =  reply.comment_id
            comment = Comment.objects.get(id = comment_id)
            comment_id = comment.id
            comment_post = comment.comment

            thread_id =  comment.thread_id
            thread = Thread.objects.get(id = thread_id)
            thread_id = thread.id
            thread_post = thread.thread

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)

            position = get_position.position

            my_id = Account.objects.get(username = username);
            my_id = my_id.id

            if_favorited = ReplyFavoriter.objects.filter(reply_id = id , account_id = my_id).exists()

            favorite_count = ReplyFavoriter.objects.filter(reply_id = id).count()

            context_list = {
                'id' : id,
                'reply_post' : reply_post,
                'date' : date,
                'comment_id' : comment_id,
                'comment_post' : comment_post,
                'thread_id' : thread_id,
                'thread_post' : thread_post,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'if_favorited' : if_favorited,
                'favorite_count' : favorite_count
            }

            content_cache.append(context_list)

        content = {
            'content_cache':content_cache,
            'is_logged_in':is_logged_in
        }


        return render(request, self.template_name, content)



class ProfileView(View):

    form_class = ProfileTemplate
    template_name = 'federal/profile.html'
    is_logged_in = False

    def get(self,request):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        account = Account.objects.get(username=username)
        account_id = account.id

        my_position_id = account.position_id
        my_position = Position.objects.get(id = my_position_id)

        thread_list = Thread.objects.filter(account_id = account_id)

        content_cache = []
        content = {}

        for thread in thread_list:

            thread_post = thread.thread
            id = thread.id
            date = thread.date



            if len(thread_post.split()) >= 50:
                is_long = 1

            else:
                is_long = 0

            account_id = thread.account_id
            account = Account.objects.get(id=account_id)

            firstname = account.firstname
            lastname = account.lastname
            position_id = account.position_id
            display_pic = account.display_pic

            get_position = Position.objects.get(id = position_id)
            position = get_position.position

            my_id = Account.objects.get(username = username);
            my_id = my_id.id

            if_favorited = ThreadFavoriter.objects.filter(thread_id = id , account_id = my_id).exists()

            favorite_count = ThreadFavoriter.objects.filter(id = id).count()

            thread_media = Media.objects.filter(thread_id = id)[:1]

            context_list = {
                'id' : id,
                'thread_post' : thread_post,
                'date' : date,
                'is_long' : is_long,
                'firstname' : firstname,
                'lastname' : lastname,
                'position' : position,
                'display_pic' : display_pic,
                'thread_media' : thread_media,
                'if_favorited' : if_favorited,
                'favorite_count' : favorite_count
            }

            content_cache.append(context_list)

        form=self.form_class(None)

        content = {
            'form' : form,
            'account' : account,
            'my_position' : my_position,
            'content_cache' : content_cache,
            'is_logged_in' : is_logged_in
        }
        return render(request ,self.template_name,content)




    def post(self,request):

        if request.session.has_key('username'):
            username = request.session['username']
            is_logged_in = True
        else :
            is_logged_in = False

        form=self.form_class(request.FILES)

        if form.is_valid():
            account = Account.objects.get(username = username)

            my_position_id = account.position_id
            my_position = Position.objects.get(id = my_position_id)

            account.display_pic = request.FILES['display_pic']
            file_type = account.display_pic.url.split('.')[-1]
            file_type = file_type.lower()

            if file_type not in IMAGE_FILE_TYPES:
                account = Account.objects.get(username=username)
                account_id = account.id

                thread_list = Thread.objects.filter(account_id = account_id)

                content_cache = []
                content = {}

                for thread in thread_list:


                    thread_post = thread.thread
                    id = thread.id
                    date = thread.date

                    if len(thread_post.split()) >= 50:
                        is_long = 1

                    else:
                        is_long = 0

                    account_id = thread.account_id
                    account = Account.objects.get(id=account_id)

                    firstname = account.firstname
                    lastname = account.lastname
                    position_id = account.position_id
                    display_pic = account.display_pic

                    get_position = Position.objects.get(id = position_id)
                    position = get_position.position

                    my_id = Account.objects.get(username = username);
                    my_id = my_id.id

                    if_favorited = ThreadFavoriter.objects.filter(thread_id = id , account_id = my_id).exists()

                    favorite_count = ThreadFavoriter.objects.filter(id = id).count()

                    thread_media = Media.objects.filter(thread_id = id)[:1]

                    context_list = {
                        'id' : id,
                        'thread_post' : thread_post,
                        'date' : date,
                        'is_long' : is_long,
                        'firstname' : firstname,
                        'lastname' : lastname,
                        'position' : position,
                        'display_pic' : display_pic,
                        'if_favorited' : if_favorited,
                        'favorite_count' : favorite_count,
                        'thread_media' : thread_media,
                        'err_msg' : 'Display picture must be PNG JPG OR JPEG'
                    }

                    content_cache.append(context_list)

                form=self.form_class(None)

                content = {
                    'form' : form,
                    'account' : account,
                    'my_position' : my_position,
                    'content_cache' : content_cache,
                    'is_logged_in' : is_logged_in
                }
                return render(request ,self.template_name,content)

            account.save()

            account = Account.objects.get(username=username)
            account_id = account.id

            my_position_id = account.position_id
            my_position = Position.objects.get(id = my_position_id)

            thread_list = Thread.objects.filter(account_id = account_id)

            content_cache = []
            content = {}

            for thread in thread_list:


                thread_post = thread.thread
                id = thread.id
                date = thread.date



                if len(thread_post.split()) >= 50:
                    is_long = 1

                else:
                    is_long = 0

                account_id = thread.account_id
                account = Account.objects.get(id=account_id)

                firstname = account.firstname
                lastname = account.lastname
                position_id = account.position_id
                display_pic = account.display_pic

                get_position = Position.objects.get(id = position_id)
                position = get_position.position

                my_id = Account.objects.get(username = username);
                my_id = my_id.id

                if_favorited = ThreadFavoriter.objects.filter(thread_id = id , account_id = my_id).exists()

                favorite_count = ThreadFavoriter.objects.filter(id = id).count()

                thread_media = Media.objects.filter(thread_id = id)[:1]

                context_list = {
                    'id' : id,
                    'thread_post' : thread_post,
                    'date' : date,
                    'is_long' : is_long,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'position' : position,
                    'display_pic' : display_pic,
                    'thread_media' : thread_media,
                    'if_favorited' : if_favorited,
                    'favorite_count' : favorite_count
                }

                content_cache.append(context_list)

            form=self.form_class(None)

            content = {
                'form' : form,
                'account' : account,
                'my_position' : my_position,
                'content_cache' : content_cache,
                'is_logged_in' : is_logged_in
            }
            return render(request ,self.template_name,content)





class FeedbackView(View):

    form_class = FeedbackTemplate
    form_class_new = FeedbackNewTemplate
    template_name = 'federal/feedback.html'

    def get(self,request):

        if request.session.has_key('username'):
                username = request.session['username']

                form=self.form_class(None)

                content = {
                    'form' : form
                }

                return render(request ,self.template_name,content)


        form=self.form_class_new(None)

        content = {
            'form' : form
        }

        return render(request ,self.template_name,content)




    def post(self,request):

        form=self.form_class(request.POST)

        if form.is_valid():

            if request.session.has_key('username'):
                    username = request.session['username']

                    feed = form.cleaned_data['feed']

                    account = Account.objects.get(username = username)

                    firstname = account.firstname
                    lastname = account.lastname

                    feedback = Feedback()

                    feedback.firstname = firstname
                    feedback.lastname = lastname
                    feedback.feed = feed

                    feedback.save()

                    form=self.form_class(None)

                    content = {
                        'form' : form
                    }

                    return render(request ,self.template_name,content)



            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            feed = form.cleaned_data['feed']

            feedback = Feedback()

            feedback.firstname = firstname
            feedback.lastname = lastname
            feedback.feed = feed

            feedback.save()

            form=self.form_class_new(None)

            content = {
                'form' : form
            }

            return render(request ,self.template_name,content)




def about(request):

    template_name = 'federal/about.html'

    return render(request , template_name)


def terms(request):

    template_name = 'federal/terms.html'

    return render(request , template_name)


def respect_policy(request):

    template_name = 'federal/respect_policy.html'

    return render(request , template_name)


def content_policy(request):

    template_name = 'federal/content_policy.html'

    return render(request , template_name)


    

class ForgotPasswordView(View):

    form_class = ForgotPasswordTemplate
    template_name = 'federal/forgot_password.html'

    def get(self,request):

        form=self.form_class(None)

        context = {
            'form' : form
        }

        return render(request , self.template_name, context)

    def post(self,request):

        form=self.form_class(request.POST)

        if form.is_valid():

            username = reply = form.cleaned_data['username']
            password = username

            send_mail(
                'Subject here',
                'Here is the message.',
                'iamcoole007@gmail.com',
                ['dretzam@gmail.com'],
                fail_silently=False,
            )

            forgot_database = ForgotPassword
            forgot_database.username = username
            forgot_database.reset_password = reset_password



        form=self.form_class(None)

        context = {
            'form' : form
        }

        return render(request , self.template_name, context)


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('federal:index')
