import re
# import unicodedata

class Converter:
    
    SCHEMES = ["Lachler", "Texting", "Leer", "Enrico", "Swanton", "Lachler-CopyPaste", "IPA"]
    UNDERLINE = "g̱"[-1]

    def __init__(self):
        self.mappings = {
            ("Lachler", "Texting"): self._lachler_to_texting,
            ("Texting", "Lachler"): self._texting_to_lachler,
            ("Lachler", "Leer"): self._lachler_to_leer,
            ("Leer", "Lachler"): self._leer_to_lachler,
            ("Lachler", "Lachler-CopyPaste"): self._lachler_to_cp,
            ("Lachler-CopyPaste", "Lachler"): self._cp_to_lachler,
            ("Lachler", "IPA"): self._lachler_to_ipa,
            ("Lachler", "Enrico"): self._lachler_to_enrico,
        }

    def _normalize(self, text):
        # TODO: Normalization to avoid e.g. combining diacritic vs. single char
        # return unicodedata.normalize('NFD', text)
        return text
    
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
    
    def _lachler_to_leer(self, text):
        voiced = "b d g gw dl j".split()
        unvoiced = "p t k kw tl ts".split()
        exception_chars = "aiuáíúwy" + self.UNDERLINE
        for v, u in zip(voiced, unvoiced):
            if v == "g":
                # handle separately to avoid devoicing ng (e.g. gudáng)
                text = re.sub(rf"([^n]){v}([^{exception_chars}])", rf"\g<1>{u}\g<2>", text)
                text = re.sub(rf"([^n]){v}$", rf"\g<1>{u}", text)
            else:
                if v == "d":
                    exception_chars += "l" # e.g. g̱ándlaay; don't devoice d
                text = re.sub(rf"{v}([^{exception_chars}])", rf"{u}\g<1>", text)
                text = re.sub(rf"{v}$", u, text)
        return text
    
    def _leer_to_lachler(self, text):
        voiced = "j b d g gw dl".split()
        unvoiced = "ts p t k kw tl".split()
        # ^ NOTE: j/ts first to avoid conflict with d/t
        exception_chars = "aiuáíúwy" + self.UNDERLINE
        for v, u in zip(voiced, unvoiced):
            text = re.sub(rf"([^n]){u}([^{exception_chars}])", rf"\g<1>{v}\g<2>", text)
            text = re.sub(rf"([^n]){u}$", rf"\g<1>{v}", text)
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
    
    def _lachler_to_ipa(self, text):
        text = text.lower()

        equivs = "aa ii uu ee oo áa íi úu ée óo x̱ g̱ x̂ hl ng".split()
        equivs_ = "aː iː uː eː oː áː íː úː éː óː ʜ ʡ χ ɬ ŋ".split()
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)

        asp = "p tl ch t ḵ k".split() # k-underline must come before k
        asp_ipa = "pʰ tɬʰ tʃʰ tʰ qʰ kʰ".split()
        for x, y in zip(asp, asp_ipa):
            text = text.replace(x, y)
            text = text.replace(y + "'", y[:-1] + "'") # fix ejectives
        # fix extra aspir.
        to_fix = "tʰʃʰ tʰɬʰ tʰs' tʰɬ'".split()
        fixed = "tʃʰ tɬʰ ts' tɬ'".split()
        for x, y in zip(to_fix, fixed):
            text = text.replace(x, y)
        
        unasp = "b dl j d ĝ g".split()
        unasp_ipa = "b̥ d̥ɮ̊ d̥ʒ̊ d̥ ɢ̥ ɡ̊".split()
        for x, y in zip(unasp, unasp_ipa):
            text = text.replace(x, y)

        equivs = "y 'w 'j 'l".split()
        equivs_ = "j wˀ jˀ lˀ".split()
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)

        # glottal stop        
        text = re.sub(r"([aeiouáéíóú]ː)'([aeiouáéíóú])", r"\g<1>ʔ\g<2>", text)
        text = re.sub(r"^([aeiouáéíóú])", r"ʔ\g<1>", text)
        text = re.sub(r" ([aeiouáéíóú])", r" ʔ\g<1>", text)

        # ejective symbol
        text = text.replace("'", "ʼ")

        # remove separator between /n/ and /g/
        text = text.replace("-", "")

        return text

    def _lachler_to_enrico(self, text):
        text = text.lower()
        equivs = "ḵ g̱ x c̱ ĝ x̂ ".split()
        equivs_ = "q r c x G X".split()
        # ^ note: c̱ because x became c
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)
        
        # glottal stop
        text = re.sub(r"([aeiouáéíóú])'([aeiouáéíóúwyl])", r"\g<1>7\g<2>", text)
        text = re.sub(r"^([aeiouáéíóúwyl])", r"7\g<1>", text)
        text = re.sub(r" ([aeiouáéíóúwyl])", r" 7\g<1>", text)

        equivs = "á é í ó ú ".split()
        equivs_ = "a e i o u".split()
        for x, y in zip(equivs, equivs_):
            text = text.replace(x, y)
        # TODO: syllable boundaries, doubling to make tone predictable

        return text

    def convert_transliteration(self,
                                text, source, target,
                                intermediate_scheme="Lachler",
                                inner_call=False,
                                unknown_text="???"):
        """
        Convert text from one transliteration scheme to another.
        """

        # Normalization to avoid e.g. combining diacritic vs. single char
        text = self._normalize(text)

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