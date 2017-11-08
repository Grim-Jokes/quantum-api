# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-13 03:13
from __future__ import unicode_literals

from django.db import migrations


def add_categories(apps, *args):
    Category = apps.get_model('transactions', 'Category')

    parent_categories = [
        'Net income (after taxes and deductions)',
        'TOTAL SAVINGS AND INVESTMENTS',
        'Housing',
        'Life and health insurance',
        'Food and groceries',
        'Transportation',
        'Childcare',
        'Education and professional development',
        'Debt repayment',
        'Entertainment and fun',
        'Personal',
        'Miscellaneous'
    ]

    sub_categories = {
        'Housing': [
            'Repairs and maintenance',
            'Purchase household items',
            'Utilities',

        ],
        'Entertainment and fun': {
            'Holidays'
        },
        'Personal': [
            'Clothing',
            'Personal care / grooming',
            'Medical',
            'Services'
        ],
        'Miscellaneous': [
            'Gifts',
            'Donations',
            'Pets'
        ]
    }

    detail_categories = {
        'Net income (after taxes and deductions)': [
            'My take-home pay',
            'My spouse/partner\'s take-home pay',
            'Business income (profit)',
            'Interest / earning on investments',
            'Rental property income',
            'Retirement income (pension, RIF, annuity, etc...)',
            'Child support income',
            'Social assistance',
            'Student loan (money received)',
            'Canada child benefit',
            'Allowance',
            'Other'
        ],
        'TOTAL SAVINGS AND INVESTMENTS': [
            'Regular savings (Major purchases, etc...)',
            'Emergency funds',
            'Tax-Free Savings Account',
            'Retirement Savings (e.g. RRSP contributions)',
            'Registered Education Savings Plan (RESP)',
            'Non registered investments (GICs, mutual funds, etc...)',
            'Other'
        ],
        'Housing': [
            'Rent',
            'Mortgage payments',
            'Property taxes',
            'Home / tenant insurance',
            'Condo fees'
        ],
        'Repairs and maintenance': [
            'Painting and decorating',
            'Plumbing',
            'Electrical',
            'Home improvements (roof repair, new furnace, etc ...) ',
            'Appliances',
            'Gardening / landscaping',
            'Household services (cleaning service, snow removal, etc...)',
            'Other'
        ],
        'Purchase household items': [
            'Furniture',
            'Appliances',
            'House contents',
            'Other'
        ],
        'Utilities': [
            'Electricity',
            'Gas',
            'Water',
            'Telephone',
            'Cable or satellite',
            'Internet',
            'Combined (if you pay telephone, Internet, TV, etc. together)',
        ],
        'Life and health insurance': [
            'Medical',
            'Your life',
            'Your partner\'s life',
            'Your disability',
            'Your partner\'s disability',
            'Other'
        ],
        'Food and groceries': [
            'Groceries',
            'Work lunches(bought)',
            'Take - out / order in',
            'Other(for example, daily coffee purchases)',
        ],
        'Transportation': [
            'Vehicle licensing and registration',
            'Vehicle insurance',
            'Gas',
            'Maintenance',
            'Vehicle loan / lease payments',
            'Parking',
            'Transit pass (bus and / or train)',
            'Taxi fares',
            'Other',
        ],
        'Childcare': [
            'Daycare',
            'After school / holiday care',
            'Babysitting',
            'Child support payments',
            'Children\'s allowance',
            'Other',
        ],
        'Debt repayment':
        [
            'Student loan',
            'Credit cards',
            'Line of credit',
            'Other',
        ],
        'Entertainment and fun': [
            'Restaurants / Dining out',
            'Nightlife(bars, cafes, etc…)',
            'Club memberships(e.g. gym)',
            'Children\'s activities',
            'Tickets for sporting events, plays and concerts',
            'Outdoor recreation(e.g. camping, skiing)',
            'Sports gear(e.g. hockey equipment)',
            'Hobbies(e.g. stamp collection, musical instruments)',
            'Movies',
            'Newspapers / magazines / books',
            'Alcohol',
            'Tobacco(e.g. cigarettes)',
            'Other',
        ],
        'Holidays': [
            'Vacation',
            'Travel insurance',
            'Other'
        ],

        'Clothing': [
            'Adults\' clothes / shoes',
            'Children\'s clothes / shoes',
            'Laundry / dry cleaning',
            'Accessories',
        ],

        'Personal care / grooming': [
            'Cosmetics / toiletries',
            'Hairdresser / barbers',
            'Other',
        ],

        'Medical': [
            'Doctor',
            'Prescriptions and medicines',
            'Dentist',
            'Other',
        ],

        'Services': [
            'Banking fees',
            'Mobile phone(s)',
            'Professional(legal, financial advice, etc...)',
            'Other',
        ],

        'Gifts': ['Gifts(holiday, birthdays, special events, etc...)'],
        'Donations': ['Charitable donations'],
        'Pets': ['Vet expenses',
                 'Pet food',
                 'Other', ],


    }

    for category in parent_categories:
        parent_category = Category.objects.create(name=category)

        sub_cats = sub_categories.get(category, [])
        parent_det_cats = detail_categories.get(category, [])

        for det_cat in parent_det_cats:
            Category.objects.create(
                name=det_cat,
                parent_category=parent_category
            )

        for sub_cat in sub_cats:
            det_cats = detail_categories.get(sub_cat, [])
            sub_cat = Category.objects.create(
                name=sub_cat,
                parent_category=parent_category
            )

            for det_cat in det_cats:
                det_cat = Category.objects.create(
                    name=det_cat,
                    parent_category=sub_cat
                )


def delete_categories(apps, *args):
    Category = apps.get_model('transactions', 'Category')

    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_categories, delete_categories)
    ]
