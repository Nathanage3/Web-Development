from rest_framework import serializers
from .models import Collection, Promotion, Course, CourseProgress, \
  Review, Customer, InstructorEarnings, CourseImage


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_course']


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'description', 'discount']


class CourseSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    promotions = PromotionSerializer(many=True, read_only=True)
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'rating', 'instructor', 'syllabus', 'prerequisites', 'is_active', 'collection', 'promotions']


class CourseProgressSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = CourseProgress
        fields = ['id', 'student', 'course', 'completed', 'progress', 'last_accessed']


class ReviewSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['id', 'course', 'rating', 'comment', 'user', 'created_at']


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'role', 'bio', 'profile_picture', 'website']


class InstructorEarningsSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()

    class Meta:
        model = InstructorEarnings
        fields = ['id', 'instructor', 'total_earnings', 'last_payout']


class CourseImageSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = CourseImage
        fields = ['id', 'course', 'video']
