from haystack import indexes

from .models import Resource


class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    created = indexes.DateTimeField(model_attr="created")
    type = indexes.MultiValueField(faceted=True)
    score = indexes.DecimalField(model_attr="rating")
    categories = indexes.MultiValueField(faceted=True)
    cities = indexes.MultiValueField(faceted=True)
    counties = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Resource

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_score(self, obj):
        return obj.rating_score

    def prepare_categories(self, obj):
        return [category.name for category in obj.categories.all()]

    def prepare_cities(self, obj):
        return [city.name for city in obj.cities.all()]

    def prepare_counties(self, obj):
        return [county.name for county in obj.counties.all()]

    def prepare_type(self, obj):
        return [url.url_type for url in obj.url_set.all()]
