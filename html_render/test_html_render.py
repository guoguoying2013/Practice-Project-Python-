"""
test code for html_render.py

"""

import io
import pytest

# import * is often bad form, but makes it easier to test everything in a module.
from html_render import *


# utility function for testing render methods
def render_result(element, ind=""):
    """
    calls the element's render method, and returns what got rendered as a
    string
    """
    outfile = io.StringIO()
    if ind:
        element.render(outfile, ind)
    else:
        element.render(outfile)
    return outfile.getvalue()

# Step 1

def test_init():
    """
    This only tests that it can be initialized with and without
    some content
    """
    e = Element()

    e = Element("this is some text")


def test_append():
    """
    This tests that you can append text
    """
    e = Element("this is some text")
    e.append("some more text")


def test_render_element():
    """
    Tests whether the Element can render two pieces of text
    """
    e = Element("this is some text")
    e.append("and this is some more text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert"this is some text" in file_contents
    assert"and this is some more text" in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<!DOCTYPE html>\n")
    assert file_contents.endswith("</html>")

def test_render_element2():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.
    """
    e = Element()
    e.append("this is some text")
    e.append("and this is some more text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert"this is some text" in file_contents
    assert"and this is some more text" in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<!DOCTYPE html>\n")
    assert file_contents.endswith("</html>")


# Step 2

# tests for the new tags
def test_html():
    e = Html("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert"this is some text" in file_contents
    assert"and this is some more text" in file_contents
    print(file_contents)
    assert file_contents.endswith("</html>")


def test_body():
    e = Body("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert"this is some text" in file_contents
    assert"and this is some more text" in file_contents

    assert file_contents.startswith("<body>")
    assert file_contents.endswith("</body>")


def test_p():
    e = P("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert"this is some text" in file_contents
    assert"and this is some more text" in file_contents

    assert file_contents.startswith("<p>")
    assert file_contents.endswith("</p>")

def test_head():
    e = Head("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert"this is some text" in file_contents
    assert"and this is some more text" in file_contents

    assert file_contents.startswith("<head>")
    assert file_contents.endswith("</head>")

def test_sub_element():
    """
    tests that you can add another element and still render properly
    """
    page = Html()
    page.append("some plain text.")
    page.append(P("A simple paragraph of text"))
    page.append("Some more plain text.")

    file_contents = render_result(page)
    print(file_contents) 

    assert "some plain text" in file_contents
    assert "A simple paragraph of text" in file_contents
    assert "Some more plain text." in file_contents
    assert "some plain text" in file_contents
    assert "<p>" in file_contents
    assert "</p>" in file_contents

# Step 3

# test for title
def test_title():
    e = Title("This is a Title")

    file_contents = render_result(e).strip()

    assert"This is a Title" in file_contents
    print(file_contents)
    assert file_contents.startswith("<title>")
    assert file_contents.endswith("</title>")
    assert "\n" not in file_contents

#test for attribute
#it should look like this:
#<p style="text-align: center" id="intro">
#a paragraph of text
#</p>
def test_attributes():
    e = P("A paragraph of text", style="text-align: center", id="intro")
    file_contents = render_result(e).strip()
    print(file_contents)
    assert "A paragraph of text" in file_contents
    assert file_contents.endswith("</p>")
    assert file_contents.startswith("<p")
    assert 'style="text-align: center"' in file_contents
    assert 'id="intro"' in file_contents
    assert file_contents[:-1].index(">") > file_contents.index('id="intro"')
    assert file_contents[:file_contents.index(">")].count(" ") == 3


def test_hr():
    """a simple horizontal rule with no attributes"""
    hr = Hr()
    file_contents = render_result(hr)
    print(file_contents)
    assert file_contents == '<hr />\n'


def test_hr_attr():
    """a horizontal rule with an attribute"""
    hr = Hr(width=400)
    file_contents = render_result(hr)
    print(file_contents)
    assert file_contents == '<hr width="400" />\n'


def test_br():
    br = Br()
    file_contents = render_result(br)
    print(file_contents)
    assert file_contents == "<br />\n"


def test_content_in_br():
    with pytest.raises(TypeError):
        br = Br("some content")


def test_append_content_in_br():
    with pytest.raises(TypeError):
        br = Br()
        br.append("some content")

#should look like this <a href="http://google.com">link to google</a>
def test_achor():
    """test link"""
    a = A("http://google.com", "link to google")
    file_contents = render_result(a)
    print(file_contents)
    assert file_contents.startswith("<a ")
    assert file_contents == '<a href="http://google.com">link to google</a>'

#what a header look like?
def test_hearder():
    """test header, one line tag"""
    head1 = H(1, "important title")
    file_contents = render_result(head1)
    print(file_contents)
    assert file_contents == "<h1> important title </h1>\n"

def test_meta():
    """test meta, one line tag"""
    meta = Meta(charset="UTF-8")
    file_contents = render_result(meta)
    print(file_contents)
    assert file_contents == '<meta charset="UTF-8" />\n'

# indentation testing

def test_indent():
    """
    Tests that the indentation gets passed through to the renderer
    """
    html = Html("some content")
    file_contents = render_result(html, ind="   ").rstrip()

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[0].startswith("   <")
    print(repr(lines[-1]))
    assert lines[-1].startswith("   <")


def test_indent_contents():
    """
    The contents in a element should be indented more than the tag
    by the amount in the indent class attribute
    """
    html = Element("some content")
    file_contents = render_result(html, ind="")

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[2].startswith(Element.indent)


def test_indent_body():
    """test body indent"""
    body = Body()
    body.append("some text")
    html = Html(body)
    file_contents = render_result(html)
    print(file_contents)
    lines = file_contents.split("\n")
    for i in range(2):
        assert lines[i+1].startswith(i*Element.indent + "<")
    assert lines[3].startswith(2 * Element.indent + "some")

def test_multiple_indent():
    """
    make sure multiple levels get indented fully
    """
    body = Body()
    body.append(P("some text"))
    html = Html(body)

    file_contents = render_result(html)

    print(file_contents)
    lines = file_contents.split("\n")
    for i in range(3):
        assert lines[i + 1].startswith(i * Element.indent + "<")

    assert lines[4].startswith(3 * Element.indent + "some")


def test_element_indent1():
    """
    Tests whether the Element indents at least simple content
    """
    e = Element("this is some text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()
    print(file_contents)
    # making sure the content got in there.
    assert"this is some text" in file_contents

    # break into lines to check indentation
    lines = file_contents.split('\n')
    # making sure the opening and closing tags are right.
    assert lines[1] == "<html>"
    # this line should be indented by the amount specified
    # by the class attribute: "indent"
    assert lines[2].startswith(Element.indent + "thi")
    assert lines[3] == "</html>"
    assert file_contents.endswith("</html>")
