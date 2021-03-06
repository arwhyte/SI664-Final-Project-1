# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

# Reference for Developer
class Developer(models.Model):
    developer_id = models.AutoField(primary_key=True)
    developer_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'developer'

    def __str__(self):
        return self.developer_name

    def get_absolute_url(self):
        # return reverse('game_detail', args=[str(self.id)])
        return reverse('developer_detail', kwargs={'pk': self.pk})

    @property
    def game_names(self):
        '''
        Return list of the regions and their respective sales in Millions
        for a given video game of interest.
        '''
        games = self.games.all().order_by('game_name')
        # sales = sale.objects.filterselect_related('game_id').order_by('total_sales')

        names = []
        for game in games:
            name = game.game_name
            if name is None:
                continue
            if name not in names:
                names.append(name)

        return ', '.join(names)


# Reference for Region
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'region'

    def __str__(self):
        return self.region_name

# Added str function
class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    # game_name = models.CharField(max_length=255, blank=True, null=True)
    game_name = models.CharField(max_length=255)
    platform = models.ForeignKey('Platform', on_delete=models.PROTECT, blank=True, null=True)
    year_released = models.IntegerField(blank=True, null=True)
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT, blank=True, null=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.PROTECT, blank=True, null=True)
    critic_score = models.IntegerField(blank=True, null=True)
    critic_count = models.IntegerField(blank=True, null=True)
    user_score = models.IntegerField(blank=True, null=True)
    user_count = models.IntegerField(blank=True, null=True)
    rating = models.ForeignKey('Rating', on_delete=models.PROTECT, blank=True, null=True)

    # Intermediate model (region -> sales <- game)
    region = models.ManyToManyField(Region, through='Sale')
    # Intermediate model (developer > game_developer <- game)
    developer = models.ManyToManyField(Developer, through='GameDeveloper', related_name='games')

    class Meta:
        managed = False
        db_table = 'game'

    def __str__(self):
        return self.game_name

    def region_display(self):
        '''Create a region string. This is required to display in Admin view.'''
        return ', '.join(
            region.region_name for region in self.region.all()[:25])

    region_display.short_description = 'Region'

    def developer_display(self):
        '''Create a string for developer. Required for display in Admin View.'''
        return ', '.join(
            developer.developer_name for developer in self.developer.all()[:25])

    developer_display.short_description = 'Developer'

    def get_absolute_url(self):
        # return reverse('game_detail', args=[str(self.id)])
        return reverse('game_detail', kwargs={'pk': self.pk})

    @property
    def sales_values(self):
        '''
        Return list of the regions and their respective sales in Millions
        for a given video game of interest.
        '''
        regions = self.region.order_by('region_name')
        # sales = sale.objects.filterselect_related('game_id').order_by('total_sales') 

        names = []
        for region in regions:
            name = region.region_name
            if name is None:
                continue
            if name not in names:
                names.append(name)

        return ', '.join(names)


# Linking table b/w Game and Developer to handle the M2M relationship
class GameDeveloper(models.Model):
    '''
    PK added to satisfy Django requirement. Mirror CONSTRAINT behavior in MySQL backend.
    '''
    game_developer_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'game_developer'

# Reference for Genre
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.genre_name


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'platform'

    def __str__(self):
        return self.platform_name


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    publisher_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'publisher'

    def __str__(self):
        return self.publisher_name


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rating_name = models.CharField(unique=True, max_length=4)

    class Meta:
        managed = False
        db_table = 'rating'

    def __str__(self):
        return self.rating_name


#"Linking table" b/w Region and Game to handle the M2M relationship
class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    total_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sale'



class TempGame(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=255)
    platform_name = models.CharField(max_length=50, blank=True, null=True)
    year_released = models.CharField(max_length=4, blank=True, null=True)
    genre_name = models.CharField(max_length=25, blank=True, null=True)
    publisher_name = models.CharField(max_length=100, blank=True, null=True)
    north_america_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    europe_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    japan_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    other_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    global_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    critic_score = models.CharField(max_length=3, blank=True, null=True)
    critic_count = models.CharField(max_length=10, blank=True, null=True)
    user_score = models.CharField(max_length=3, blank=True, null=True)
    user_count = models.CharField(max_length=10, blank=True, null=True)
    developer_name = models.CharField(max_length=100, blank=True, null=True)
    rating_name = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_game'
