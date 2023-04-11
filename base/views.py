from datetime import timedelta

import stripe
from django.shortcuts import render, redirect

# Create your views here
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from base.forms import MyForm, TeacherForm
from base.models import Student, Teacher
from base.serializers import TeacherSerializer, StudentSerializer
from base.tasks import hello
from hi_itis import settings


def my_view(request):
    print(request.method, request.path)
    if request.method == 'GET':
        student = Student.objects.all()
        respones_data = '; '.join(', '.join(value) for value in student.values_list('name', 'surname', 'group__title'))
        return HttpResponse(respones_data)


class MyView(View):
    def get(self, request):
        students = Student.objects.all()

        form = MyForm()

        context = {'students': students, 'form': form}

        return render(request, 'hello.html', context=context)

    def post(self, request):
        print(request.POST)
        form = MyForm(request.POST)
        if form.is_valid():
            student = Student.objects.create(**form.cleaned_data)
            return redirect('/hello')


class TeacherView(View):
    def get(self, request):
        hello.apply_async(eta=now() + timedelta(seconds=15))

        teachers = Teacher.objects.all()

        form = TeacherForm()

        context = {'teachers': teachers, 'form': form}

        return render(request, 'teachers.html', context=context)

    def post(self, request):
        print(request.POST)
        form = TeacherForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            teacher = form.save(commit=False)
            teacher.save()
            form.save_m2m()

            return redirect('/teachers')


# ViewSets define the view behavior.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


# ViewSets define the view behavior.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.order_by('-id')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class HomePageView(TemplateView):
    template_name = 'home.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        print(stripe_config)
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1Mt6esKy1JgzaB6ftueqnCIq',
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(View):
    def get(self, request):
        print(request.GET)
        session_id = request.GET.get('session_id', '')
        stripe.api_key = settings.STRIPE_SECRET_KEY

        checkout_session = stripe.checkout.Session.retrieve(
            session_id,
        )
        print(checkout_session)
        return render(request, 'success.html')


class CancelledView(TemplateView):
    template_name = 'cancelled.html'
