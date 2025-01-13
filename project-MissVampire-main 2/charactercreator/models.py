from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Character(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    name = models.CharField(max_length=100,default='New Character')

    special_talent = models.CharField(max_length=200, blank=True)

    # level
    level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)])

    # origin
    PEGASUS = "P"
    UNICORN = "U"
    EARTH_PONY = "E"
    ORIGIN_CHOICES = {
        PEGASUS: "Pegasus",
        UNICORN: "Unicorn",
        EARTH_PONY: "Earth Pony",
    }
    origin = models.CharField(
        max_length=1,
        choices=ORIGIN_CHOICES,
        default=EARTH_PONY,
    )

    # Role
    GENEROSITY = "GE"
    HONESTY = "HO"
    KINDNESS = "KI"
    LAUGHTER = "LA"
    LOYALTY = "LO"
    MAGIC = "MA"
    ROLE_CHOICES = {
        GENEROSITY: "Generosity",
        HONESTY: "Honesty",
        KINDNESS: "Kindness",
        LAUGHTER: "Laughter",
        LOYALTY: "Loyalty",
        MAGIC: "Magic",
    }
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=MAGIC,
    )

    image = models.ImageField(upload_to='character_images/', blank=True, null=True)

    cutie_mark_image = models.ImageField(upload_to='character_images/', blank=True, null=True)

    SE = "SE"
    HH = "HH"
    TT = "TT"
    SH = "SH"
    ST = "ST"
    HT = "HT"
    AA = "AA"
    PRONOUN_CHOICES = {
        SE: "she/her",
        HH: "he/him",
        TT: "they/them",
        SH: "she/he",
        ST: "she/they",
        HT: "he/they",
        AA: "she/he/they",
    }
    pronouns = models.CharField(
        max_length=2,
        choices=PRONOUN_CHOICES,
        default=TT,
    )

    # character description
    description = models.TextField(blank=True)

    health = models.IntegerField(default=0)

    movement = models.CharField(max_length=50, default='0')

    base_strength = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(15)])
    base_speed = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(15)])
    base_smarts = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(15)])
    base_social = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(15)])

    STATUS_CHOICES = [
        ('diamond', 'Diamond'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]
    strength_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)
    speed_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)
    smarts_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)
    social_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)

    def level_bonus(self):
        bonuses = {'strength': 0, 'speed': 0, 'smarts': 0, 'social': 0}
        status_map = {
            self.strength_status: 'strength',
            self.speed_status: 'speed',
            self.smarts_status: 'smarts',
            self.social_status: 'social',
        }
        level = self.level

        # Assigning bonuses based on level
        if level >= 1:
            bonuses[status_map['diamond']] += 2
            bonuses[status_map['gold']] += 1
        if level >= 2:
            bonuses[status_map['gold']] += 1
        if level >= 3:
            bonuses[status_map['silver']] += 1
        if level >= 4:
            bonuses[status_map['bronze']] += 1
        if level >= 5:
            bonuses[status_map['diamond']] += 1
        if level >= 6:
            bonuses[status_map['gold']] += 1
        if level >= 7:
            bonuses[status_map['silver']] += 1
        if level >= 8:
            bonuses[status_map['bronze']] += 1
        if level >= 9:
            bonuses[status_map['diamond']] += 1
        if level >= 10:
            bonuses[status_map['gold']] += 1
        if level >= 11:
            bonuses[status_map['silver']] += 1
        if level >= 12:
            bonuses[status_map['bronze']] += 1
        if level >= 13:
            bonuses[status_map['diamond']] += 1
        if level >= 14:
            bonuses[status_map['gold']] += 1
        if level >= 15:
            bonuses[status_map['silver']] += 1
        if level >= 16:
            bonuses[status_map['diamond']] += 1
        if level >= 17:
            bonuses[status_map['gold']] += 1
        if level >= 18:
            bonuses[status_map['diamond']] += 1
        if level >= 19:
            bonuses[status_map['gold']] += 1
        if level >= 20:
            bonuses[status_map['diamond']] += 1

        return bonuses

    # Method to calculate the final values for stats
    def strength(self):
        return self.base_strength + self.level_bonus().get('strength', 0)

    def speed(self):
        return self.base_speed + self.level_bonus().get('speed', 0)

    def smarts(self):
        return self.base_smarts + self.level_bonus().get('smarts', 0)

    def social(self):
        return self.base_social + self.level_bonus().get('social', 0)

    influences = models.ManyToManyField('Influence', blank=True, related_name='characters')
    perks = models.ManyToManyField('Perk', blank=True, related_name='characters')
    hangups = models.ManyToManyField('HangUp', blank=True, related_name='characters')
    background_bonds = models.ManyToManyField('BackgroundBond', blank=True, related_name='characters')

    def calculate_perks(self):
        perks = []
        for influence in self.influences.all():
            perks.extend(influence.perks.all())
        return perks

    def required_hangups_count(self):
        return max(0, self.influences.count() - 1)

    def __str__(self):
        return self.name


class Influence(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    characteristics = models.TextField(blank=True)

    def __str__(self):
        return self.name


class HangUp(models.Model):
    influence = models.ForeignKey(Influence, on_delete=models.CASCADE, related_name='hangups')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Perk(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    prerequisite = models.TextField(blank=True)
    influence = models.ForeignKey(Influence, on_delete=models.CASCADE, related_name='perks', blank=True, null=True)

    def __str__(self):
        return self.name


# Gotta figure these out
class BackgroundBond(models.Model):
    influence = models.ForeignKey(Influence, on_delete=models.CASCADE, related_name="background_bonds")
    description = models.TextField()

    def __str__(self):
        return f"{self.description} (for {self.influence.name})"

# class Specialization(models.Model):
