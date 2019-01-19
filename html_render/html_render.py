#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element():
    """"This is most basic element class in html render, other classes will be built based on it"""
    tag_name = "html"
    indent = "    "

    def __init__(self, content=None, **kwargs):
        self.content = [] if content is None else [content]
        self.kwargs = kwargs

    def append(self, new_content):
        """add new content between tags"""
        self.content.append(new_content)

    def render(self, out_file, cur_ind=""):
        """render functions"""
        if self.tag_name == "html":
            out_file.write(cur_ind)
            out_file.write("<!DOCTYPE html>\n")

        #open tag
        if cur_ind:
            out_file.write(cur_ind)
        if self.kwargs is not None:
            open_tag = ["<{}".format(self.tag_name)]
            for x in self.kwargs:
                open_tag.append(" ")
                open_tag.append(x)
                open_tag.append("=")
                open_tag.append('"{}"'.format(self.kwargs[x]))
            open_tag.append(">\n")
            out_file.write("".join(open_tag))
        else:
            out_file.write("<{}>".format(self.tag_name))
            out_file.write("\n")

        #content
        for content in self.content:
            try:
                content.render(out_file, cur_ind+self.indent)
            except AttributeError:
                if cur_ind:
                    out_file.write(cur_ind)
                out_file.write(self.indent)
                out_file.write(content)
                out_file.write("\n")

        #end tag
        if cur_ind:
            out_file.write(cur_ind)
        out_file.write("</{}>\n".format(self.tag_name))


#a subclass of Element with tag body
class Body(Element):
    """body tag"""
    tag_name = "body"

#subclass for paragraph
class P(Element):
    """paragraph"""
    tag_name = "p"

class Html(Element):
    """html tag"""
    tag_name = "html"

class Head(Element):
    """head tag"""
    tag_name = "head"


class OneLineTag(Element):
    """class for one line with tags"""
    def render(self, out_file, cur_ind=""):
        if cur_ind:
            out_file.write(cur_ind)
        for content in self.content:
            out_file.write("<{}> ".format(self.tag_name))
            try:
                content.render(out_file)
            except AttributeError:
                out_file.write(content)
            out_file.write(" </{}>\n".format(self.tag_name))

    #change the test file with import pytest
    def append(self, content):
        raise NotImplementedError

class Title(OneLineTag):
    """Title class, one line"""
    tag_name = "title"

class SelfClosingTag(Element):
    """"self closing tag"""
    def __init__(self, content=None, **kwargs):
        if content is not None:
            raise TypeError("SelfClosingTag can not contain any content")
        super().__init__(content=content, **kwargs)

    def append(self):
        raise TypeError("You can not add content to a SelfClosingTag")

    #somethinkg like <hr width="400" />
    def render(self, out_file, cur_ind=""):
        if cur_ind:
            out_file.write(cur_ind)
        open_tag = ["<{} ".format(self.tag_name)]
        if self.kwargs:
            for x in self.kwargs:
                open_tag.append(x)
                open_tag.append("=")
                open_tag.append('"{}"'.format(self.kwargs[x]))
                out_file.write("".join(open_tag))
                out_file.write(" ")
        else:
            out_file.write("".join(open_tag))

        out_file.write("/>\n")

class Hr(SelfClosingTag):
    """Hr tag class, self closing tag"""
    tag_name = "hr"

class Br(SelfClosingTag):
    """Br tag, self closing tag"""
    tag_name = "br"

#should look like this <a href="http://google.com">link to google</a>
class A(OneLineTag):
    """anchor tag, one line tag"""
    tag_name = "a"

    def __init__(self, link, content, **kwargs):
        kwargs['href'] = link
        self.content = content
        super().__init__(content, **kwargs)

    def render(self, out_file, cur_ind=""):
        if cur_ind:
            out_file.write(cur_ind)
        open_tag = ["<{} ".format(self.tag_name)]
        if self.kwargs:
            for x in self.kwargs:
                open_tag.append(x)
                open_tag.append("=")
                open_tag.append('"{}"'.format(self.kwargs[x]))
                open_tag.append(">{}".format(self.content[0]))
                out_file.write("".join(open_tag))
        else:
            out_file.write("".join(open_tag))

        out_file.write("</{}>".format(self.tag_name))

class H(OneLineTag):
    """head, one line tag"""
    def __init__(self, level, content=None, **kwargs):
        self.tag_name = "h{}".format(level)
        self.content = [content]
        super().__init__(content, **kwargs)

class Li(OneLineTag):
    """list tag, one line tag"""
    tag_name = "li"

    def render(self, out_file, cur_ind=""):
        if cur_ind:
            out_file.write(cur_ind)
        open_tag = ["<{} ".format(self.tag_name)]
        if self.kwargs:
            for x in self.kwargs:
                open_tag.append(x)
                open_tag.append("=")
                open_tag.append('"{}">'.format(self.kwargs[x]))
                out_file.write("".join(open_tag))
        else:
            open_tag.append(">")
            out_file.write("".join(open_tag))

        for content in self.content:
            try:
                content.render(out_file)
            except AttributeError:
                out_file.write(content)

        out_file.write("</{}>\n".format(self.tag_name))

    def append(self, new_content):
        self.content.append(new_content)

class Ul(Element):
    """Ul tag, normal element"""
    tag_name = "ul"

class Meta(SelfClosingTag):
    """Meta tag, self closing tag """
    tag_name = "meta"
