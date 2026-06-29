from django.db import migrations


def seed_initial_fleet_services(apps, schema_editor):
    Service = apps.get_model('pages', 'Service')
    Fleet = apps.get_model('pages', 'Fleet')

    services = [
        ('Business Class', 'Mercedes-Benz E-Class, BMW 5 Series, Cadillac XTS or similar'),
        ('Chauffeur Hailing', 'Professional chauffeur service for business, events, and city travel.'),
        ('Airport Transfers', 'Reliable airport pickup and drop-off service across major regional airports.'),
        ('Sprinter Class', 'Spacious luxury transportation for groups, meetings, and special occasions.'),
        ('Wedding Class', 'Premium wedding transportation with polished vehicles and professional chauffeurs.'),
        ('Travel Transfer', 'Comfortable private transfers for leisure, business, and long-distance travel.'),
    ]
    for index, (title, description) in enumerate(services, start=1):
        Service.objects.get_or_create(
            title=title,
            defaults={
                'short_description': description,
                'is_active': True,
                'order': index,
            },
        )

    fleets = [
        ('Luxury Sedan', 'Premium executive sedan for refined private travel.', 3, 3),
        ('Premium SUV', 'Luxury SUV service for families, business travelers, and extra luggage.', 6, 6),
    ]
    for index, (title, description, passengers, luggage) in enumerate(fleets, start=1):
        Fleet.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'passengers': passengers,
                'luggage': luggage,
                'is_active': True,
                'order': index,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_fleet_image'),
    ]

    operations = [
        migrations.RunPython(seed_initial_fleet_services, migrations.RunPython.noop),
    ]
