# lims_backend/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'role_display',   # ✅ tambahin di output
            'phone',
            'department',
            'is_active',
            'date_joined',
            'is_staff',
            'is_superuser',
        ]
        read_only_fields = ['id', 'date_joined', 'is_staff', 'is_superuser']

    def get_role_display(self, obj):
        if obj.is_superuser:
            return "Superuser"
        if obj.is_staff and not obj.role:
            return "Staff"
        return obj.get_role_display() if obj.role else "-"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)  # wajib dipilih

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password','password2','role','phone','department']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password":"Password dan password2 harus sama."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone','department','password']

    def update(self, instance, validated_data):
        pw = validated_data.pop('password', None)
        for k,v in validated_data.items():
            setattr(instance, k, v)
        if pw:
            instance.set_password(pw)
        instance.save()
        return instance

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role','is_active']
