from rest_framework import serializers
from contas.models import Aluno, Perfil
from rest_framework_simplejwt.tokens import RefreshToken
from turma.models import Turma

class AtualizarFotoPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['fotoPerfil']    

class PerfilSerializer(serializers.ModelSerializer):
    nome_do_aluno = serializers.CharField(source='aluno.nomeAluno', read_only=True)
    turma_aluno = serializers.SerializerMethodField()  # Usando SerializerMethodField para lidar com a ausência de turma
    matricula_aluno = serializers.CharField(source='aluno.matricula', read_only=True)

    class Meta:
        model = Perfil
        fields = ['id', 'fotoPerfil', 'aluno', 'turma', 'nome_do_aluno', 'turma_aluno', 'matricula_aluno']

    def get_turma_aluno(self, obj):
        # Verifica se o objeto 'turma' não é None antes de acessar 'codicoTurma'
        if obj.turma:
            return obj.turma.codicoTurma
        return 'Sem turma'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove o campo 'turma' da representação se for None
        if instance.turma is None:
            representation.pop('turma_aluno', None)
        return representation
class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nomeAluno', 'instituicao', 'matricula', 'email', 'turma']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Aluno
        fields = ['nomeAluno', 'instituicao', 'matricula', 'email', 'password', 'turma']

    def create(self, validated_data):
        user = Aluno.objects.create_user(
            email=validated_data['email'],
            nomeAluno=validated_data['nomeAluno'],
            matricula=validated_data['matricula'],
            instituicao=validated_data['instituicao'],
            password=validated_data['password'],
            turma=validated_data.get('turma')
        )
        return user
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        return data