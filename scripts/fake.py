import os
import pathlib
import random
import sys
from datetime import timedelta

import django
import faker
from django.utils import timezone


# 将django项目根目录添加到python的模版搜索路径中，从而单独执行fake.py可以找到相应的模块文件

back = os.path.dirname
BASEDIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
print(sys.path)


if __name__ == '__main__':
    # 设置django配置变量，并setup启动django
    # 只有启动django后，才能使用django的orm的接口，才能匹配生成测试数据，
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings.local')
    django.setup()

    from blog.models import Post, Category, Tag
    from comments.models import Comments
    from django.contrib.auth.models import User

    # 下面就是开始生成测试数据：

    # 1、清理所有旧有数据，生成用户
    print('clean old data')
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comments.objects.all().delete()
    User.objects.all().delete()

    print('create blog user')
    user = User.objects.create_user('admin', 'admin@gmail.com', 'admin')

    # 2、生成一些定义好的分类、标签，一篇测试的md格式的文章
    category_list = ['python', 'java', 'c/c++', 'golang', 'rust', 'javascript']
    tag_list = ['web', 'backend', 'machine learning', 'devops']
    a_year_ago = timezone.now() - timedelta(days=365)

    print('create tags and categories')
    for cate in category_list:
        Category.objects.create(
            name=cate,
        )

    for tag in tag_list:
        Tag.objects.create(
            name=tag,
        )

    print('create a md post')
    Post.objects.create(
        title='md 文章测试',
        body=pathlib.Path(BASEDIR).joinpath('scripts', 'md.simple').read_text(encoding='utf-8'),
        category=Category.objects.create(name='md测试'),
        user=user,
    )
    # 3、随即生成100篇英文文章
    print('create som faked posts in english ,which publised within the past year')
    fake = faker.Faker() # 默认英文
    for _ in range(100):
        tags = Tag.objects.order_by('?') # 随即排序
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now", tzinfo=timezone.get_current_timezone())

        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            user=user
        )

        post.tags.add(tag1, tag2)
        post.save()

    # 4、随即生成100篇中文文章
    print('create som faked posts in zh_CN ,which publised within the past year')
    fake = faker.Faker('zh_CN') # 默认英文
    for _ in range(100):
        tags = Tag.objects.order_by('?') # 随即排序
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now", tzinfo=timezone.get_current_timezone())

        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            user=user
        )

        post.tags.add(tag1, tag2)
        post.save()

    # 5、给前20篇文件，生成评论（3-15条）
    print('create some comments')
    for post in Post.objects.all()[:20]:
        post_created_time = post.created_time
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comments.objects.create(
                name=fake.name(),
                email=fake.email(),
                website=fake.uri(),
                text=fake.paragraph(),
                created_time=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
                post=post,

            )
    print('done!')
















