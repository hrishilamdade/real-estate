import random
import string
from tabnanny import verbose
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class PropertyPublishManager(models.Manager):
    def get_queryset(self):
        return super(PropertyPublishManager,self).get_queryset().filter(published_status=True)

class Property(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = 'For Sale', _('For Sale')
        FOR_RENT = 'For Rent', _('For Rent')
        FOR_AUCTION = 'Auction',_('Auction')
    
    class PropertyType(models.TextChoices):
        APARTMENT = 'Apartment', _('Apartment')
        HOUSE = 'House', _('House')
        WAREHOUSE = 'Warehouse', _('Warehouse')
        OFFICE = 'Office', _('Office')
        COMMERCIAL = 'Commercial', _('Commercial')
        OTHER = 'Other', _('Other')

    user = models.ForeignKey(User,verbose_name=_("Agent,Buyer or Seller"),related_name='agent_buyer',on_delete=models.DO_NOTHING)
    title = models.CharField(verbose_name=_("Property Title"),max_length=250)
    slug = AutoSlugField(populate_from='title',unique=True,verbose_name=_("Slug"),always_update=True)
    ref_code = models.CharField(verbose_name=_("Property Reference Code"),max_length=255,unique=True,blank=True,null=True)
    description = models.TextField(verbose_name=_("Property Description"),default="Add small description of your property",blank=True,null=True)
    country = CountryField(verbose_name=_("Country"),default="IND",blank_label= "Select country",blank=False,null=False)
    city = models.CharField(verbose_name=_("City"),max_length=180,default="Mumbai",blank=False,null=False)
    postal_code = models.CharField(verbose_name=_("Postal Code"),max_length=100,default="401501")
    street_address = models.CharField(verbose_name=_("Street Address"),max_length=255,default = "KG8 Avenue",blank=False,null=False)
    property_number = models.IntegerField(verbose_name=_("Property Number"),validators=[MinValueValidator(1)],default=112)
    price = models.DecimalField(verbose_name=_("Price"),max_digits=10,decimal_places=2,default=0.0)
    tax = models.DecimalField(verbose_name=_("Property Tax"),max_digits=10,decimal_places=2,default=0.15,help_text="15% property tax charged")
    plot_area = models.DecimalField(verbose_name=_("Plot Area(m^2)"),max_digits=10,decimal_places=2,default=0.0)
    total_floors = models.IntegerField(verbose_name=_("Total Floors"),default=1)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"),default=1)
    bathrooms = models.IntegerField(verbose_name=_("Bathrooms"),default=1)
    advert_type = models.CharField(verbose_name=_("Advert Type"),max_length=50,choices=AdvertType.choices,default=AdvertType.FOR_SALE)
    property_type = models.CharField(verbose_name=_("Property Type"),max_length=50,choices=PropertyType.choices,default=PropertyType.APARTMENT)
    cover_photo = models.ImageField(verbose_name=_("Main Photo"),default = "/house_sample.jpg",upload_to="properties/cover_photos/",blank=True,null=True)
    photo1 = models.ImageField(default = "/interior_sample.jpg",upload_to="properties/cover_photos/",blank=True,null=True)
    photo2 = models.ImageField(default = "/interior_sample.jpg",upload_to="properties/cover_photos/",blank=True,null=True)    
    photo3 = models.ImageField(default = "/interior_sample.jpg",upload_to="properties/cover_photos/",blank=True,null=True)
    photo4 = models.ImageField(default = "/interior_sample.jpg",upload_to="properties/cover_photos/",blank=True,null=True)
    published_status = models.BooleanField(verbose_name=_("Published Status"),default=False)
    views = models.IntegerField(verbose_name=_("Total Views"),default=0)
    objects = models.Manager()
    published = PropertyPublishManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
    
    def save(self,*args,**kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(random.choices(string.ascii_uppercase+string.digits,k=10))

        super(Property,self).save(*args,**kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage*property_price,2)
        price_after_tax = float(round(property_price+tax_amount,2))
        return price_after_tax

class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(max_length=250,verbose_name = _('IP Address'))
    property = models.ForeignKey(Property,related_name ='property_views',on_delete = models.CASCADE )

    def __str__(self):
        return f"Total views on - {self.property.title} is - {self.property.views} view(s)"

    class Meta:
        verbose_name = "Total views on property"
        verbose_name_plural = "Total Property views"