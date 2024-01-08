# Generated by Django 3.2.3 on 2021-09-24 11:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api_user", "0001_initial"),
        ("api_skill", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="titleskill",
            name="set_by_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="title_skills",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="titleskill",
            name="skill_definition",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="title_skills",
                to="api_skill.skilldefinition",
            ),
        ),
        migrations.AddField(
            model_name="titleskill",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="title_skills",
                to="api_user.titles",
            ),
        ),
        migrations.AddField(
            model_name="skillvote",
            name="skill_definition",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="skill_votes",
                to="api_skill.skilldefinition",
            ),
        ),
        migrations.AddField(
            model_name="skillvote",
            name="voted_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="skill_votes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="skillvote",
            name="voter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="skilldefinition",
            name="level",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="definitions",
                to="api_skill.skilllevel",
            ),
        ),
        migrations.AddField(
            model_name="skilldefinition",
            name="skill",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="definitions",
                to="api_skill.skill",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="titleskill",
            unique_together={("title", "skill_definition")},
        ),
        migrations.AlterUniqueTogether(
            name="skillvote",
            unique_together={("voter", "voted_user", "skill_definition")},
        ),
        migrations.AlterUniqueTogether(
            name="skilldefinition",
            unique_together={("skill", "level")},
        ),
    ]
