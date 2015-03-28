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
        with open(path) as f:
            self.classes[name] = jsx.transform_string(f.read())

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

        return execjs.eval(expression)


render = Renderer()

