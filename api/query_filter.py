import re
from typing import Set, List


class QueryFilter:
    def __init__(self):
        # Запрещенные термины сгруппированы по категориям
        self.blocked_terms = {
            # Жестокость и насилие
            "violence": self._get_violence_terms(),
            # Графическая/экстремальная жестокость
            "graphic_violence": self._get_graphic_violence_terms(),
            # Эротика и сексуальный контент
            "erotica": self._get_erotica_terms(),
            # ЛГБТ контент
            "lgbt": self._get_lgbt_terms(),
        }

        # Компилируем паттерны для эффективной проверки
        self.compiled_patterns = self._compile_patterns()

    def _get_violence_terms(self) -> Set[str]:
        """Термины насилия - базовая жестокость"""
        return {
            "violence", "violent", "violently", "non-violent",
            "brutal", "brutality", "brutally",
            "gore", "gory", "gorier", "goriest",
            "blood", "bloody", "bloodshed", "bleed", "bleeding",
            "murder", "murderer", "murderous", "murdering", "murdered",
            "kill", "killing", "killer", "killed", "kills", "killable",
            "death", "deadly", "dying", "deathly", "fatal", "fatality",
            "massacre", "massacred", "slaughter", "slaughtering", "slaughtered",
            "torture", "torturing", "tortured", "torturer", "torturous",
            "assault", "assaulting", "assaulted", "assaulter",
            "genocide", "genocidal",
            "war", "warfare", "warring", "wars",
            "fight", "fighting", "fighter", "fights", "fought",
            "combat", "combating", "combated", "combative",
            "weapon", "weapons", "weaponry",
            "gun", "guns", "gunning", "gunned", "gunfight",
            "shoot", "shooting", "shooter", "shoots", "shot",
            "sword", "swords", "swordfight",
            "stab", "stabbing", "stabbed", "stabber",
            "grenade", "grenades", "bomb", "bombing", "bombed", "bombs",
            "explode", "explosion", "explosive", "exploded", "exploding",
            "hit", "hitting", "hits", "hitter",
            "strike", "striking", "struck", "striker", "strikes",
            "punch", "punching", "punched", "puncher",
            "kick", "kicking", "kicked", "kicker",
            "beat", "beating", "beaten", "beater", "beats",
            "abuse", "abusing", "abused", "abuser", "abusive",
            "harm", "harming", "harmed", "harmful", "harms",
            "injure", "injuring", "injury", "injured", "injures",
            "maim", "maiming", "maimed", "maimer",
            "savage", "savagery", "savagely",
            "carnage", "butcher", "butchery", "butchering", "butchered",
            "dismember", "dismembering", "dismembered", "dismemberment",
            "decapitate", "decapitating", "decapitated", "decapitation", "behead", "beheading", "beheaded",
            "mutilate", "mutilating", "mutilated", "mutilation", "mutilator",
            "disembowel", "disemboweling", "disemboweled", "disembowelment",
            "guts", "entrails", "intestines", "viscera",
            "splatter", "splattering", "splattered", "splattery",
            "cruel", "cruelty", "cruelly",
            "sadistic", "sadist", "sadism", "sadistically",
            "vicious", "viciously", "viciousness",
            "ferocious", "ferociously", "ferocity",
            "ruthless", "ruthlessly", "ruthlessness",
            "merciless", "mercilessly", "mercilessness",
            "bloodbath", "bloodbaths",
            "culling", "cull",
            "execute", "executed", "execution", "executing",
            "crucify", "crucifying", "crucified", "crucifixion",
            "hang", "hanging", "hanged", "hanger",
            "strangle", "strangling", "strangled", "strangler",
            "suffocate", "suffocating", "suffocated", "suffocation",
            "drown", "drowning", "drowned",
            "burn", "burning", "burned", "burnt", "arson",
            "poison", "poisoning", "poisoned",
            "electrocute", "electrocuted", "electrocution",
            "wound", "wounding", "wounded", "wounds",
            "maul", "mauling", "mauled",
            "rip", "ripping", "ripped", "ripper",
            "tear", "tearing", "torn", "tears",
            "break", "breaking", "broken", "breaks",
        }

    def _get_graphic_violence_terms(self) -> Set[str]:
        """Термины графической/экстремальной жестокости"""
        return {
            "graphic violence", "extreme violence", "explicit violence", "brutal violence",
            "graphic gore", "extreme gore", "explicit gore", "brutal gore",
            "graphic blood", "extreme blood", "explicit blood", "brutal blood",
            "realistic violence", "intense violence", "ultra violent", "hyper violent",
            "hyperviolence", "graphic content", "graphic depiction",
            "splatterpunk", "torture porn", "gorn", "grindhouse",
            "body horror", "cosmic horror", "grotesque",
            "dismemberment", "decapitation", "mutilation",
            "evisceration", "eviscerating", "eviscerated",
            "cannibal", "cannibalism", "cannibalistic",
            "necrophilia", "necrophiliac",
            "snuff", "snuff film",
            "shock value",
        }

    def _get_erotica_terms(self) -> Set[str]:
        """Термины эротики и сексуального контента"""
        base_terms = {
            # Прямые термины
            "porn", "porno", "pornography", "pornographic",
            "erotic", "erotica", "erotical", "erotism",
            "sex", "sexual", "sexuality", "sexy", "sexed", "sexing",
            "nude", "nudity", "nudes", "naked", "nudie",
            "explicit", "explicitly", "xxx", "xx",
            "hentai", "ecchi", "harem",
            "boobs", "tits", "breasts", "breast", "titties", "tittie",
            "ass", "butt", "booty", "arse", "buttocks", "glutes",
            "dick", "cock", "penis", "phallus", "dong", "schlong", "wiener",
            "pussy", "vagina", "cunt", "vulva", "clit", "clitoris",
            "fuck", "fucking", "fucked", "fucks", "fucker", "fuckery",
            "masturbate", "masturbating", "masturbation", "masturbated", "masturbator", "masturbatory",
            "orgasm", "orgasmic", "orgasms", "orgasmically",
            "seduce", "seducing", "seduced", "seduction", "seductive", "seductively",
            "strip", "stripping", "stripper", "stripped", "striptease",
            "lingerie", "underwear", "panties", "thong", "g-string",
            "fetish", "fetishes", "fetishism", "fetishistic",
            "bdsm", "bondage", "domination", "dominant", "submission", "submissive",
            "kink", "kinky", "kinkiness",
            "threesome", "foursome", "orgy", "orgies", "gangbang",
            "prostitute", "prostitution", "prostituting", "prostituted", "hooker", "whore",
            "escort", "escorting", "escorted", "escorts",
            "brothel", "bordello", "red light",
            "pimp", "pimping", "pimped",
            "incest", "incestuous", "incestuously",
            "rape", "raping", "raped", "rapist", "rapists",
            "molest", "molesting", "molestation", "molested", "molester",
            "harass", "harassing", "harassment", "harassed",
            "pervert", "perverted", "perversion", "pervertedly", "pervs",
            "voyeur", "voyeurism", "voyeuristic",
            "exhibitionist", "exhibitionism", "exhibitionistic",
            "foreplay", "foreplaying",
            "intercourse", "coitus", "copulate", "copulating", "copulation",
            "fornicate", "fornicating", "fornication", "fornicator",
            "lewd", "lewdness", "lewdly",
            "lascivious", "lasciviously", "lasciviousness",
            "libidinous", "libidinously",
            "prurient", "prurience",
            "salacious", "salaciously", "salaciousness",
            "sensual", "sensuality", "sensually",
            "risque",
            "titillating", "titillate", "titillation",
            "provocative", "provocatively",
            "suggestive", "suggestively",
            "intimate", "intimacy", "intimately",
            "arousing", "arousal", "arouse", "aroused",
            "lust", "lustful", "lusting", "lustfully", "lustiness",
            "desire", "desirous", "desired", "desiring",
            "passion", "passionate", "passionately", "passioned",
            "pleasure", "pleasuring", "pleasured", "pleasurable",
            "fantasy", "fantasize", "fantasizing",
            "kissing", "kisses", "kissed", "kiss", "make out", "making out", "made out",
            "spicy", "spiciest", "spicier",
            "naughty", "naughtier", "naughtiest",
            "dirty", "dirtier", "dirtiest",
            "filthy", "filthier", "filthiest", "filth",
            "smut", "smutty", "smuttier", "smuttiest",
            "raunchy", "raunchier", "raunchiest",
            "obscene", "obscenity", "obscenely",
            "indecent", "indecency", "indecently",
            "hardcore", "softcore",
            "uncensored", "unrated", "uncut",
            "after hours", "late night",
        }

        # Эвфемизмы и кодовые слова
        euphemisms = {
            "adult only", "adult-only", "adults only", "adults-only",
            "18+", "18 plus", "eighteen plus", "18-and-over", "age restricted",
            "mature content", "mature themes", "mature rating", "mature audiences",
            "not safe for work", "nsfw", "nsfw content", "not suitable for work",
            "private shows", "private show", "private viewing", "private entertainment",
            "special massage", "special massages", "special treatment", "special services",
            "companionship", "companionship services",
            "adult fun", "adult entertainment", "adult themes", "adult oriented",
            "exotic", "exotic entertainment", "exotic dancers", "exotic dancing",
            "forbidden", "forbidden content", "forbidden themes",
            "taboo", "taboo content", "taboo themes", "taboo subjects",
            "love scene", "love scenes", "love making", "love-making",
            "romance scene", "romance scenes", "romantic encounter",
            "bedroom activities", "bedroom scene", "bedroom scenes",
            "intimate scene", "intimate scenes", "intimate moments",
            "personal entertainment", "personal time", "personal enjoyment",
            "self care", "self-care", "self pleasure",
            "alternative content", "special content", "bonus content", "extra content",
            "hidden content", "secret content", "unlockable content", "dlc exclusive",
            "uncut version", "unrated version", "directors cut", "director's cut",
            "extended cut", "special edition", "limited edition", "collector's edition",
            "behind the scenes", "behind-the-scenes",
            "red light", "red-light", "red light district", "amsterdam",
            "victoria's secret", "playboy", "playgirl", "penthouse", "hustler",
        }

        return base_terms.union(euphemisms)

    def _get_lgbt_terms(self) -> Set[str]:
        """Термины ЛГБТ контента"""
        base_terms = {
            # Основные идентичности
            "lgbt", "lgbtq", "lgbtq+", "lgbtqia", "lgbtqia+", "lgbtq2s", "lgbtqqiaap",
            "gay", "gays", "gayness", "homosexual", "homosexuals", "homosexuality",
            "lesbian", "lesbians", "lesbianism", "sapphic",
            "bisexual", "bisexuals", "bisexuality", "bi", "bi-sexual",
            "transgender", "transgenders", "transgenderism", "trans", "trans-sexual", "transsexual",
            "queer", "queers", "queerness",
            "non-binary", "nonbinary", "non binary", "genderqueer", "gender queer", "gender non-conforming",
            "genderfluid", "gender fluid", "gender-fluid", "genderfluidity",
            "pansexual", "pansexuals", "pansexuality", "pan",
            "asexual", "asexuals", "asexuality", "ace", "aro", "aromantic",
            "intersex", "intersexual", "intersexuality",
            "drag queen", "drag queens", "drag king", "drag kings", "drag show", "drag performances",
            "crossdresser", "crossdressers", "crossdressing", "cross-dresser", "cross-dressers", "cross-dressing",
            "transvestite", "transvestites", "transvestism",
            "coming out", "out of the closet", "closeted",
            "gay marriage", "same-sex marriage", "same sex marriage", "same-sex union", "same sex union",
            "gay pride", "lgbt pride", "trans pride", "pride month", "pride parade", "pride flag", "rainbow flag",
            "lgbt community", "gay community", "trans community", "queer community", "lgbtq community",
            "lgbt rights", "gay rights", "trans rights", "queer rights", "lgbtq rights",
            "pronouns", "preferred pronouns", "gender pronouns", "they/them", "she/her", "he/him",
            "gender identity", "sexual orientation", "gender expression",
            "boys love", "boyslove", "bl",
            "girls love", "girlslove", "gl",
            "yaoi", "yuri", "shounen ai", "shonen ai", "shoujo ai", "shojo ai",
            "bara", "femslash", "slash fiction", "slashfic",
            "lgbt protagonist", "gay protagonist", "lesbian protagonist", "trans protagonist", "queer protagonist",
            "lgbt main character", "gay main character", "lesbian main character", "trans main character",
            "queer main character",
            "lgbt hero", "gay hero", "lesbian hero", "trans hero", "queer hero",
            "lgbt character", "gay character", "lesbian character", "trans character", "queer character",
            "lgbt romance", "gay romance", "lesbian romance", "trans romance", "queer romance", "same-sex romance",
            "same sex romance",
            "lgbt relationship", "gay relationship", "lesbian relationship", "trans relationship", "queer relationship",
            "lgbt love", "gay love", "lesbian love", "trans love", "queer love",
            "lgbt storyline", "gay storyline", "lesbian storyline", "trans storyline", "queer storyline",
            "lgbt themes", "gay themes", "lesbian themes", "trans themes", "queer themes",
            "lgbt representation", "gay representation", "lesbian representation", "trans representation",
            "queer representation",
            "lgbt inclusive", "lgbt-inclusive", "lgbt friendly", "lgbt-friendly",
        }

        # Эвфемизмы и описательные фразы
        euphemisms = {
            # Диверситетные коды
            "diverse romance", "diverse love", "diverse relationships",
            "diverse characters", "diverse character", "diverse protagonist", "diverse hero",
            "character diversity", "relationship diversity", "story diversity",
            "inclusive romance", "inclusive love", "inclusive relationships", "inclusive characters",
            "inclusive storyline", "inclusive themes", "inclusive representation",
            "alternative romance", "alternative love", "alternative relationships", "alternative lifestyle",
            "alternative lifestyles",
            "modern romance", "contemporary romance", "modern love", "contemporary love",
            "modern relationships", "contemporary relationships",
            "progressive romance", "progressive love", "progressive relationships", "progressive themes",
            "non-traditional romance", "non traditional romance", "nontraditional romance",
            "non-traditional love", "non traditional love", "nontraditional love",
            "non-traditional relationships", "non traditional relationships", "nontraditional relationships",
            "different love story", "different romance", "different relationships",
            "unique romance", "unique love story", "unique relationships",
            "special romance", "special love story", "special relationships",
            "love is love", "love wins", "proud", "pride themes", "rainbow themes", "colorful themes",
            "representation matters", "diverse representation", "authentic representation",
            "identity themes", "gender themes", "sexuality themes",
            "social themes", "contemporary issues", "modern issues",
            "acceptance themes", "tolerance themes", "understanding themes", "equality themes",
            "coming of age story", "finding yourself", "self discovery", "self-discovery",
            "breaking barriers", "challenging norms", "defying conventions",
            "forbidden love", "taboo love", "forbidden romance", "taboo romance",
        }

        return base_terms.union(euphemisms)

    def _compile_patterns(self) -> List[re.Pattern]:
        """Компилирует паттерны для эффективного поиска"""
        all_terms = set()
        for category_terms in self.blocked_terms.values():
            all_terms.update(category_terms)

        # Сортируем по длине (длинные фразы первыми)
        sorted_terms = sorted(all_terms, key=len, reverse=True)

        patterns = []
        for term in sorted_terms:
            # Экранируем спецсимволы
            escaped_term = re.escape(term)

            # Для фраз: проверяем целое совпадение
            if " " in term:
                pattern = r'(?<!\w)' + escaped_term + r'(?!\w)'
            else:
                # Для слов: строгие границы слов
                pattern = r'\b' + escaped_term + r'\b'

            try:
                compiled = re.compile(pattern, re.IGNORECASE)
                patterns.append(compiled)
            except re.error:
                continue

        return patterns

    def validate(self, query: str) -> tuple[bool, List[str]]:
        """Валидация запроса"""
        if not query or not isinstance(query, str) or not query.strip():
            return False, ["empty_query"]

        violations = set()
        query_lower = query.lower()

        # Проверяем каждый паттерн
        for pattern in self.compiled_patterns:
            matches = pattern.findall(query)
            if matches:
                violations.update(match.lower() for match in matches)

        return len(violations) == 0, list(violations)


# Глобальный экземпляр
query_filter = QueryFilter()