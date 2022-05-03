from awesome_align import modeling
from awesome_align.modeling import BertForMaskedLM
from awesome_align.configuration_bert import BertConfig
from awesome_align.tokenization_bert import BertTokenizer
from awesome_align.run_align import set_seed

from .config import ENVIRONMENT

class Aligner:
    model: BertForMaskedLM 
    tokenizer: BertTokenizer 


aligner = Aligner()


async def load_aligner():
    set_seed(1234)

    model_path = "aligner-model"
    config = BertConfig.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    modeling.PAD_ID = tokenizer.pad_token_id
    modeling.CLS_ID = tokenizer.cls_token_id
    modeling.SEP_ID = tokenizer.sep_token_id

    if ENVIRONMENT == 'development':
        model = BertForMaskedLM.from_pretrained(model_path, config=config)
    else:
        model = BertForMaskedLM(config=config)

    aligner.model = model
    aligner.tokenizer = tokenizer


async def get_aligner() -> Aligner:
    return aligner
