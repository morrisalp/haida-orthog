import re


class Converter:
    
    SCHEMES = ["Lachler", "Texting", "Leer", "Enrico", "Swanton", "Lachler-CopyPaste"]

    def __init__(self):
        self.mappings = {
            ("Lachler", "Texting"): self._lachler_to_texting,
            ("Texting", "Lachler"): self._texting_to_lachler,
            ("Lachler", "Lachler-CopyPaste"): self._lachler_to_cp,
            ("Lachler-CopyPaste", "Lachler"): self._cp_to_lachler,
        }
    
    def _lachler_to_texting(self, text):
        equivs = "ḵ g̱ x̱ ĝ x̂".split()
        equivs_ = "kh gh xh G X".split()
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)
            text = text.replace(x.title(), y.title()) # handle uppercase
        return text

    def _texting_to_lachler(self, text):
        equivs = "kh gh xh".split()
        equivs_ = "ḵ g̱ x̱".split()
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)
            text = text.replace(x.title(), y.title()) # handle uppercase
        # Have to handle carons separately to avoid bug
        # with e.g. "Xh" getting both underline and caron
        # Heuristic: non-initial capitals get caron
        # NOTE: Can't handle initial carons.
        text = re.sub(r"([^ ])G", r"\g<1>ĝ", text)
        text = re.sub(r"([^ ])X", r"\g<1>x̂", text)
        return text

    def _lachler_to_cp(self, text):
        equivs = "ḵ g̱ x̱ ĝ x̂ -".split()
        equivs_ = "ñ ç ý ð þ ¬".split()
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)
            text = text.replace(x.title(), y.title()) # handle uppercase
        return text
    
    def _cp_to_lachler(self, text):
        equivs = "ñ ç ý ð þ ¬".split()
        equivs_ = "ḵ g̱ x̱ ĝ x̂ -".split()
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)
            text = text.replace(x.title(), y.title()) # handle uppercase
        return text

    def convert_transliteration(self,
                                text, source, target,
                                intermediate_scheme="Lachler",
                                inner_call=False,
                                unknown_text="???"):
        """
        Convert text from one transliteration scheme to another.
        """
        if source == target:
            return text
        
        # Get the appropriate mapping function
        mapping = self.mappings.get((source, target))

        if mapping:
            return mapping(text)
        
        # If direct mapping doesn't exist, go through an intermediate scheme
        if inner_call:
            return unknown_text
        elif source != intermediate_scheme:
            intermediate = self.convert_transliteration(text, source, intermediate_scheme, inner_call=True)
            return self.convert_transliteration(intermediate, intermediate_scheme, target, inner_call=True)
        elif target != intermediate_scheme:
            intermediate = self.convert_transliteration(text, source, intermediate_scheme, inner_call=True)
            return self.convert_transliteration(intermediate, intermediate_scheme, target, inner_call=True)
        else:
            return unknown_text