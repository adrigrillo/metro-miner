import re

from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token

from metro_analyzer import config


class MetroLinesRecognizer(object):
    """Pipeline component that recognises the Madrid underground system lines
    and sets entity annotations to the text that holds them. This allow the
    easy recognition and handling of the lines.

    The lines are labelled as FACILITY and their spans are merged into one token.
    Additionally, ._.has_metro_line and ._.is_metro_line is set on the
    Doc/Span and Token respectively
    """
    name = 'metro_lines_recognizer'  # component name, will show up in the pipeline

    def __init__(self, nlp):
        """
        Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the configured lines (config.ini) and
        generate Doc objects as phrase match patterns.

        :param nlp: spaCy nlp instance
        """
        self.label = nlp.vocab.strings['FACILITY']  # get entity label ID

        LINE_PATTERN = re.compile('l([i|í]nea){0,1}', re.IGNORECASE)
        LONG_METRO_LINE_PATTERN = re.compile('l([i|í]nea){0,1}[ -]{0,1}(1[0-2]|[1-9])', re.IGNORECASE)

        line_flag = lambda text: bool(LINE_PATTERN.match(text))
        IS_LINE = nlp.vocab.add_flag(line_flag)
        metro_line_flag = lambda text: bool(LONG_METRO_LINE_PATTERN.match(text))
        IS_METRO_LINE = nlp.vocab.add_flag(metro_line_flag)

        # Set up the PhraseMatcher – it can now take Doc objects as patterns,
        # so even if the list of companies is long, it's very efficient
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('METRO_LINES', None, [{IS_LINE: True}, {'IS_SPACE': True}, {'IS_DIGIT': True}],
                         [{IS_LINE: True}, {'IS_DIGIT': True}], [{IS_METRO_LINE: True}])

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension('is_metro_line', default=False)

        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_element_matched == True.
        Doc.set_extension('has_metro_line', getter=self.has_metro_line)
        Span.set_extension('has_metro_line', getter=self.has_metro_line)

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and modify it if matches
        are found. Return the Doc, so it can be processed by the next component
        in the pipeline, if available.

        :param doc: text to be analysed
        :return: text updated with the tags and the entities matched
        """
        matches = self.matcher(doc)
        spans = []  # keep the spans for later so we can merge them afterwards
        for _, start, end in matches:
            # Generate Span representing the entity and set label
            entity = Span(doc, start, end, label=self.label)
            spans.append(entity)
            # Set custom attribute on each token of the entity
            for token in entity:
                token._.set('is_metro_line', True)
            # Overwrite doc.ents and add entity
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token.
            span.merge()
        return doc

    @staticmethod
    def has_metro_line(tokens):
        """
        Getter for Doc and Span attributes

        :param tokens: tokens of the Doc or the Span, that is, the text
        :return: True if one of the tokens is a matched element
        """
        return any([token._.get('is_metro_line') for token in tokens])


class MetroStationsRecognizer(object):
    """Pipeline component that recognises the Madrid underground system stations
    and sets entity annotations to the text that holds them. This allow the
    easy recognition and handling of the stations.

    The stations are labelled as FACILITY and their spans are merged into one token.
    Additionally, ._.has_metro_station and ._.is_metro_station is set on the
    Doc/Span and Token respectively
    """
    name = 'metro_stations'  # component name, will show up in the pipeline

    def __init__(self, nlp):
        """
        Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the configured stations (config.ini) and
        generate Doc objects as phrase match patterns.

        :param nlp: spaCy nlp instance
        """
        self.label = nlp.vocab.strings['FACILITY']  # get entity label ID

        # Set up the PhraseMatcher – it can now take Doc objects as patterns,
        # so even if the list of companies is long, it's very efficient
        metro_stations = config['keywords']['stations'].split(',')
        metro_stations += config['keywords']['stations_lw'].split(',')
        patterns = [nlp(org) for org in metro_stations]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('METRO_STATIONS', None, *patterns)

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension('is_metro_station', default=False)

        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_element_matched == True.
        Doc.set_extension('has_metro_station', getter=self.has_metro_station)
        Span.set_extension('has_metro_station', getter=self.has_metro_station)

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and modify it if matches
        are found. Return the Doc, so it can be processed by the next component
        in the pipeline, if available.

        :param doc: text to be analysed
        :return: text updated with the tags and the entities matched
        """
        matches = self.matcher(doc)
        spans = []  # keep the spans for later so we can merge them afterwards
        for _, start, end in matches:
            # Generate Span representing the entity and set label
            entity = Span(doc, start, end, label=self.label)
            spans.append(entity)
            # Set custom attribute on each token of the entity
            for token in entity:
                token._.set('is_metro_station', True)
            # Overwrite doc.ents and add entity
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token.
            span.merge()
        return doc

    @staticmethod
    def has_metro_station(tokens):
        """
        Getter for Doc and Span attributes

        :param tokens: tokens of the Doc or the Span, that is, the text
        :return: True if one of the tokens is a matched element
        """
        return any([token._.get('is_metro_station') for token in tokens])