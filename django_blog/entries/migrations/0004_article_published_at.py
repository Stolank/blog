from django.db import migrations, models


def preserve_existing_publications(apps, schema_editor):
    article = apps.get_model("entries", "Article")
    article.objects.using(schema_editor.connection.alias).update(published_at=models.F("created_at"))


class Migration(migrations.Migration):
    dependencies = [
        ("entries", "0003_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="published_at",
            field=models.DateTimeField("дата публикации", null=True, blank=True, editable=False),
        ),
        migrations.RunPython(preserve_existing_publications, migrations.RunPython.noop),
    ]
