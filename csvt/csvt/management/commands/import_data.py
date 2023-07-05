import json, sys

from django.contrib.auth.models import Group

from lk.models import User
from page.models import Page
from product.models import Product


def load_data(f):
    def _load_data(data):
        return f(json.load(open(data)))
    return _load_data


@load_data
def import_group(data):
    for g in data:
        Group(name=g['fields']['name']).save()
    return data

@load_data
def import_user(data):
    for u in data:
        if 'user_permissions' in u['fields']:
            u['fields'].pop('user_permissions')
        if 'groups' in u['fields']:
            u['fields'].pop('groups')
        User(id=u['pk'],**u['fields']).save()
    return data

@load_data
def import_page(data):
    for p in data:
        try:
            fields = dict(
                template_name=p['fields']['template_name'],
                attributes=p['fields']['attributes'],
                is_public=p['fields']['is_public'],
                slug=p['fields']['slug'],
            )
            page = Page(**fields)
            page.save()
            page.set_current_language('ru')
            trans_ru = dict(
                name = p['fields']['name'],
                title = p['fields']['title'],
                content = p['fields']['content'],
                seo_h1 = p['fields']['seo_h1'],
                seo_h2 = p['fields']['seo_h2'],
                seo_keywords = p['fields']['keywords'],
                seo_description = p['fields']['description'],
            )

            for k, v in trans_ru.items():
                if k and v:
                    setattr(page, k, v)

            page.save()

            page.set_current_language('en')
            trans_en = dict(
                name = p['fields']['name_en'],
                title = p['fields']['title_en'],
                content = p['fields']['content_en'],
                seo_h1 = p['fields']['seo_h1_en'],
                seo_h2 = p['fields']['seo_h2_en'],
                seo_keywords = p['fields']['keywords_en'],
                seo_description = p['fields']['description_en']
            )

            for k, v in trans_en.items():
                if k and v:
                    setattr(page, k, v)

            page.save()

        except Exception as error:
            print(p["pk"])

    return data

@load_data
def import_page(data):
    enable_fields = set(sorted(f.name for f in Page._meta.fields))
    available_fields = set(sorted(f for f in data[0]['fields'].keys()))
    parler_fields = set(Page._parler_meta.get_translated_fields())

    print(sorted(enable_fields - available_fields))
    print(sorted(parler_fields - available_fields))
    print(available_fields)

    alias_fields = dict(
        seo_title="title",
        seo_keywords="keywords",
    )

    for p in data:
        fields = p['fields']
        if "setting_attributes" in fields:
            fields["attributes"] = fields.pop("setting_attributes")
        page = Page(**dict([k, v] for k, v in fields.items() if k in enable_fields))
        page.save()

        trans_fields = parler_fields - available_fields
        page.set_current_language('ru')

        for k in ("name", "title"):
            if fields.get(k):
                setattr(page, k, fields[k])

        page.save()

        page.set_current_language('en')

        for k in ("name", "title"):
            if fields.get("{k}_en"):
                setattr(page, k, fields["{k}_en"])

        page.save()




@load_data
def import_product(data):
    enable_fields = list(sorted(f.name for f in Product._meta.fields))
    parler_fields = list(sorted(Product._parler_meta.get_translated_fields()))
    for p in data:
        fields = p['fields']
        product = Product(**dict([k, v] for k, v in fields.items() if k in enable_fields))
        product.save()
