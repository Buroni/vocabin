from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .fields import Category
from .models import Sentence
from .serializers import UserSerializer, SentenceSerializer
from .sql import query_sentences
from .nlp import NLP
from .throttles import BurstRateThrottle


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

    @staticmethod
    def get_difficulty_from_score(score, language, categories):
        difficulties = NLP.get_avg_difficulties(language, categories)
        if score < difficulties[1]:
            return "easy"
        elif difficulties[1] <= score < difficulties[2]:
            return "moderate"
        else:
            return "difficult"


class SentenceFormsView(SentenceListMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [BurstRateThrottle]

    def get(self, request, language, word):
        nlp = NLP(language)
        categories = self.get_categories(request)
        response = {"sentences": []}
        difficulty = int(request.GET.get("difficulty")) if request.GET.get("difficulty") else None
        inflect = True if request.GET.get("inflect") == "true" else False
        word_forms = nlp.get_word_forms(word) if inflect else [word]
        res = query_sentences(word_forms, difficulty, categories, language)

        for w in word_forms:
            sentences_list = [{
                "source": s[2],
                "sentence": s[1],
                "id": s[0],
                "category": s[3]} for s in res if s[4] == w]
            entry = {"word": w, "pos": nlp.get_pos_tag(w), "sentences": sentences_list}
            response["sentences"].append(entry)
        response["forms"] = word_forms
        return Response(response)


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(('GET',))
def index(request):
    return Response({"version": "0.1", "is_authenticated": request.user.is_authenticated})

