from abc import ABC, abstractmethod


class BaseUseCase(ABC):

    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass
