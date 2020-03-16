# Generated by Django 2.2.5 on 2020-03-01 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a book genre (e.g. Science Fiction)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=200)),
                ('book_cover', models.ImageField(upload_to='gallery')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('summary', models.TextField(help_text='Enter a brief description of the book', max_length=1000)),
                ('isbn', models.CharField(help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=13, verbose_name='ISBN')),
                ('release_date', models.DateField(null=True)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookstore.Author')),
                ('genre', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookstore.Genre')),
                ('publisher', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookstore.Publisher')),
            ],
            options={
                'ordering': ['book_title'],
            },
        ),
    ]