# encoding: utf-8
"""
Search indexes for Haystack.

"""
from haystack import indexes

from sphinxdoc.models import Document


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index for :class:`~sphinxdoc.models.Document`.

    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    project = indexes.IntegerField(model_attr='project_id')

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
