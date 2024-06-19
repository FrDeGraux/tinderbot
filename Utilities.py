class Utilities:
    def extract_after_colon_newline_partition(in_str):
        before, sep, after = in_str.partition(":\n\n")
        if sep:
            return after.strip()
        return in_str


