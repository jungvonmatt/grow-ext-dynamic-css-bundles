# -*- coding: utf-8 -*-
import uuid
from operator import itemgetter

from grow import extensions
from grow.documents import document
from grow.extensions import hooks


class DynamicCssBundle(object):

    def __init__(self, doc):
        self.doc = doc
        # Used to determine where to print the finished styles
        self._placeholder = '/* {} */'.format(uuid.uuid4())
        # Stores registered paths
        self.css_files = []

    def __repr__(self):
        return '<DynamicCssBundle({})>'.format(self.placeholder)

    def addCssFile(self, path, priority=1):
        self.css_files.append((path, priority))
        # Return empty string to not interfer with content
        return ''

    def emit(self):
        return self._placeholder

    def inject(self, content):
        # Check wether the content has the placeholder
        if self.placeholder not in content:
            return

        # Sort CSS files by priority
        self.css_files.sort(key=itemgetter(1))

        base_path = self.doc.pod.root
        stylesheet = []
        # Try to get CSS from files and concat it
        for path, priority in self.css_files:
            path = '{}/{}'.format(base_path, path)
            try:
                with open(path, 'r') as css_file:
                    css = css_file.read()
                    stylesheet.append(css)
            except IOError:
                print('ERROR: Could not find {}'.format(path))

        stylesheet = ''.join(stylesheet)
        return content.replace(self.placeholder, stylesheet)


class DynamicCssBundlesPreRenderHook(hooks.PreRenderHook):
    """Handle the post-render hook."""

    def should_trigger(self, previous_result, doc, original_body, *_args,
                       **_kwargs):
        """Should the hook trigger with current document?"""
        return True

    def trigger(self, previous_result, doc, raw_content, *_args, **_kwargs):
        content = previous_result if previous_result else raw_content

        # Create dynamic stylesheet and attach to document for use in template
        setattr(doc, 'styles', DynamicCssBundle(doc))

        return content


class DynamicCssBundlesPostRenderHook(hooks.PostRenderHook):
    """Handle the post-render hook."""

    def should_trigger(self, previous_result, doc, original_body, *_args,
                       **_kwargs):
        """Should the hook trigger with current document?"""
        return True

    def trigger(self, previous_result, doc, raw_content, *_args, **_kwargs):
        content = previous_result if previous_result else raw_content

        if not doc.styles:
            return content

        return doc.styles.inject(content)


class DynamicCssBundlesExtension(extensions.BaseExtension):
    """Dynamic CSS Bundles Extension."""

    def __init__(self, pod, config):
        super(DynamicCssBundlesExtension, self).__init__(pod, config)

    @property
    def available_hooks(self):
        """Returns the available hook classes."""
        return [
            DynamicCssBundlesPreRenderHook,
            DynamicCssBundlesPostRenderHook,
        ]
