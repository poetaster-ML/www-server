class BaseBackend:
    def get_tokens(self):
        raise NotImplementedError()

    def get_parts_of_speech(self):
        raise NotImplementedError()

    def get_dependency_parse(self):
        raise NotImplementedError()
