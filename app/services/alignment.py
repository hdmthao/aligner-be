from awesome_align.run_align import word_align


from .base import AppService
from .sentence_pair import SentencePairCRUD
from ..models.sentence_pair import SentencePair
from ..models.alignment import AlignmentStatus, AlignmentActionInfo, AlignmentInUpdate
from ..core.aligner import Aligner
from ..core.utils import process_raw_alignments


class AlignmentService(AppService):
    async def request_to_acquire_sentence_pair(self, sentence_pair: SentencePair) -> AlignmentActionInfo:
        if not sentence_pair.is_free_to_acquire():
            return AlignmentActionInfo(success=False, message=f"Failed to acquire a {sentence_pair.status} sentence pair")

        await SentencePairCRUD(self.db, self.current_user, self.session).update_status(sentence_pair, new_status=AlignmentStatus.aligning)
        return AlignmentActionInfo(success=True, message=f"Successfully acquired")


    async def mark_sentence_pair_as_aligned(self, sentence_pair: SentencePair) -> AlignmentActionInfo:
        await SentencePairCRUD(self.db, self.current_user, self.session).update_status(sentence_pair, new_status=AlignmentStatus.aligned)
        return AlignmentActionInfo(success=True, message=f"Successfully aligned")


    async def update_alignments_of_sentence_pair(self, sentence_pair: SentencePair, alignments_param: AlignmentInUpdate) -> SentencePair:
        new_sentence_pair = sentence_pair.copy()
        new_sentence_pair.alignments = alignments_param.alignments

        await SentencePairCRUD(self.db, self.current_user, self.session).update_alignments(sentence_pair, new_alignments=new_sentence_pair.alignments)

        return new_sentence_pair


    async def auto_align_sentence_pair(self, aligner: Aligner, sentence_pair: SentencePair) -> SentencePair:
        sentence_pairs = [[sentence_pair.src_tokenize, sentence_pair.tgt_tokenize]]
        raw_alignments_from_model = word_align(aligner.model, aligner.tokenizer, sentence_pairs)

        alignments = process_raw_alignments(raw_alignments_from_model[0])
        
        await SentencePairCRUD(self.db, self.current_user, self.session).update_alignments(sentence_pair, alignments)

        sentence_pair.alignments = alignments

        return sentence_pair
