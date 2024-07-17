from rest_framework import serializers
from contas.models import Aluno, Perfil
from rest_framework_simplejwt.tokens import RefreshToken

class PerfilSerilizer(serializers.ModelSerializer):
    class Meta:
        nome_do_aluno = serializers.CharField(source = 'aluno.nomeALuno', read_only = True)
        turma_aluno = serializers.CharField(source = 'turma.codicoTurma', read_only = True)
        matricla_aluno = serializers.CharField(source = 'aluno.matricula', read_only = True)
        model = Perfil
        fields = ['fotoPerfil', 'aluno', 'turma', 'nome_do_aluno','turma_aluno', 'matricla_aluno' ]



class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nomeAluno', 'institucao', 'matricula', 'email']

class RegisterAlunoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Aluno
        fields = ('id', 'nomeAluno', 'institucao', 'matricula', 'email', 'password')
    
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError('A senha não pode ser em branco')
        if len(value) < 8:
            raise serializers.ValidationError('A senha deve ter pelo menos 8 caracteres')
        return value
    def create(self, validated_data):
        password = validated_data.pop('password')
        aluno = Aluno.objects.create_user(password=password, **validated_data)
        return aluno



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            aluno = Aluno.objects.filter(email=email).first()

            if aluno and aluno.check_password(password):
                refresh = RefreshToken.for_user(aluno)
                return {
                    'email': aluno.email,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            else:
                raise serializers.ValidationError("Credenciais inválidas Tente novamente.")
        else:
            raise serializers.ValidationError("Email e senha são obrigatórios.")