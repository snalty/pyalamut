from datetime import datetime
from enum import Enum
from lxml import html

class VariantType(Enum):
    """Enum for variant type, not yet used"""
    SUBSTITION = "subsitution"
    MISSENSE = "missense"
    DUPLICATION = "duplication"

class Nomenclature():
    """Classs to hold nomenclature information for a variant

    Attributes
    ----------
    gnomen : string
        Genominc nomenclature of the variant
    cnomen : string
        Coding DNA nomenclature
    rnomen : string
        transcript nomenclature of the variant
    pnomen : string
        protein nomenclature of the variant
    refseq : string
        refseq transcript identifier
    """
    def __init__(self, gnomen, cnomen, rnomen, pnomen, refseq):
        self.gnomen = gnomen
        self.cnomen = cnomen
        self.rnomen = rnomen
        self.pnomen = pnomen
        self.refseq = refseq

class Variant():
    """Base class for all variant classes
    
    Attributes
    ----------
    type : str
        A string containing the type of the variant
    nomenclature : Nomenclature
        A nomenclature class holding the variant nomenclature
    """    

    def __init__(self, type, nomenclature):
        self.type = type
        self.nomenclature = nomenclature

    def __repr__(self):
        rep = f"{self.__class__.__name__}, ({self.nomenclature.refseq}, {self.nomenclature.cnomen})"
        return rep

class DeletionVariant(Variant):
    """
    Class representing a Deletion Variant

    Attributes
    ----------
    type : str
        A string containing the type of the variant
    nomenclature : Nomenclature
        A nomenclature class holding the variant nomenclature
    from_ : int
        base which the deletion starts at
    to : int
        base which the deletion ends at
    """
    def __init__(self, type, nomenclature, from_, to):
        super(DeletionVariant, self).__init__(type, nomenclature)
        self.from_ = from_
        self.to = to

class SubstitutionVariant(Variant):
    """
    Class representing a Substitution Variant

    Attributes
    ----------
    type : str
        A string containing the type of the variant
    nomenclature : Nomenclature
        A nomenclature class holding the variant nomenclature
    pos : int:
        Position of the substitution
    base_from : str
        Original base
    base_to : str
        Alternative base
    """
    def __init__(self, type, nomenclature, pos, base_from, base_to):
        super(SubstitutionVariant, self).__init__(type, nomenclature)
        self.pos = pos
        self.base_from = base_from
        self.base_to = base_to

    def __str__(self):
        return self.__repr__()

class DuplicationVariant(Variant):
    """
    Class representing a Duplication Variant

    Attributes
    ----------
    type : str
        A string containing the type of the variant
    nomenclature : Nomenclature
        A nomenclature class holding the variant nomenclature
    from_ : int
        base which the duplication starts at
    to : int
        base which the duplication ends at
    """
    def __init__(self, type, nomenclature, from_, to):
        super(DuplicationVariant, self).__init__(type, nomenclature)
        self.from_ = from_
        self.to = to

class DelinsVariant(Variant):
    """
    Class representing a Delins (indel) Variant

    Attributes
    ----------
    type : str
        A string containing the type of the variant
    nomenclature : Nomenclature
        A nomenclature class holding the variant nomenclature
    from_ : int
        base which the deletion starts at
    to : int
        base which the deletion ends at
    inserted : str
        sequence of the inserted bases
    """
    def __init__(self, type, nomenclature, from_, to, inserted):
        super(DelinsVariant, self).__init__(type, nomenclature)
        self.from_ = from_
        self.to = to
        self.inserted = inserted

class InsertionVariant(Variant):
    """
    Class representing an Insertion Variant

    Attributes
    ----------
    type : str
        A string containing the type of the variant
    nomenclature : Nomenclature
        A nomenclature class holding the variant nomenclature
    from_ : int
        coord which the insertion starts at
    to : int
        coord which the insertion ends at
    inserted : str
        sequence of the inserted bases
    """
    def __init__(self, type, nomenclature, from_, to, inserted):
        super(InsertionVariant, self).__init__(type, nomenclature)
        self.from_ = from_
        self.to = to
        self.inserted = inserted

