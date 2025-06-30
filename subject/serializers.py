# sections/serializers.py
from rest_framework import serializers
from .models import SectionSubjectRequirement, Section 
from .models import Subject 
from django.utils.translation import gettext_lazy as _ 

class SubjectSerializer(serializers.ModelSerializer):
    class_obj_name = serializers.CharField(source='class_obj.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    stream_type_display = serializers.CharField(source='get_stream_type_display', read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'class_obj', 'section', 'stream_type', 'name', 'description', 
            'is_active', 'pdf_url', 
            'class_obj_name', 'section_name', 'stream_type_display',
            'created_at', 'updated_at' 
        ]
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        class_obj = data.get('class_obj')
        section = data.get('section')
        stream_type = data.get('stream_type')


        if class_obj and not section and not stream_type:
            # مادة لصف كامل
            pass
        elif section and not class_obj and not stream_type:
            # مادة لشعبة محددة
            pass
        elif class_obj and stream_type and not section:
            # مادة لمسار (مثل عاشر علمي)
            pass
        elif not class_obj and not section and not stream_type:
            # مادة عامة بدون ربط (ربما مادة تعريفية فقط، أو مادة "مفتوحة" يمكن ربطها لاحقا)
            pass
        else:
            raise serializers.ValidationError(
                _("يجب ربط المادة إما بصف، أو بشعبة محددة، أو بمسار ضمن صف. لا يمكن خلط الروابط بطرق غير منطقية.")
            )


        return data

class SectionSubjectRequirementSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = SectionSubjectRequirement
        fields = [
            'id', 'section', 'subject', 'weekly_lessons_required', 'created_at',
            'section_name', 'subject_name' 
        ]
        read_only_fields = ('created_at',)
