import re

next_char = re.compile(r"[\(\)\[\]\{\},\"\'`]", re.MULTILINE)


def get_args(data, offset=0):
    if not data or data[offset] != "(":
        raise ValueError("Failed to find function args (No leading paren)")
    arg_indicies = [offset]
    paren_count = 1
    offset += 1
    while paren_count > 0:
        m = next_char.search(data, offset)
        if not m:
            raise ValueError("Failed to find function args (eof before matching all parens)")
        char = m.group()
        offset = m.span()[1]
        if char in "([{":
            paren_count += 1
        elif char in ")]}":
            paren_count -= 1
        elif char == ",":
            if paren_count == 1:
                arg_indicies.append(offset)
        else:
            # TODO: correct support for ` is harder
            end_quote = re.compile(r"(?<!\\)%s" % char, re.MULTILINE)
            quote_m = end_quote.search(data, offset)
            if not quote_m:
                raise ValueError("Failed to find function args (failed to find end of string)")
            offset = quote_m.span()[1]

    arg_indicies.append(offset)
    args = []
    if len(arg_indicies) > 1:
        for start, end in zip(arg_indicies[:-1], arg_indicies[1:]):
            if end - 1 <= start + 1:
                # Empty trailing args are allowed but we don't check where they are
                continue
            arg = data[start + 1:end - 1].strip()
            if arg:
                args.append(arg)

    return args
