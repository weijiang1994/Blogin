"""
# coding:utf-8
Markdown extensions for custom HTML styling.
"""
from markdown import extensions
from markdown.treeprocessors import Treeprocessor


class MyMDStyleTreeProcessor(Treeprocessor):
    def run(self, root):
        for child in root.getiterator():
            if child.tag == 'table':
                child.set("class", "table table-bordered table-hover")
            elif child.tag == 'img':
                child.set("class", "img-fluid d-block img-pd10")
            elif child.tag == 'blockquote':
                child.set('class', 'blockquote-comment')
            elif child.tag == 'p':
                child.set('class', 'mt-0 mb-0 p-break')
            elif child.tag == 'pre':
                child.set('class', 'mb-0')
            elif child.tag == 'h1':
                child.set('class', 'comment-h1')
            elif child.tag == 'h2':
                child.set('class', 'comment-h2')
            elif child.tag == 'h3':
                child.set('class', 'comment-h3')
            elif child.tag in ['h4', 'h5', 'h6']:
                child.set('class', 'comment-h4')
        return root


# noinspection PyAttributeOutsideInit
class MyMDStyleExtension(extensions.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.processor = MyMDStyleTreeProcessor()
        self.processor.md = md
        self.processor.config = self.getConfigs()
        md.treeprocessors.add('mystyle', self.processor, '_end')
