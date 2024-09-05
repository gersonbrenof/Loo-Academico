from rest_framework import serializers
from contas.models import Aluno, Perfil
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from turma.models import Turma
from django.contrib.auth import authenticate
from desempenho.models import Desempenho
class AtualizarFotoPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['fotoPerfil']

class PerfilSerializer(serializers.ModelSerializer):
    nome_do_aluno = serializers.CharField(source='aluno.nomeAluno', read_only=True)
    turma_aluno = serializers.SerializerMethodField()
    respostas_corretas = serializers.SerializerMethodField()
    matricula_aluno = serializers.CharField(source='aluno.matricula', read_only=True)

    class Meta:
        model = Perfil
        fields = ['id', 'fotoPerfil', 'aluno', 'nome_do_aluno', 'turma_aluno', 'matricula_aluno', 'respostas_corretas']
    def get_respostas_corretas(self, obj):
        try:
            # Obter o desempenho do aluno associado ao perfil
            desempenho = Desempenho.objects.get(aluno=obj.aluno, turma=obj.aluno.turma)
            return desempenho.respostas_corretas
        except Desempenho.DoesNotExist:
            return 0 
    def get_turma_aluno(self, obj):
        # Verifica se o aluno está vinculado a uma turma
        if obj.aluno and obj.aluno.turma:
            return obj.aluno.turma.codicoTurma
        return 'Sem turma'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class AlunoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True,  min_length=8)
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Aluno
        fields = ['id', 'nomeAluno', 'instituicao', 'matricula', 'email', 'is_active', 'is_staff', 'password']
    def validate_email(self, value):
         if not value.lower().endswith('@alunos.ufersa.edu.br'):
            raise serializers.ValidationError("O email deve ter o domínio @alunos.ufersa.edu.br.")
         return value
    def validate_password(self, value):
        if value and len(value) < 8:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if ' ' in value:
            raise serializers.ValidationError("A senha não pode conter espaços em branco.")
        return value
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
        fields = ['nomeAluno', 'instituicao', 'matricula', 'email', 'password']

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