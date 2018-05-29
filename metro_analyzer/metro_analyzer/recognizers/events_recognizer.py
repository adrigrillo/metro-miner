from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token


class MetroFaultsRecognizer(object):
    """Pipeline component that recognises the Madrid underground system fautls
    and sets entity annotations to the text that holds them. This allow the
    easy recognition and handling of the faults.

    The faults are labelled as an EVENT and their spans are merged into one token.
    Additionally, ._.has_metro_fault and ._.is_metro_fault is set on the
    Doc/Span and Token respectively
    """
    name = 'faults_recognizer'  # component name, will show up in the pipeline

    def __init__(self, nlp):
        """
        Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the configured lines (config.ini) and
        generate Doc objects as phrase match patterns.

        :param nlp: spaCy nlp instance
        """
        self.label = nlp.vocab.strings['EVENT']  # get entity label ID
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('METRO_FAULTS', None, [{'LOWER': 'circulación'}, {'LOWER': 'interrumpida'}],
                         [{'LOWER': 'incidencia'}],
                         [{'LOWER': 'circulacion'}, {'LOWER': 'interrumpida'}],
                         [{'LOWER': 'circulación'}, {'LOWER': 'lenta'}],
                         [{'LOWER': 'circulacion'}, {'LOWER': 'lenta'}],
                         [{'LOWER': 'tramo'}, {'LOWER': 'interrumpido'}],
                         [{'LOWER': 'tramo'}, {'LOWER': 'cortado'}],
                         [{'LOWER': 'servicio'}, {'LOWER': 'interrumpido'}],
                         [{'LOWER': 'servicio'}, {'LOWER': 'cortado'}],
                         [{'LOWER': 'trenes'}, {'LOWER': 'no'}, {'LOWER': 'efectúan'}, {'LOWER': 'parada'}],
                         [{'LOWER': 'trenes'}, {'LOWER': 'no'}, {'LOWER': 'efectuan'}, {'LOWER': 'parada'}])

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension('is_metro_fault', default=False)

        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_element_matched == True.
        Doc.set_extension('has_metro_fault', getter=self.has_metro_fault)
        Span.set_extension('has_metro_fault', getter=self.has_metro_fault)

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
                token._.set('is_metro_fault', True)
            # Overwrite doc.ents and add entity
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token.
            span.merge()
        return doc

    @staticmethod
    def has_metro_fault(tokens):
        """
        Getter for Doc and Span attributes

        :param tokens: tokens of the Doc or the Span, that is, the text
        :return: True if one of the tokens is a matched element
        """
        return any([token._.get('is_metro_fault') for token in tokens])


class MetroDelaysRecognizer(object):
    """Pipeline component that recognises the Madrid underground system delays
    and sets entity annotations to the text that holds them. This allow the
    easy recognition and handling of the delays.

    The delays are labelled as an EVENT and their spans are merged into one token.
    Additionally, ._.has_metro_delay and ._.is_metro_delay is set on the
    Doc/Span and Token respectively
    """
    name = 'delays_recognizer'  # component name, will show up in the pipeline

    def __init__(self, nlp):
        """
        Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the configured lines (config.ini) and
        generate Doc objects as phrase match patterns.

        :param nlp: spaCy nlp instance
        """
        self.label = nlp.vocab.strings['EVENT']  # get entity label ID
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('METRO_DELAYS', None, [{'LOWER': 'retrasos'}], [{'LOWER': 'retraso'}],
                         [{'LOWER': 'frequencia'}],
                         [{'LOWER': 'minutos'}, {'LOWER': 'de'}, {'LOWER': 'espera'}],
                         [{'LOWER': 'min'}, {'LOWER': 'de'}, {'LOWER': 'espera'}],
                         [{'LOWER': 'minutos'}, {'LOWER': 'de'}, {'LOWER': 'retraso'}],
                         [{'LOWER': 'min'}, {'LOWER': 'de'}, {'LOWER': 'retraso'}],
                         [{'LOWER': 'minutos'}, {'LOWER': 'esperando'}],
                         [{'LOWER': 'tiempo'}, {'LOWER': 'de'}, {'LOWER': 'espera'}],
                         [{'LOWER': 'tiempos'}, {'LOWER': 'de'}, {'LOWER': 'espera'}],
                         [{'LOWER': 'frecuencia'}, {'LOWER': 'de'}, {'LOWER': 'paso'}],
                         [{'LOWER': 'frecuencias'}, {'LOWER': 'de'}, {'LOWER': 'paso'}],
                         [{'LOWER': 'frecuencias'}, {'LOWER': 'de'}, {'LOWER': 'trenes'}])

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension('is_metro_delay', default=False)

        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_element_matched == True.
        Doc.set_extension('has_metro_delay', getter=self.has_metro_delay)
        Span.set_extension('has_metro_delay', getter=self.has_metro_delay)

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
                token._.set('is_metro_delay', True)
            # Overwrite doc.ents and add entity
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token.
            span.merge()
        return doc

    @staticmethod
    def has_metro_delay(tokens):
        """
        Getter for Doc and Span attributes

        :param tokens: tokens of the Doc or the Span, that is, the text
        :return: True if one of the tokens is a matched element
        """
        return any([token._.get('is_metro_delay') for token in tokens])


class MetroSolutionsRecognizer(object):
    """Pipeline component that recognises the Madrid underground system solutions to faults
    abd delays and sets entity annotations to the text that holds them. This allow the
    easy recognition and handling of the solutions.

    The solutions are labelled as an EVENT and their spans are merged into one token.
    Additionally, ._.has_metro_solution and ._.is_metro_solution is set on the
    Doc/Span and Token respectively
    """
    name = 'solutions_recognizer'  # component name, will show up in the pipeline

    def __init__(self, nlp):
        """
        Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the configured lines (config.ini) and
        generate Doc objects as phrase match patterns.

        :param nlp: spaCy nlp instance
        """
        self.label = nlp.vocab.strings['EVENT']  # get entity label ID
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('METRO_SOLUTIONS', None, [{'LOWER': 'circulación'}, {'LOWER': 'normalizada'}],
                         [{'LOWER': 'circulacion'}, {'LOWER': 'normalizada'}],
                         [{'LOWER': 'servicio'}, {'LOWER': 'normalizado'}],
                         [{'LOWER': 'normalizado'}, {'LOWER': 'el'}, {'LOWER': 'servicio'}],
                         [{'LOWER': 'restablecido'}, {'LOWER': 'el'}, {'LOWER': 'servicio'}],
                         [{'LOWER': 'ya'}, {'LOWER': 'efectúan'}, {'LOWER': 'parada'}],
                         [{'LOWER': 'ya'}, {'LOWER': 'efectuan'}, {'LOWER': 'parada'}])

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension('is_metro_solution', default=False)

        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_element_matched == True.
        Doc.set_extension('has_metro_solution', getter=self.has_metro_solution)
        Span.set_extension('has_metro_solution', getter=self.has_metro_solution)

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
                token._.set('is_metro_solution', True)
            # Overwrite doc.ents and add entity
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token.
            span.merge()
        return doc

    @staticmethod
    def has_metro_solution(tokens):
        """
        Getter for Doc and Span attributes

        :param tokens: tokens of the Doc or the Span, that is, the text
        :return: True if one of the tokens is a matched element
        """
        return any([token._.get('is_metro_solution') for token in tokens])


class MetroStrikesRecognizer(object):
    """Pipeline component that recognises the Madrid underground system strikes
    and sets entity annotations to the text that holds them. This allow the
    easy recognition and handling of the delays.

    The strikes are labelled as an EVENT and their spans are merged into one token.
    Additionally, ._.has_metro_strike and ._.is_metro_strike is set on the
    Doc/Span and Token respectively
    """
    name = 'strikes_recognizer'  # component name, will show up in the pipeline

    def __init__(self, nlp):
        """
        Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the configured lines (config.ini) and
        generate Doc objects as phrase match patterns.

        :param nlp: spaCy nlp instance
        """
        self.label = nlp.vocab.strings['EVENT']  # get entity label ID
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('METRO_STRIKES', None, [{'LOWER': 'huelga'}], [{'LOWER': 'paros'}],
                         [{'LOWER': 'servicios'}, {'LOWER': 'minimos'}],
                         [{'LOWER': 'servicios'}, {'LOWER': 'mínimos'}],
                         [{'LOWER': 'paros'}, {'LOWER': 'convocados'}, {'LOWER': 'para'}, {'LOWER': 'hoy'}],
                         [{'LOWER': 'paros'}, {'LOWER': 'convocados'}, {'LOWER': 'para'}, {'LOWER': 'mañana'}],
                         [{'LOWER': 'paros'}, {'LOWER': 'convocados'}, {'LOWER': 'para'}, {'LOWER': 'el'},
                          {'LOWER': 'dia'}, {'IS_DIGIT': True}],
                         [{'LOWER': 'paros'}, {'LOWER': 'convocados'}, {'LOWER': 'para'}, {'LOWER': 'el'},
                          {'LOWER': 'día'}, {'IS_DIGIT': True}],
                         [{'LOWER': 'paros'}, {'LOWER': 'convocados'}])

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension('is_metro_strike', default=False)

        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_element_matched == True.
        Doc.set_extension('has_metro_strike', getter=self.has_metro_strike)
        Span.set_extension('has_metro_strike', getter=self.has_metro_strike)

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
                token._.set('is_metro_strike', True)
            # Overwrite doc.ents and add entity
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token.
            span.merge()
        return doc

    @staticmethod
    def has_metro_strike(tokens):
        """
        Getter for Doc and Span attributes

        :param tokens: tokens of the Doc or the Span, that is, the text
        :return: True if one of the tokens is a matched element
        """
        return any([token._.get('is_metro_strike') for token in tokens])
