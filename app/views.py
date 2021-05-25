from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    source = request.GET.get('from-landing')
    counter_click[source] += 1
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    return render(request, 'index.html')


def landing(request):
    mode = request.GET.get('ab_test-arg')
    counter_show[mode] += 1
    if mode == 'test':
        return render(request, 'landing_alternate.html')
    if mode == 'original':
        # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
        # в зависимости от GET параметра ab-test-arg
        # который может принимать значения original и test
        # Так же реализуйте логику подсчета количества показов
        return render(request, 'landing.html')
    else:
        return HttpResponse('НЕ ВЕРНО УКАЗАНА СТРАНИЦА!!!')


def stats(request):
    conversion = {'test': 'Показов не было', 'original': 'Показов не было'}
    for name in counter_show:
        if counter_show[name] == 0:
            continue
        else:
            conversion[name] = counter_click[name] / counter_show[name]
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    return render(request, 'stats.html', context={
        'test_conversion': conversion['test'],
        'original_conversion': conversion['original'],
    })
