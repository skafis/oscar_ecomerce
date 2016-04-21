from django.db import models

# Create your models here.
from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.apps.models import *

class AbstractProductClass(models.Model):
    """
    Used for defining options and attributes for a subset of products.
    E.g. Books, DVDs and Toys. A product can only belong to one product class.

    At least one product class must be created when setting up a new
    Oscar deployment.

    Not necessarily equivalent to top-level categories but usually will be.
    """
    name = models.CharField(_('Name'), max_length=128)
    slug = AutoSlugField(_('Slug'), max_length=128, unique=True,
                         populate_from='name')
    #: Some product type don't require shipping (eg digital products) - we use
    #: this field to take some shortcuts in the checkout.
    requires_shipping = models.BooleanField(_("Requires shipping?"),
                                            default=True)
                                            
    options = models.ManyToManyField(
        'catalogue.Option', blank=True, verbose_name=_("Options"))   
        
    class Meta:
        abstract = True
        app_label = 'catalogue'
        ordering = ['name']
        verbose_name = _("Product class")
        verbose_name_plural = _("Product classes")
        
class AbstractProductCategory(models.Model):
    """
    Joining model between products and categories. Exists to allow customising.
    """
    product = models.ForeignKey('catalogue.Product', verbose_name=_("product"))
    category = models.ForeignKey('catalogue.Category',
                                verbose_name = _("Category"))
                                
    class Meta:
        abstract = True
        app_label = 'catalogue'
        ordering = ['product', 'category']
        unique_together = ('product', 'category')
        verbose_name = ('Product category')
        verbose_name_plural = _('Product categories')
        
    def __str__ (self):
        return u"<productcategory for product '&s'>" %self.product

class AbstractProductRecommendation(models.Model):
    
     """
    'Through' model for product recommendations
    """
    primary = models.ForeignKey(
        'catalogue.Product', related_name='primary_recommendations',
        verbose_name=_("Primary product"))
    recommendation = models.ForeignKey(
        'catalogue.Product', verbose_name=_("Recommended product"))
    ranking = models.PositiveSmallIntegerField(
        _('Ranking'), default=0,
        help_text=_('Determines order of the products. A product with a higher'
                    ' value will appear before one with a lower ranking.'))


    class Meta:
            abstract = True
            app_label = 'catalogue'
            ordering = ['primary', '-ranking']
            unique_together = ('primary', 'recommendation')
            verbose_name = _('Product recommendation')
            verbose_name_plural = _('Product recomendations')