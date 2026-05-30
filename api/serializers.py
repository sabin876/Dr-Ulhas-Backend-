from rest_framework import serializers
from .models import Article, Service, Translation, SiteSetting

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

import json

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_internal_value(self, data):
        # Convert QueryDict to a standard dict to avoid list parsing issues with multi-value keys
        if hasattr(data, 'dict'):
            data = data.dict()
        elif hasattr(data, '_mutable'):
            data._mutable = True

        json_fields = ['items', 'faqs', 'conditions', 'checklist_items', 'tag_badges', 'schema_markup']
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except (ValueError, TypeError):
                    pass

        return super().to_internal_value(data)

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = '__all__'

class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'
