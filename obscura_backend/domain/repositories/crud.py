class CRUD:
    def create(self, *args, **kwargs):
        raise NotImplementedError("This method should be overridden by subclasses")
    def read(self, *args, **kwargs):
        raise NotImplementedError("This method should be overridden by subclasses")
    def update(self, *args, **kwargs):
        raise NotImplementedError("This method should be overridden by subclasses")
    def delete(self, *args, **kwargs):
        raise NotImplementedError("This method should be overridden by subclasses")