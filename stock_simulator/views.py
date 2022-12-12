from django.shortcuts import render, redirect
from django.http import HttpResponse as response
from django.contrib.auth import authenticate, login, logout
from . models import User, Owned, Transactions
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from . helpers import apology, lookup, usd
import django.forms as forms


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    confirmation = forms.CharField()

class BuyForm(forms.Form):
    symbol = forms.CharField()
    shares = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

@require_http_methods(['GET'])
@login_required
def index(request):
    user = request.user
    owned = Owned.objects.filter(user_id=user)
    data = []
    total_stocks = 0
    for row in owned:
        symbol_data = lookup(row.symbol)
        price = symbol_data['price']
        shares = row.shares
        total = price * shares
        dict = {
            'symbol': row.symbol,
            'name': symbol_data['name'],
            'shares': shares,
            'price': usd(price),
            'total': usd(total)
        }
        total_stocks = total_stocks + (symbol_data['price'] * row.shares)
        data.append(dict)
    cash = float(user.cash)
    cash_usd = usd(cash)
    grand_total = cash + total_stocks
    gt_usd = usd(grand_total)

    return render(request, 'index.html', {'data': data, 'cash_usd': cash_usd, 'gt_usd': gt_usd})

@require_http_methods(['GET', 'POST'])
@login_required
def buy(request):
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            shares = form.cleaned_data['shares']

            if not symbol or lookup(symbol) is None:
                return apology("Enter valid stock symbol")
            if not shares or not shares.isdigit():
                return apology("Enter positive integer")
            elif int(shares) <= 0:
                return apology("Enter positive integer")

            shares = int(shares)
            symbol_data = lookup(symbol)
            price = float(symbol_data["price"])
            user = request.user
            owned = Owned.objects.filter(user_id=user.id)
            cash = float(user.cash)
            trigger = 0
            
            if cash < (price * shares):
                return apology("Insufficient funds")
            for i in range(len(owned)):
                if symbol == owned[i].symbol:
                    trigger = 1
                    owned[i].shares = owned[i].shares + shares
                    owned[i].save()
            if trigger != 1:
                o = Owned(user_id=user, symbol=symbol, shares=shares)
                o.save()
            cash = cash - (price * shares)
            user.cash = cash
            user.save()
            t = Transactions(user_id=user, symbol=symbol, price=price, shares=shares, type="buy")
            t.save()

            return redirect('/')
    return render(request, 'buy.html')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['confirmation']

            if not username:
                return apology("Input valid username")
            elif not password or not confirmation:
                return apology("Input password and confirmation")
            elif password != confirmation:
                return apology("Passwords do not match")
            
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'register.html')

@require_http_methods(['GET', 'POST'])
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    return render(request, 'login.html')

@require_http_methods(['GET'])
def logout_user(request):
    logout(request)
    return redirect('/login')
