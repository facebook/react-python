import json

import execjs

import jsx
import source


class Renderer(object):

    def __init__(self):
        with open(source.path_for('react.min.js')) as f:
            self.react = f.read()
            self.classes = {}

    def load_class(self, name, path):
        self.classes[name] = jsx.transform(path)

    def load_class_string(self, name, src):
        self.classes[name] = jsx.transform_string(src)

    def render(self, path):
        with open(path) as f:
            return self.render_string(f.read())

    def render_string(self, src, **context):
        transformed = jsx.transform_string(src)

        classes = '\n'.join(
            'var {} = {};'.format(name, class_)
            for name, class_ in self.classes.iteritems())

        context = '\n'.join(
            'var {} = {};'.format(key, json.dumps(value))
            for key, value in context.iteritems())

        expression = u"""
            (function() {{
                {}
                var React = (global.React || module.exports);
                {}
                {}
                var element = {};
                return React.renderToString(element);
            }}())
        """.format(self.react, classes, context, transformed)

        try:
            return execjs.eval(expression)
        except execjs.ProgramError as e:
            raise RenderError(e.message)


class RenderError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


default_renderer = Renderer()


def load_class(name, path):
    return default_renderer.load_class(name, path)


def load_class_string(name, src):
    return default_renderer.load_class_string(name, src)


def render(path):
    return default_renderer.render(path)


def render_string(src, **context):
    return default_renderer.render_string(src, **context)
