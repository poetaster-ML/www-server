class SyntaxBackend:
    def get_context_free_grammar_parse(self, text: str):
        raise NotImplementedError()

    def get_xbar_parse(self, text: str):
        raise NotImplementedError()

    def get_government_binding_parse(self, text: str):
        raise NotImplementedError()

    def get_lexical_functional_parse(self, text: str):
        raise NotImplementedError()

    def get_head_driven_phrase_structure_parse(self, text: str):
        raise NotImplementedError()

    def get_tree_adjoining_parse(self, text: str):
        raise NotImplementedError()

    def get_combinatory_categorial_grammar_parse(self, text: str):
        raise NotImplementedError()

    def get_dependency_parse(self, text: str):
        raise NotImplementedError()


class SemanticBackend:
    def get_lambda_ccg(self, tokens: list):
        raise NotImplementedError()


class BaseBackend:
    def get_tokens(self):
        raise NotImplementedError()

    def get_parts_of_speech(self):
        raise NotImplementedError()

    def get_constituency_parse(self):
        raise NotImplementedError()
