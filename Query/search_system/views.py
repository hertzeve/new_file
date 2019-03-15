from django.shortcuts import render

from search_system import models
from search_system.python_code import boolean_model_query
from search_system.python_code import highlighted
from search_system.python_code import vectors_query
from search_system.python_code import query_process
def search(request):
    return render(request, 'search_system/search_page.html')


def search_result(request):
    articles = []
    dict = {}
    search_query = request.POST["input_query"]
    model_select = request.POST["which_model"]
    search_query = search_query.strip()
    if search_query is "":
        return render(request, 'search_system/search_result.html', {'input_empty': 0})
    else:
        if model_select is "1":
            search_result, identify = boolean_model_query.main(search_query)
            if identify == 0:
                return render(request, 'search_system/search_result.html', {'article_dict': None})
            elif identify == 1:
                for ids in search_result:
                    int_ids = int(ids)
                    article = (models.Article.objects.get(pk=int_ids))
                    content = highlighted.highlight_one(article,search_query)
                    dict[article] = content
                return render(request, 'search_system/search_result.html', {'article_dict': dict})
            elif identify == 2:
                for ids in search_result:
                    int_ids = int(ids)
                    article = (models.Article.objects.get(pk=int_ids))
                    content = highlighted.highlight_andor(article,search_query)
                    dict[article] = content
                return render(request, 'search_system/search_result.html', {'article_dict': dict})
            elif identify == 3:
                for ids in search_result:
                    int_ids = int(ids)
                    article = (models.Article.objects.get(pk=int_ids))
                    content = highlighted.highlight_phrase(article, search_query)
                    dict[article] = content
                return render(request, 'search_system/search_result.html', {'article_dict': dict})

        elif model_select is "2":
            lem_query = query_process.lemmatizing(search_query)
            search_result = vectors_query.main(lem_query)
            if len(lem_query) == 1:
                for ids in search_result:
                    article = (models.Article.objects.get(pk=ids))
                    content = highlighted.highlight_one(article,search_query)
                    dict[article] = content
                return render(request, 'search_system/search_result.html', {'article_dict': dict})
            else:
                for ids in search_result:
                    # int_ids = int(ids)
                    article = (models.Article.objects.get(pk=ids))
                    content = highlighted.highlight_rankPhrase(article, search_query)
                    dict[article] = content
                return render(request, 'search_system/search_result.html', {'article_dict': dict})


def article_page(request, article_id):
    article= models.Article.objects.get(pk = article_id)
    return render(request, 'search_system/article_page.html', {'article': article})



