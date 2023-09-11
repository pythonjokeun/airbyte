#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

import itertools
from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable, List, Optional, Tuple, TypeVar

from airbyte_cdk.destinations.vector_db_based.document_processor import Chunk
from airbyte_cdk.models import AirbyteMessage, ConfiguredAirbyteCatalog


class Indexer(ABC):
    """
    Indexer is an abstract class that defines the interface for indexing documents.

    The Writer class uses the Indexer class to internally index documents generated by the document processor.
    In a destination connector, implement a custom indexer by extending this class and implementing the abstract methods.
    """

    def __init__(self, config: Any):
        self.config = config

    def pre_sync(self, catalog: ConfiguredAirbyteCatalog) -> None:
        """
        Run before the sync starts. This method should be used to make sure all records in the destination that belong to streams with a destination mode of overwrite are deleted.
        """
        pass

    def post_sync(self) -> List[AirbyteMessage]:
        """
        Run after the sync finishes. This method should be used to perform any cleanup operations and can return a list of AirbyteMessages to be logged.
        """
        return []

    @abstractmethod
    def index(self, document_chunks: List[Chunk], delete_ids: List[str]) -> None:
        """
        Index a list of document chunks. This method should be used to index the documents in the destination. The delete_ids parameter contains a list of record ids - all chunks with a record id in this list should be deleted from the destination.
        """
        pass

    @abstractmethod
    def check(self) -> Optional[str]:
        """
        Check if the indexer is configured correctly. This method should be used to check if the indexer is configured correctly and return an error message if it is not.
        """
        pass


T = TypeVar("T")


def chunks(iterable: Iterable[T], batch_size: int) -> Generator[Tuple[T, ...], None, None]:
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    while chunk := tuple(itertools.islice(it, batch_size)):
        yield chunk
