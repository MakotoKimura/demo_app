from django.shortcuts import render, redirect
from .forms import InputForm
from .models import Customers
from sklearn.externals import joblib
import numpy as np

# globalに置いておくと、処理が軽くて済む
loaded_model = joblib.load('demo_app/demo_model.pkl')

# Create your views here.
def index(request):
    return render(request, 'demo_app/index.html', {})

def input_form(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()  # 保存
            return redirect('result')
    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html', {'form':form})

def result(request):
    # 最新の登録者のデータを取得
    _data = Customers.objects.order_by('id').reverse().values_list\
        ('limit_balance', 'sex', 'education', 'marriage', 'age', 'pay_0', 'pay_2', 'pay_3', 'pay_4', 'pay_5', 'pay_6', 'bill_amt_1', 'pay_amt_1', 'pay_amt_2', 'pay_amt_3', 'pay_amt_4', 'pay_amt_5', 'pay_amt_6')

    x = np.array([_data[0]])
    y = loaded_model.predict(x)
    y_proba = loaded_model.predict_proba(x)
    y_proba = y_proba * 100

    # 結果に基づいてコメントを返す
    if y[0] == 0:
        if y_proba[0][y[0]] > 75:
            comment = 'この方への貸し出しは危険です'
        else:
            comment = 'この方への貸し出しは要検討です'
    else:
        if y_proba[0][y[0]] > 75:
            comment = 'この方への貸し出しは全く問題ありません'
        else:
            comment = 'この方への貸し出しは問題ないでしょう'

    return render(request, 'demo_app/result.html', {'y':y[0], 'y_proba':round(y_proba[0][y[0]], 2), 'comment':comment}) # commentを追加
    # 推論結果の保存
    _customer = Customers.objects.order_by('id').reverse()[0] # Customerの切り出し
    _customer.proba = _y_proba[0][y[0]]
    _customer.result = y[0]
    _customer.comment = comment
    _customer.save() # データを保存
'''
def result(request):
    # DBからデータを取得
    _data = Customers.objects.order_by('id').reverse().values_list\
    ('limit_balance', 'sex', 'education', 'marriage', 'age', 'pay_0', 'pay_2', \
    'pay_3', 'pay_4', 'pay_5', 'pay_6', 'bill_amt_1', 'pay_amt_1', 'pay_amt_2', \
    'pay_amt_3', 'pay_amt_4', 'pay_amt_5', 'pay_amt_6')
    x = np.array([_data[0]])
    y = loaded_model.predict(x)
    y_proba = loaded_model.predict_proba(x)
    _y_proba = y_proba * 100
    # return render(request, 'demo_app/result.html', {'y':y[0], 'y_proba':round(y_proba[0][y[0]], 2)})
    if y[0] == 0:
        if y_proba[0][y[0]] > 0.75:
            comment = 'この方への貸し出しは危険です'
        else:
            comment = 'この方への貸し出しは要検討です'
    else:
        if y_proba[0][y[0]] > 0.75:
            comment = 'この方への貸し出しは全く問題ありません'
        else:
            comment = 'この方への貸し出しは問題ないでしょう'
    return render(request, 'demo_app/result.html', {'y':y[0], 'y_proba':round(_y_proba[0][y[0]], 2), 'comment':comment})
    # 推論結果の保存
    _customer = Customers.objects.order_by('id').reverse()[0] # Customerの切り出し
    _customer.proba = _y_proba[0][y[0]]
    _customer.result = y[0]
    _customer.comment = comment
    _customer.save() # データを保存
'''

def history(request):
    if request.method == 'POST':
        d_id = request.POST
        d_customer = Customers.objects.filter(id=d_id['d_id'])
        d_customer.delete()
        customers = Customers.objects.all()
        return render(request, 'demo_app/history.html', {'customers':customers})
    else:
        customers = Customers.objects.all()
        return render(request, 'demo_app/history.html', {'customers':customers})

# W9補講
def calculate(request):
    if request.method == 'POST':
        nums = request.POST
        ans = int(nums['num1']) + int(nums['num2'])
        print(ans)
        return render(request, 'demo_app/calculate.html', {'answer':ans})
    else:
        return render(request, 'demo_app/calculate.html', {})
