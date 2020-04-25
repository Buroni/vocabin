import itertools
from django.contrib.auth.models import User
from django.http import HttpResponse
from google.cloud import translate_v2 as translate
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .fields import Category
from .models import Sentence
from .nlp import NLP
from .serializers import UserSerializer, SentenceSerializer
from .utils import wordtype2group
from .throttles import BurstRateThrottle, GCloudThrottle


class SentenceListMixin:

    @staticmethod
    def get_categories(request):
        category = request.query_params.get('category', None)
        categories = [category] if category else [Category.NEWS, Category.WEB]
        return categories

    @staticmethod
    def get_min_max_score(request, language, categories):
        nlp = NLP(language)
        difficulty = int(request.query_params.get('difficulty', -1))
        return nlp.get_min_max_score(difficulty, categories)


class SentenceFormsView(SentenceListMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [BurstRateThrottle]

    def get(self, request, language, word):
        nlp = NLP(language)
        word_forms = nlp.get_word_forms(word)
        response = {"forms": []}
        form_objs = []
        if not nlp.is_noun(word):
            word = word.lower()
        for w in word_forms:
            form_objs.append(self.make_form_obj(w, nlp))
        response["search_term"] = self.make_form_obj(word, nlp)
        search_form_group = response["search_term"]["group"]
        try:
            forms = sorted([f for f in form_objs if f["group"] == search_form_group], key=lambda k: k["word_type"])
            response["forms"] = [{
                "word_type": key,
                "group": wordtype2group(key),
                "results": list(group)} for (key, group) in itertools.groupby(forms, key=lambda k: k["word_type"])
            ]
        except NameError:
            response["forms"] = [{
                "word_type": "Unknown Type",
                "group": "unk",
                "results": [{"word": word, "pos": "", "word_type": "Unknown Type", "group": "unk"}]
            }]
        return Response(response)

    @staticmethod
    def make_form_obj(word, nlp):
        typ, group, pos = nlp.get_pos_tag(word)
        return {"word": word, "pos": pos, "word_type": typ, "group": group}


class SentenceListView(SentenceListMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [BurstRateThrottle]

    def get(self, request, language, word):
        nlp = NLP(language)
        categories = self.get_categories(request)
        difficulty = int(request.GET.get("difficulty")) if request.GET.get("difficulty") else None
        sentences = Sentence.objects.filter(
            content__regex=r"\b(" + word + r")\b",
            **nlp.build_difficulty_filter(difficulty),
            reports__lte=3,
            language__exact=language,
            category__in=categories
        )[:5]
        sentences_list = [{
            "word": word,
            "sentence": s.content,
            "id": s.ref_id,
            "category": s.category} for s in sentences]
        return Response({"sentences": sentences_list})


class SentenceDetailView(GenericAPIView):
    serializer_class = SentenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [BurstRateThrottle]

    def get(self, request, ref_id):
        sentence = self.get_object(ref_id)
        serializer = SentenceSerializer(sentence)
        return Response(serializer.data)

    def get_object(self, ref_id):
        return Sentence.objects.get(ref_id=ref_id)


class SentenceReportView(GenericAPIView):
    serializer_class = SentenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [BurstRateThrottle]

    def post(self, request):
        s_id = request.data["id"]
        s = Sentence.objects.get(ref_id=s_id)
        s.reports += 1
        s.save()
        return HttpResponse(status=204)


# Throttled wrapper around the Google Translate API
class SentenceTranslateView(GenericAPIView):
    translate_client = translate.Client()
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [GCloudThrottle]

    def post(self, request):
        sentence = request.data["sentence"]
        target_lang = request.data["target_lang"]
        result = self.translate_client.translate(sentence, target_language=target_lang)
        return Response({"translation": result["translatedText"]})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(('GET',))
def index(request):
    return Response({"version": "0.1", "is_authenticated": request.user.is_authenticated})

