from awesome_align.run_align import word_align

from .base import AppService
from .sentence_pair import SentencePairCRUD
from ..models.dataset import Dataset
from ..models.sentence_pair import SentencePair
from ..models.alignment import AlignmentStatus, AlignmentActionInfo, AlignmentInUpdate, ReleaseAlignmentStatus, OPEN_STATUSES
from ..core.aligner import Aligner
from ..core.utils import process_raw_alignments


class AlignmentService(AppService):
    async def request_to_acquire_sentence_pair(self, sentence_pair: SentencePair) -> AlignmentActionInfo:
        if not sentence_pair.is_free_to_acquire():
            return AlignmentActionInfo(success=False, message=f"Failed to acquire a {sentence_pair.status} sentence pair")

        await SentencePairCRUD(self.db, self.current_user, self.session).update_status(sentence_pair, new_status=AlignmentStatus.aligning)
        return AlignmentActionInfo(success=True, message=f"Successfully acquired")


    async def release_sentence_pair_with_alignment_status(self, sentence_pair: SentencePair, status: ReleaseAlignmentStatus) -> AlignmentActionInfo:
        new_status = AlignmentStatus(status)
        await SentencePairCRUD(self.db, self.current_user, self.session).update_status(sentence_pair, new_status=new_status)
        return AlignmentActionInfo(success=True, message=f"Successfully released")

    async def mark_sentence_pair_as_aligned(self, sentence_pair: SentencePair) -> AlignmentActionInfo:
        await SentencePairCRUD(self.db, self.current_user, self.session).update_status(sentence_pair, new_status=AlignmentStatus.aligned)
        return AlignmentActionInfo(success=True, message=f"Successfully aligned")


    async def update_alignments_of_sentence_pair(self, sentence_pair: SentencePair, alignments_param: AlignmentInUpdate) -> SentencePair:
        new_sentence_pair = sentence_pair.copy()
        new_sentence_pair.alignments = alignments_param.alignments

        await SentencePairCRUD(self.db, self.current_user, self.session).update_alignments(sentence_pair.id, new_alignments=new_sentence_pair.alignments)

        return new_sentence_pair


    async def auto_align_sentence_pair(self, aligner: Aligner, sentence_pair: SentencePair) -> SentencePair:
        sentence_pairs = [[sentence_pair.src_tokenize, sentence_pair.tgt_tokenize, str(sentence_pair.id)]]
        raw_alignments_from_model = word_align(aligner.model, aligner.tokenizer, sentence_pairs)

        alignments = process_raw_alignments(raw_alignments_from_model[str(sentence_pair.id)])
       
        await SentencePairCRUD(self.db, self.current_user, self.session).update_alignments(sentence_pair.id, alignments)

        sentence_pair.alignments = alignments

        return sentence_pair


    async def auto_align_dataset(self, aligner: Aligner, dataset: Dataset) -> AlignmentActionInfo:
        sentence_pairs_in_db = await SentencePairCRUD(self.db, self.current_user).get_sentence_pair_from_dataset_with_status(dataset, OPEN_STATUSES)
        sentence_pairs = []
        for row in sentence_pairs_in_db:
            sentence_pairs.append([row.src_tokenize, row.tgt_tokenize, str(row.id)])

        raw_alignments_from_model = word_align(aligner.model, aligner.tokenizer, sentence_pairs)

        for row in sentence_pairs_in_db:
            alignments = process_raw_alignments(raw_alignments_from_model[str(row.id)])

            await SentencePairCRUD(self.db, self.current_user, self.session).update_alignments(row.id, alignments)
            
        return AlignmentActionInfo(success=True, message=f"Successfully auto alignment all sentence pairs of the dataset")


