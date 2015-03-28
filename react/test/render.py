from unittest import TestCase
from os.path import join

from react.render import Renderer, RenderError
from react.test import TEST_ROOT


class TestRender(TestCase):

    def setUp(self):
        self.renderer = Renderer()

    def test_render_string(self):
        result = self.renderer.render_string(
            '<div>Hello, world!</div>')

        self.assertIn('reactid', result)
        self.assertIn('Hello, world!', result)

    def test_render_string_with_context(self):
        source = """
            (function() {
                var lis = array.map(function(item) {
                    return <li>{item}</li>;
                });

                return <div>
                    <h1>{title}</h1>
                    <p>The ultimate answer: {42}</p>
                    <ul>{lis}</ul>
                </div>;
            }())
        """

        result = self.renderer.render_string(
            source, title='Buttercakes', array=[1, 2, 3])

        self.assertIn('Buttercakes</h1>', result)
        self.assertIn('1</li>', result)
        self.assertIn('2</li>', result)
        self.assertIn('3</li>', result)

    def test_render(self):
        result = self.renderer.render(join(TEST_ROOT, 'files/test_script.jsx'))

        self.assertIn('Hello, world!</h1>', result)
        self.assertIn('1</li>', result)
        self.assertIn('2</li>', result)
        self.assertIn('3</li>', result)

    def test_load_class(self):
        self.renderer.load_class('Test', join(TEST_ROOT, 'files/test_class.jsx'))
        result = self.renderer.render_string('<Test foo="bar" />')

        self.assertIn('bar</div>', result)

    def test_load_class_string(self):
        self.renderer.load_class_string('Test',  (
            'React.createClass({'
            '    render: function() {'
            '        return <div>{this.props.foo}</div>;'
            '    }'
            '})'
        ))

        result = self.renderer.render_string('<Test foo="bar" />')

        self.assertIn('bar</div>', result)

    def test_exception(self):
        with self.assertRaisesRegexp(RenderError, r'ReferenceError'):
            self.renderer.render_string('<div>{foo}</div>')
