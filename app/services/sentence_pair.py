from ..core.config import db_name, sentence_pairs_collection_name
from .base import AppService, AppCRUD
from .dataset import DatasetService
from ..models.sentence_pair import SentencePair, SentencePairInCreate, SentencePairInDB
from ..models.dataset import Dataset

class SentencePairService(AppService):
    async def new_sentence_pair_for_dataset(self, sentence_pair_params: SentencePairInCreate, dataset_slug: str) -> SentencePair:
        dataset = await DatasetService(self.db, self.current_user).get_dataset(dataset_slug)

        db_sentence_pair = await SentencePairCRUD(self.db, session=self.session).new_sentence_pair_for_dataset(sentence_pair_params, dataset)
        sentence_pair = SentencePair(**db_sentence_pair.dict(), dataset=dataset)

        return sentence_pair


class SentencePairCRUD(AppCRUD):
    async def new_sentence_pair_for_dataset(self, sentence_pair_params: SentencePairInCreate, dataset: Dataset) -> SentencePairInDB:
        src_sent = sentence_pair_params.src_sent.strip()
        tgt_sent = sentence_pair_params.tgt_sent.strip()
        src_tokenize = src_sent.split()
        tgt_tokenize = tgt_sent.split()
        sentence_pair_doc = SentencePairInDB(
            dataset_slug=dataset.slug,
            src_tokenize=src_tokenize, tgt_tokenize=tgt_tokenize,
            src_sent=src_sent, tgt_sent=tgt_sent
        )

        await self.db[db_name][sentence_pairs_collection_name].insert_one(sentence_pair_doc.dict(), session=self.session)

        return sentence_pair_doc
