from rest_framework import serializers

from .models import SurveyModel, AskModel, AskAnswerSelectionOnListAnswerModel, ResultModel, ResultAnswerModel
from UserProfileApp.models import User


def getIDList(data):
    itemList = []
    for i, item in enumerate(data):
        if 'id' in item:
            itemList.append(item['id'])
    return itemList


def validateAsk(data, isCreate=True):
    answerInput = data.get('answerInput', None)
    isMulti = data.get('isMulti', None)
    answerListData = data.get('answerListData', None)
    if (isMulti or answerListData) and answerInput:
        raise serializers.ValidationError({'detail': "Вы не можете создать ответ с выбором и с текстовым вводом!"})
    if isCreate:
        if not answerInput and not answerListData:
            raise serializers.ValidationError({'detail': "Ни один из вариантов ответов не представлен!"})
    if answerListData:
        validAnswerCount = 0
        for i, item in enumerate(answerListData):
            validStatus = item.get('validStatus', None)
            answer = item.get('answer', None)
            if validStatus:
                validAnswerCount += 1
            if not validStatus or not answer:
                raise serializers.ValidationError(
                    {'detail': "В одном из вариантов на выбор не предоставлены требуемые данные!"})
        if len(answerListData) < 2:
            raise serializers.ValidationError(
                {'detail': "При использовании варианта ответа с выбором, должно быть минимум 2 ответа!"})
        if validAnswerCount == 0:
            raise serializers.ValidationError(
                {'detail': "Вы должны указать хотя бы один верный ответ!"})
        if not isMulti and validAnswerCount > 1:
            raise serializers.ValidationError(
                {'detail': "Вы не можете добавить несколько верных ответов, если не установлен множественный выбор!"})
    return data


class AskAnswerListDetailManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskAnswerSelectionOnListAnswerModel
        fields = ('id', 'answer', 'validStatus',)


class AskAnswerListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskAnswerSelectionOnListAnswerModel
        fields = ('id', 'answer',)


class AskAnswerListCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=AskAnswerSelectionOnListAnswerModel.objects.all())

    class Meta:
        model = AskAnswerSelectionOnListAnswerModel
        fields = ('id',)


class AskDetailManageSerializer(serializers.ModelSerializer):
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')
    answerListData = serializers.JSONField(required=False, write_only=True)

    class Meta:
        model = AskModel
        fields = ('id', 'ask', 'isMulti', 'answerList', 'answerListData', 'answerInput',)

    def get_answerList(self, instance):
        if instance.answerList.count() > 0:
            return AskAnswerListDetailManageSerializer(many=True, instance=instance.answerList).data
        else:
            return None

    def validate(self, data):
        return validateAsk(data=data, isCreate=False)

    def update(self, instance, validated_data):
        answerListData = validated_data.pop('answerListData', None)
        if 'ask' in validated_data:
            instance.ask = validated_data['ask']
        if answerListData and not 'answerInput' in validated_data:
            askAnswerListID = getIDList(instance.answerList.all().values('id'))
            instance.answerList.clear()
            for i, item in enumerate(answerListData):
                if 'id' in item and item['id'] in askAnswerListID:
                    askAnswerList = AskAnswerSelectionOnListAnswerModel.objects.get(id=item['id'])
                    if 'answer' in item:
                        askAnswerList.answer = item['answer']
                    if 'validStatus' in item:
                        askAnswerList.validStatus = item['validStatus']
                    askAnswerList.save()
                    instance.answerList.add(askAnswerList)
                else:
                    instance.answerList.add(AskAnswerSelectionOnListAnswerModel.objects.create(**item))
        if 'answerInput' in validated_data and not answerListData:
            instance.answerInput = validated_data['answerInput']
        instance.save()
        return instance


class AskDetailSerializer(serializers.ModelSerializer):
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')
    answerInput = serializers.SerializerMethodField(source='get_answerInput')

    class Meta:
        model = AskModel
        fields = ('id', 'ask', 'isMulti', 'answerList', 'answerInput',)

    def get_answerList(self, instance):
        if instance.answerList.count() > 0:
            return AskAnswerListDetailSerializer(many=True, instance=instance.answerList).data
        else:
            return None

    def get_answerInput(self, instance):
        if instance.answerInput:
            return True
        else:
            return None


class AskCreateSerializer(serializers.ModelSerializer):
    ask = serializers.CharField(required=True)
    answerListData = serializers.JSONField(required=False, write_only=True)
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')

    class Meta:
        model = AskModel
        fields = ('id', 'ask', 'isMulti', 'answerList', 'answerListData', 'answerInput',)

    def validate(self, data):
        return validateAsk(data)

    def create(self, validated_data):
        answerListData = validated_data.pop('answerListData', None)
        ask = AskModel.objects.create(**validated_data)
        if answerListData:
            for i, item in enumerate(answerListData):
                ask.answerList.add(AskAnswerSelectionOnListAnswerModel.objects.create(**item))
        ask.save()
        return ask

    def get_answerList(self, instance):
        if instance.answerList.count() > 0:
            return AskAnswerListDetailManageSerializer(many=True, instance=instance.answerList).data
        else:
            return None


class SurveyDetailManageSerializer(serializers.ModelSerializer):
    askList = AskDetailManageSerializer(read_only=True, many=True)
    startDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SurveyModel
        fields = ('id', 'name', 'description', 'startDate', 'endDate', 'askList',)


class SurveyDetailSerializer(serializers.ModelSerializer):
    askList = AskDetailSerializer(many=True)

    class Meta:
        model = SurveyModel
        fields = ('id', 'name', 'description', 'startDate', 'endDate', 'askList',)


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyModel
        fields = ('id', 'name', 'description', 'startDate', 'endDate',)


class SurveyCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    startDate = serializers.DateTimeField(required=True)
    endDate = serializers.DateTimeField(required=True)

    class Meta:
        model = SurveyModel
        fields = ('id', 'name', 'description', 'startDate', 'endDate',)


class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyModel
        fields = ('id', 'name', 'description', 'startDate', 'endDate',)


class ResultAnswerSerializer(serializers.ModelSerializer):
    ask = serializers.SlugRelatedField(read_only=True, slug_field='ask')
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')

    class Meta:
        model = ResultAnswerModel
        fields = ('id', 'ask', 'answerList', 'answerInput', 'answerValid',)

    def get_answerList(self, instance):
        if instance.answerList.count() > 0:
            return AskAnswerListDetailSerializer(many=True, instance=instance.answerList).data
        else:
            return None


class ResultAnswerCreateSerializer(serializers.ModelSerializer):
    ask = serializers.PrimaryKeyRelatedField(queryset=AskModel.objects.all())
    answerList = AskAnswerListCreateSerializer(many=True, required=False)
    answerInput = serializers.CharField(required=False)

    class Meta:
        model = ResultAnswerModel
        fields = ('id', 'ask', 'answerList', 'answerInput')


class ResultAnswerDetailSerializer(serializers.ModelSerializer):
    ask = AskDetailSerializer(required=False)
    answerList = serializers.SerializerMethodField(read_only=True, source='get_answerList')
    answerInput = serializers.SerializerMethodField(read_only=True, source='get_answerInput')
    answerValid = serializers.BooleanField(required=False)

    class Meta:
        model = ResultAnswerModel
        fields = ('id', 'ask', 'answerList', 'answerInput', 'answerValid',)

    def get_answerList(self, instance):
        if instance.answerList.count() > 0:
            return AskAnswerListDetailSerializer(many=True, instance=instance.answerList).data
        else:
            return None

    def get_answerInput(self, instance):
        if instance.answerInput:
            return instance.answerInput
        else:
            return None


class ResultSerializer(serializers.ModelSerializer):
    survey = SurveySerializer()
    resultList = ResultAnswerDetailSerializer(many=True, required=True)

    class Meta:
        model = ResultModel
        fields = ('id', 'survey', 'isAnon', 'resultList',)


class ResultCreateSerializer(serializers.ModelSerializer):
    survey = serializers.PrimaryKeyRelatedField(queryset=SurveyModel.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    resultList = ResultAnswerCreateSerializer(many=True, required=True)

    class Meta:
        model = ResultModel
        fields = ('id', 'survey', 'user', 'isAnon', 'resultList',)

    def validate(self, data):
        askAnswerListID = getIDList(data['survey'].askList.all().values('id'))
        if len(askAnswerListID) != len(data['resultList']):
            raise serializers.ValidationError({'detail': "Не на все вопросы получены ответы!"})
        for i, item in enumerate(data['resultList']):
            ask = item['ask']
            answerInput = item.get('answerInput', None)
            answerList = item.get('answerList', None)
            if not answerInput and not answerList:
                raise serializers.ValidationError(
                    {'detail': "Вы не ответили на один из вопросов!"})
            if not ask.id in askAnswerListID:
                raise serializers.ValidationError({'detail': "Получен ответ на вопрос, не из опроса!"})
            else:
                askAnswerListID.remove(ask.id)
            if ((answerInput and ask.answerList.count()) or (answerList and ask.answerInput)) or (
                    (ask.isMulti or answerList) and answerInput):
                raise serializers.ValidationError(
                    {'detail': "Вы дали ответ не того типа!"})
            if answerList:
                answerListID = getIDList(ask.answerList.all().values('id'))
                for j, jtem in enumerate(answerList):
                    if not jtem['id'].id in answerListID:
                        raise serializers.ValidationError({'detail': "Ответ с выбором не из данного вопрос!"})
                    else:
                        answerListID.remove(jtem['id'].id)
        return data

    def create(self, validated_data):
        isAnon = validated_data.get('isAnon', False)
        user = validated_data.get('user', None)
        newResult = ResultModel.objects.create(survey=validated_data['survey'])
        if isAnon:
            newResult.isAnon = True
            newResult.user = None
        else:
            newResult.user = user
        for i, item in enumerate(validated_data['resultList']):
            newResultAnswer = ResultAnswerModel.objects.create(ask=item['ask'])
            newResult.resultList.add(newResultAnswer)
            newResult.save()
            answerInput = item.get('answerInput', None)
            answerList = item.get('answerList', None)
            if answerInput and item['ask'].answerInput:
                pass
                newResultAnswer.answerInput = answerInput
                if answerInput.lower() == item['ask'].answerInput.lower():
                    newResultAnswer.answerValid = True
            elif answerList and item['ask'].answerList:
                answerCount = 0
                askList = item['ask'].answerList.filter(validStatus=True)
                askListID = getIDList(askList.values('id'))
                for j, jtem in enumerate(answerList):
                    newResultAnswer.answerList.add(jtem['id'])
                    if jtem['id'].id in askListID:
                        answerCount += 1
                if (answerCount == len(askListID)) and (len(askListID) == len(answerList)):
                    newResultAnswer.answerValid = True
            newResultAnswer.save()
        return newResult