import hypothesis.strategies as st
from hypothesis.strategies import characters, composite, text


@composite
def passwords(draw):
    uppercase = characters(whitelist_categories=["Lu"])
    lowercase = characters(whitelist_categories=["Ll"])
    digits = characters(whitelist_categories=["Nd"])
    special = characters(whitelist_categories=["Po", "Sc"])
    uppercase_char = draw(uppercase)
    lowercase_char = draw(lowercase)
    digit_char = draw(digits)
    special_char = draw(special)

    others = draw(
        text(
            characters(blacklist_characters=["\n", "\r", "\t", "\x0b", "\x0c"]),
            min_size=4,
            max_size=4,
        )
    )

    password_list = list(
        uppercase_char + lowercase_char + digit_char + special_char + others
    )
    rng = draw(st.randoms())
    rng.shuffle(password_list)
    return "".join(password_list)
