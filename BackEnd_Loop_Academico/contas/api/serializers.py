from rest_framework import serializers
from contas.models import Aluno, Perfil
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from turma.models import Turma
from django.contrib.auth import authenticate
class AtualizarFotoPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['fotoPerfil']

class PerfilSerializer(serializers.ModelSerializer):
    nome_do_aluno = serializers.CharField(source='aluno.nomeAluno', read_only=True)
    turma_aluno = serializers.SerializerMethodField()
    matricula_aluno = serializers.CharField(source='aluno.matricula', read_only=True)

    class Meta:
        model = Perfil
        fields = ['id', 'fotoPerfil', 'aluno', 'turma', 'nome_do_aluno', 'turma_aluno', 'matricula_aluno']

    def get_turma_aluno(self, obj):
        if obj.turma:
            return obj.turma.codicoTurma
        return 'Sem turma'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.turma is None:
            representation.pop('turma_aluno', None)
        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class AlunoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Aluno
        fields = ['id', 'user', 'nomeAluno', 'instituicao', 'matricula', 'email', 'turma', 'is_active', 'is_staff', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_data = {
            'username': validated_data['email'],
            'email': validated_data['email']
        }
        user = User.objects.create(**user_data)
        if password:
            user.set_password(password)
        user.save()

        aluno = Aluno.objects.create(
            user=user,
            nomeAluno=validated_data['nomeAluno'],
            instituicao=validated_data['instituicao'],
            matricula=validated_data['matricula'],
            email=validated_data['email'],
            turma=validated_data.get('turma'),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False)
        )
        return aluno

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = instance.user

        user.username = validated_data.get('email', user.username)
        user.email = validated_data.get('email', user.email)
        if password:
            user.set_password(password)
        user.save()

        instance.nomeAluno = validated_data.get('nomeAluno', instance.nomeAluno)
        instance.instituicao = validated_data.get('instituicao', instance.instituicao)
        instance.matricula = validated_data.get('matricula', instance.matricula)
        instance.email = validated_data.get('email', instance.email)
        instance.turma = validated_data.get('turma', instance.turma)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()

        return instance

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Aluno
        fields = ['nomeAluno', 'instituicao', 'matricula', 'email', 'password', 'turma']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        aluno = Aluno.objects.create(
            user=user,
            nomeAluno=validated_data['nomeAluno'],
            matricula=validated_data['matricula'],
            instituicao=validated_data['instituicao'],
            turma=validated_data.get('turma')
        )
        return aluno
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
            else:
                raise serializers.ValidationError("Credenciais inválidas")
        else:
            raise serializers.ValidationError("Campos de email e senha são obrigatórios")