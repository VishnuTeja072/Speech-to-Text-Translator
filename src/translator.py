# src/translator.py
_tokenizer = None
_model = None
# Use a public, non-gated model for English-to-Telugu translation
_model_name = "facebook/mbart-large-50-one-to-many-mmt"

def _load_model():
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    except Exception as e:
        raise ImportError(
            "Missing dependency: install 'transformers' and 'sentencepiece' (pip install transformers sentencepiece)"
        ) from e

    tokenizer = AutoTokenizer.from_pretrained(_model_name, token=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(_model_name, token=False)
    return tokenizer, model

def translate_text(text, target_lang_code="te_IN"):
    """Translate English text using mBART-50 (multilingual translation).

    Args:
        text: English text to translate.
        target_lang_code: mBART language code (e.g., "te_IN" for Telugu, "hi_IN" for Hindi).

    The model and tokenizer are loaded lazily to avoid heavy downloads at import time.
    Uses Facebook's mBART-50 which supports 50+ languages including Telugu, Hindi, Tamil.
    """
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer, _model = _load_model()

    # Set source language to English
    _tokenizer.src_lang = "en_XX"
    
    # Encode the input text
    tokens = _tokenizer(text, return_tensors="pt", padding=True)
    
    # Get the target language token ID from the tokenizer's lang_code_to_id mapping
    target_lang_id = _tokenizer.lang_code_to_id.get(target_lang_code)
    if target_lang_id is None:
        raise ValueError(f"Unsupported language code: {target_lang_code}")
    
    # Generate translation with the target language as the decoder start token
    translated = _model.generate(**tokens, forced_bos_token_id=target_lang_id)
    
    # Decode the translation
    decoded = _tokenizer.batch_decode(translated, skip_special_tokens=True)
    return decoded[0] if decoded else ""
