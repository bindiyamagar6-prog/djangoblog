from django.db import migrations, models
from django.utils.text import slugify


def _make_unique(model, source_attr, prefix):
    """Keep good slugs, replace empty or duplicate ones with unique ones."""
    objs = list(model.objects.all().order_by("id"))
    used = set()
    keep = set()
    for o in objs:
        s = (o.slug or "").strip()
        if s and s not in used:
            used.add(s)
            keep.add(o.pk)
    for o in objs:
        if o.pk in keep:
            continue
        base = slugify(getattr(o, source_attr, "") or "")[:45] or f"{prefix}-{o.pk}"
        slug, n = base, 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        model.objects.filter(pk=o.pk).update(slug=slug)


def fill_slugs(apps, schema_editor):
    _make_unique(apps.get_model("blog", "Tag"), "name", "tag")
    _make_unique(apps.get_model("blog", "Category"), "name", "category")
    _make_unique(apps.get_model("blog", "Post"), "title", "post")


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_category_slug_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, default='', db_index=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]