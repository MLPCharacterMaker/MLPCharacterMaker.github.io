from django.contrib import admin

from .models import Character, Perk, Influence, BackgroundBond, HangUp


class BackgroundBondInline(admin.TabularInline):
    model = BackgroundBond


class PerkInline(admin.TabularInline):
    model = Perk


class HangUpInline(admin.TabularInline):
    model = HangUp


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'origin', 'role')


@admin.register(Influence)
class InfluenceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [BackgroundBondInline, PerkInline, HangUpInline]


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = ('name', 'influence')
    search_fields = ('name', 'description')
    list_filter = ('influence',)
