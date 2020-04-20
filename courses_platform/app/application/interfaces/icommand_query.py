import abc


class ICommandQuery(abc.ABC):

    @abc.abstractmethod
    def execute(self, request):
        pass
