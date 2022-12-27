from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import templates
from sudoku.models import Ranking
from .api.sudokus import Sudoku

from django.core import serializers

import json
import datetime

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    context = {}
    return render(request, 'sudoku/index.html',context)

def ranking(request):
    context = {}
    return render(request, 'sudoku/ranking.html',context)

def get_ranking_list(request):
    ranking_list = Ranking.objects.order_by('elapsed_time')[:100]
    ranking_data = serializers.serialize("json",ranking_list, fields=('name','elapsed_time'))
    ranking_data = json.loads(ranking_data)
    ranking_data = [{**item['fields'],**{"pk" : item['pk']}} for item in ranking_data]
    #** : 딕셔너리, * : 튜플
    ranking_data = {
        "data" : ranking_data
    }
    return JsonResponse(ranking_data)

def register_ranking(request):
    if 'elapsed_time' not in request.session:
        return JsonResponse({'status' : 'failed'})

    data = json.loads(request.body)
    name = data['name']
    elapsed_time = request.session['elapsed_time']

    datetime_args = elapsed_time//3600,(elapsed_time%3600)//60,elapsed_time%60
    d = datetime.time(datetime_args[0], datetime_args[1], datetime_args[2]) 

    ranking = Ranking(name = name, elapsed_time = d)
    ranking.save()

    return JsonResponse({'status' : 'success'})

#check_sudoku 함수는, 사용자가 json형식으로 데이터를 HTTP 프로토콜을 이용해서 보냄
def check_sudoku(request):
    sudoku_api = Sudoku()

    req_data = json.loads(request.body)
    #받은 데이터를 json.loads 함수를 이용해서 json -> 파이썬 dict로 변환을 수행

    if 'puzzle' not in req_data or 'elapsed_time' not in req_data:
        JsonResponse({'status' : "fail"})

    puzzle = req_data['puzzle']
    elapsed_time = req_data['elapsed_time'] #경과시간

    result = sudoku_api.sudoku_check(puzzle) #내가 푼 퍼즐 정답이 맞는지 틀린지 확인
    data = {} #data 딕셔너리
    if result == True:
        data['status'] = "clear" 
        request.session['status'] = "clear" #status창을 clear로
        request.session['elapsed_time'] = elapsed_time
    else:
        data['status'] = "fail"

    return JsonResponse(data)

def make_sudoku(request):
    sudoku_api = Sudoku()
    board = sudoku_api.generate_sudoku() # 스도쿠 퍼즐을 생성
    result = {
        'board' : board
    } # resulf 변수를 선언해서, 반환할 스도쿠 퍼즐 데이터를 생성

    return JsonResponse(result)
     # JsonResponse 함수를 이용해서 json 형식으로 변환해서 json 데이터가 담긴 HttpResponse을 리턴










