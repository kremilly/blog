#!/usr/bin/python3

from markupsafe import Markup

from backend.utils.files import FilesUtils

from backend.classes.my_blog import MyBlog
from backend.classes.settings import Settings
from backend.classes.md_builder import MDBuilder

from backend.actions.posts_meta import PostsMeta

class Posts:
    
    @classmethod
    def list_posts(cls) -> dict:
        list_posts = []
        url_root = MyBlog.get_url_root()
        path = Settings.get('paths.contents.blog', 'string')
        
        for post in FilesUtils.scan_path(path):
            file = post.split('/')[-1].replace('.md', '')
            slug = post.split('/')[-1].replace('+', '-').replace(' ', '-').replace('.md', '')
            
            list_posts.append({
                'slug': slug,
                'url': f'{url_root}/blog/{slug}',
                'date': PostsMeta.post_metadata_date(file),
                'title': PostsMeta.post_metadata(file, 'Title'),
                'read_time': PostsMeta.post_metadata_read_time(file),
                'description': PostsMeta.post_metadata(file, 'Description'),
            })
            
        return sorted(
            list_posts, key=lambda x: x['date']
        )

    @classmethod
    def get_post(cls, file:str) -> str:
        file_path = FilesUtils.get_file_path(file, 'blog')
        md_content = FilesUtils.read_content(file_path)

        if md_content is not None:
            return Markup(
                MDBuilder.render(md_content.content)
            )