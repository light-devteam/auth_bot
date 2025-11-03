from typing import Any

from msgspec.json import Encoder, Decoder


def __encoder_hook(object: Any) -> Any:
    raise TypeError(f'Object of type {type(object)} is not JSON serializable')


json_encoder = Encoder(enc_hook=__encoder_hook)

json_decoder = Decoder()
