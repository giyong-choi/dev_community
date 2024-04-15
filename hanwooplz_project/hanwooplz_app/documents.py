from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post, UserProfile

@registry.register_document
class PostDocument(Document):
    author = fields.KeywordField(attr='author.username')
    title = fields.TextField()
    content = fields.TextField()

    class Index:
        name = 'posts'

    def get_queryset(self):
        return super().get_queryset().select_related('author')

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, UserProfile):
            return related_instance.post_set.all()

        return super().get_instances_from_related(related_instance)

    class Django:
        model = Post
