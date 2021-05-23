
class Article:
    title = ''
    description = ''
    image_url = ''
    url = ''
    category_name = ''
    category_slug = ''
    created_at = ''

    def __init__(self, title, description, image_url, url, category_name, category_slug, created_at):
        self.title = title
        self.description = description
        self.image_url = image_url
        self.url = url
        self.category_name = category_name
        self.category_slug = category_slug
        self.created_at = created_at
