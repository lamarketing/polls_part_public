from rest_framework.serializers import ModelSerializer, SlugRelatedField

from polls.models import Polls, Questions, Answers, PollsResults


class AnswersSerializer(ModelSerializer):

    class Meta:
        model = Answers
        fields = ['id', 'name']


class QuestionsSerializer(ModelSerializer):
    answers = AnswersSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ['id', 'name', 'answers', 'file']


class PollsListSerializer(ModelSerializer):
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Polls
        fields = ['id', 'name', 'description', 'questions']


class PollsResultsSerializer(ModelSerializer):

    class Meta:
        model = PollsResults
        fields = ['poll', 'result']

    # def validate(self, attrs):
    #     print(self)
    #
    # def create(self, validated_data):
    #     print(self)