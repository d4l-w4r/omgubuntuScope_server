# -*- coding: utf-8 -*-
###
# Author: Daniel Waller <2waller@informatik.uni-hamburg.de>
#
###

from html import parser

###
# Custom extension of the html.parser.HTMLParser class to handle the parsing
# of the inner CDATA html in each <item> of the omgubuntu rss feed.
# It will parse the description tag of the item to filter out a long description,
# short description, author name, and thumbnail url
#
# @method retrieve_info() – only useful accessible method that will return the
# parsed result after customHTMLParser.feed("html_string") has finished
###
class customHTMLParser(parser.HTMLParser):

    def __init__(self):
        super(customHTMLParser, self).__init__()
        self.image = ""
        self.author = ""
        self.description = ""
        #flags to denote that the next time a 'data' field is encountered it will contain the desired information
        self.headsUpAuthor = False
        self.headsUpDesc = False

    ###
    # Function called every time an opening tag is encountered in the html
    #
    # @param str, str – the type of tag (eg. <a>, <div>, etc.),
    # and the associated attributes (eg. src="", id="", etc.) that were encountered
    ###
    def handle_starttag(self, tag, attrs):
        #if the tag is an <img> and it has a src="" attribute, we know it stores
        #our thumbnail url. Attributes are represented as a list of ("key", "value") tuples
        if tag == "img":
            for att in attrs:
                if att[0] == "src":
                    self.image = att[1]
                    return
        #if a tag is an <a> and has a href="" attribute that contains the string
        #"rel=authorrel=author" in its value we know that the next datablock we encounter
        #will be the authors name so we set the headsUpAuthor flag to be able to properly react
        elif tag == "a":
            for att in attrs:
                if att[0] == "href" and str(att[1]).find("rel=authorrel=author") != -1:
                    self.headsUpAuthor = True
                    return

    ###
    # Function called every time a closing tag is encountered in the html
    #
    # @param str – the type of tag that was encountered (eg. <a>, <div>, etc.)
    ###
    def handle_endtag(self, tag):
        #from looking at the xml we know that everytime the </img> that closes the thumbnail
        #appears, the description will be on the next block of data.
        #so we set the headsUpDesc flag
        if tag == "img":
            self.headsUpDesc = True

    ###
    # Function called every time a general data block (like plain text in a <p>)
    # is encountered in the html
    #
    # @param str – the string of data that was encountered
    ###
    def handle_data(self, data):
        #if the appropriate flag is set, store data as the desired information
        if self.headsUpAuthor:
            self.author = data
            self.headsUpAuthor = False #unset the flag so the information isn't
            return                     #overwritten when the next data block is encountered
        elif self.headsUpDesc:
            self.description = data
            self.headsUpDesc = False

    ###
    # Function needs to be called after the HTMLParser.feed() function has been
    # called on this object instance!
    # Returns the values that have been parsed from the html block
    #
    # @return str, str, str, str – description, short description, author name,
    # and thumbnail url for the given article
    ###
    def retrieve_info(self):
        return self.description, self.description.split(".")[0], self.author, self.image


######## Unimportant for our purposes ########
    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        pass
###############################################
