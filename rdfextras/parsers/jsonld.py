# -*- coding: UTF-8 -*-
"""
This serialiser will read in an JSON-LD formatted document and create an RDF
Graph. See:

    http://json-ld.org/

Example usage::

    >>> from rdflib import Graph, plugin, URIRef, Literal
    >>> from rdflib.parser import Parser
    >>> plugin.register('json-ld', Parser,
    ...     'rdfextras.parsers.jsonld', 'JsonLDParser')
    >>> test_json = '''
    ... {
    ...     "@context": {
    ...         "dc": "http://purl.org/dc/terms/",
    ...         "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    ...         "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
    ...     },
    ...     "@id": "http://example.org/about",
    ...     "dc:title": {
    ...         "@language": "en",
    ...         "@literal": "Someone's Homepage"
    ...     }
    ... }
    ... '''
    >>> g = Graph().parse(data=test_json, format='json-ld')
    >>> list(g) == [(URIRef('http://example.org/about'),
    ...     URIRef('http://purl.org/dc/terms/title'),
    ...     Literal(u"Someone's Homepage", lang=u'en'))]
    True

"""
# NOTE: This code reads the entire JSON object into memory before parsing, but
# we should consider streaming the input to deal with arbitrarily large graphs.

import warnings

from rdflib.parser import Parser
from rdflib.namespace import RDF, XSD
from rdflib.term import URIRef, BNode, Literal

from rdfextras.ldcontext import Context, Term, CONTEXT_KEY, ID_KEY, LIST_KEY
from rdfextras.ldcontext import json, source_to_json


class JsonLDParser(Parser):
    def __init__(self):
        super(JsonLDParser, self).__init__()

    def parse(self, source, sink, **kwargs):
        encoding = kwargs.get('encoding') or 'utf-8'
        if encoding not in ('utf-8', 'utf-16'):
            warnings.warn("JSON should be encoded as unicode. " +
                    "Given encoding was: %s" % encoding)

        base = kwargs.get('base') or sink.absolutize(
                source.getPublicId() or source.getSystemId() or "")

        context_data = kwargs.get('context')

        tree = source_to_json(source)
        to_rdf(tree, sink, base, context_data)


def to_rdf(tree, graph, base=None, context_data=None):
    context = Context()
    context.load(context_data or tree.get(CONTEXT_KEY) or {}, base)

    id_obj = tree.get(context.id_key)
    resources = id_obj if isinstance(id_obj, list) else [tree]

    for term in context.terms:
        if term.iri and term.iri.endswith(('/', '#', ':')):
            graph.bind(term.key, term.iri)

    state = graph, context, base
    for node in resources:
        _add_to_graph(state, node)

    return graph


def _add_to_graph(state, node):
    graph, context, base = state
    id_val = node.get(context.id_key)
    subj = URIRef(context.expand(id_val), base) if id_val else BNode()

    for pred_key, obj_nodes in node.items():
        if pred_key in (CONTEXT_KEY, context.id_key):
            continue
        if pred_key == context.type_key:
            pred = RDF.type
            term = Term(None, None, context.id_key)
        else:
            pred_uri = context.expand(pred_key)
            pred = URIRef(pred_uri)
            term = context.get_term(pred_uri)

        if not isinstance(obj_nodes, list):
            obj_nodes = [obj_nodes]

        if term and term.container == LIST_KEY:
            obj_nodes = [{context.list_key: obj_nodes}]

        for obj_node in obj_nodes:
            obj = _to_object(state, term, obj_node)
            graph.add((subj, pred, obj))

    return subj


def _to_object(state, term, node):
    graph, context, base = state

    if isinstance(node, dict) and context.list_key in node:
        node_list = node.get(context.list_key)
        if node_list:
            first_subj = BNode()
            l_subj, l_next = first_subj, None
            for l_node in node_list:
                if l_next:
                    graph.add((l_subj, RDF.rest, l_next))
                    l_subj = l_next
                l_obj = _to_object(state, None, l_node)
                graph.add((l_subj, RDF.first, l_obj))
                l_next = BNode()
            graph.add((l_subj, RDF.rest, RDF.nil))
            return first_subj
        else:
            node = {context.id_key: unicode(RDF.nil)}

    if not isinstance(node, dict):
        if not term or not term.coercion:
            if isinstance(node, float):
                # TODO: JSON-LD promotes double over decimal; verify correctness...
                return Literal(node, datatype=XSD.double)
            return Literal(node, lang=context.lang)
        else:
            if term.coercion == ID_KEY:
                node = {context.id_key: context.expand(node)}
            else:
                node = {context.type_key: term.coercion,
                        context.literal_key: node}

    if context.lang_key in node:
        return Literal(node[context.literal_key], lang=node[context.lang_key])
    elif context.type_key and context.literal_key in node:
        return Literal(node[context.literal_key],
                datatype=context.expand(node[context.type_key]))
    else:
        return _add_to_graph(state, node)

