# -*- coding: utf-8 -*-

from html import parser


class customHTMLParser(parser.HTMLParser):

    def __init__(self):
        super(customHTMLParser, self).__init__()
        self.image = ""
        self.author = ""
        self.description = ""
        self.headsUpAuthor = False
        self.headsUpDesc = False

    def handle_starttag(self, tag, attrs):
        #print("Start tag: {0}".format(tag))
        if tag == "img":
            for att in attrs:
                if att[0] == "src":
                    self.image = att[1]
                    return
        elif tag == "a":
            for att in attrs:
                #print(att)
                if att[0] == "href" and str(att[1]).find("rel=authorrel=author") != -1:
                    self.headsUpAuthor = True
                    return



    def handle_endtag(self, tag):
        #print("End tag: {0}".format(tag))
        if tag == "img":
            self.headsUpDesc = True

    def handle_data(self, data):
        #print("Data: {0}".format(data))
        if self.headsUpAuthor:
            self.author = data
            self.headsUpAuthor = False
            return
        elif self.headsUpDesc:
            self.description = data
            self.headsUpDesc = False
            
    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        pass

    def retrieve_info(self):
        return self.description, self.description.split(".")[0], self.author, self.image
