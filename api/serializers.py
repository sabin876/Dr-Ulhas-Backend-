from rest_framework import serializers
from .models import Article, Service, SubService, Translation, SiteSetting, GalleryItem, HeroVideo, SecondOpinion, HomePage

import json

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def to_internal_value(self, data):
        if hasattr(data, 'dict'):
            data = data.dict()
        elif hasattr(data, '_mutable'):
            data._mutable = True

        for json_field in ['faqs', 'schema_markup']:
            if json_field in data and isinstance(data[json_field], str):
                if data[json_field].strip() == '':
                    data[json_field] = None
                else:
                    try:
                        data[json_field] = json.loads(data[json_field])
                    except (ValueError, TypeError):
                        pass

        return super().to_internal_value(data)

import json

class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = ['id', 'title', 'slug', 'description', 'index_page', 'follow_links']

class SecondOpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondOpinion
        fields = ['id', 'category', 'title', 'paragraph_1', 'paragraph_2', 'order', 'is_active']

class ServiceSerializer(serializers.ModelSerializer):
    sub_services = SubServiceSerializer(many=True, read_only=True)
    second_opinions = SecondOpinionSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

    def to_internal_value(self, data):
        # Convert QueryDict to a standard dict to avoid list parsing issues with multi-value keys
        if hasattr(data, 'dict'):
            data = data.dict()
        elif hasattr(data, '_mutable'):
            data._mutable = True

        if 'second_opinion_is_active' in data and isinstance(data['second_opinion_is_active'], str):
            data['second_opinion_is_active'] = data['second_opinion_is_active'].lower() in ['true', '1', 'yes']

        json_fields = ['items', 'faqs', 'conditions', 'checklist_items', 'tag_badges', 'schema_markup', 'who_needs_items', 'commonly_treated', 'highlight_checklist_items', 'highlight_doctor_badges', 'journey_steps']
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except (ValueError, TypeError):
                    pass

        return super().to_internal_value(data)

    def create(self, validated_data):
        sub_services_data = self.initial_data.get('sub_services')
        instance = super().create(validated_data)
        
        if sub_services_data:
            if isinstance(sub_services_data, str):
                try:
                    sub_services_data = json.loads(sub_services_data)
                except ValueError:
                    sub_services_data = []
            
            for ss_item in sub_services_data:
                title = ss_item.get('title')
                desc = ss_item.get('description') or ss_item.get('desc', '')
                if title:
                    SubService.objects.create(
                        service=instance,
                        title=title,
                        description=desc
                    )
        return instance

    def update(self, instance, validated_data):
        sub_services_data = self.initial_data.get('sub_services')
        instance = super().update(instance, validated_data)
        
        if sub_services_data is not None:
            if isinstance(sub_services_data, str):
                try:
                    sub_services_data = json.loads(sub_services_data)
                except ValueError:
                    sub_services_data = []
            
            instance.sub_services.all().delete()
            for ss_item in sub_services_data:
                title = ss_item.get('title')
                desc = ss_item.get('description') or ss_item.get('desc', '')
                if title:
                    SubService.objects.create(
                        service=instance,
                        title=title,
                        description=desc
                    )
        return instance

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = '__all__'

class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = '__all__'


class HeroVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroVideo
        fields = '__all__'


class SecondOpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondOpinion
        fields = '__all__'


class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePage
        fields = '__all__'

    def to_internal_value(self, data):
        if hasattr(data, 'dict'):
            data = data.dict()
        elif hasattr(data, '_mutable'):
            data._mutable = True

        for json_field in ['faqs', 'schema_markup']:
            if json_field in data and isinstance(data[json_field], str):
                if data[json_field].strip() == '':
                    data[json_field] = None
                else:
                    try:
                        data[json_field] = json.loads(data[json_field])
                    except (ValueError, TypeError):
                        pass

        return super().to_internal_value(data)


