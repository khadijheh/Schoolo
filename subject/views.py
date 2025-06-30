from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from django.db import transaction

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAdminUser] # أو [permissions.IsAuthenticated, CustomAdminPermission]

    def perform_create(self, serializer):
        with transaction.atomic():
            subject_instance = serializer.save()
            self._create_or_update_section_subject_requirements(subject_instance)

    def perform_update(self, serializer):
        with transaction.atomic():
            subject_instance = serializer.save()
            SectionSubjectRequirement.objects.filter(subject=subject_instance).delete()
            self._create_or_update_section_subject_requirements(subject_instance)

    def _create_or_update_section_subject_requirements(self, subject_instance):
        """
        دالة مساعدة لإنشاء/تحديث سجلات SectionSubjectRequirement
        بناءً على ربط المادة بـ (صف، شعبة، نوع مسار).
        """
        weekly_lessons = subject_instance.weekly_sessions
        
        # Scenario 1: Subject linked to a specific Section
        if subject_instance.section:
            SectionSubjectRequirement.objects.create(
                section=subject_instance.section,
                subject=subject_instance,
                weekly_lessons_required=weekly_lessons,
                academic_year=subject_instance.section.academic_year # ربطها بالسنة الأكاديمية للشعبة
            )
            print(f"Created SSR for specific section: {subject_instance.section.name}")

        elif subject_instance.class_obj and not subject_instance.stream_type:
            sections_in_class = Section.objects.filter(class_obj=subject_instance.class_obj)
            for section in sections_in_class:
                SectionSubjectRequirement.objects.create(
                    section=section,
                    subject=subject_instance,
                    weekly_lessons_required=weekly_lessons,
                    academic_year=section.academic_year
                )
                print(f"Created SSR for section {section.name} in class {subject_instance.class_obj.name}")

        elif subject_instance.class_obj and subject_instance.stream_type:
            sections_in_stream = Section.objects.filter(
                class_obj=subject_instance.class_obj,
                stream_type=subject_instance.stream_type
            )
            for section in sections_in_stream:
                SectionSubjectRequirement.objects.create(
                    section=section,
                    subject=subject_instance,
                    weekly_lessons_required=weekly_lessons,
                    academic_year=section.academic_year
                )
                print(f"Created SSR for section {section.name} in stream {subject_instance.stream_type} of class {subject_instance.class_obj.name}")
        else:
            print(f"Subject '{subject_instance.name}' is not linked to a specific section, class or stream type, so no SectionSubjectRequirement created.")


class SectionSubjectRequirementViewSet(viewsets.ModelViewSet):
    queryset = SectionSubjectRequirement.objects.all()
    serializer_class = SectionSubjectRequirementSerializer
    def get_queryset(self):
        queryset = SectionSubjectRequirement.objects.all()
        section_id = self.request.query_params.get('section_id')
        subject_id = self.request.query_params.get('subject_id')
        academic_year_id = self.request.query_params.get('academic_year_id') 

        if section_id:
            queryset = queryset.filter(section__id=section_id)
        if subject_id:
            queryset = queryset.filter(subject__id=subject_id)
        if academic_year_id: 
            queryset = queryset.filter(academic_year__id=academic_year_id)

        return queryset
    # permission_classes = [permissions.IsAuthenticated]