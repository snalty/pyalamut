from lxml import etree
from typing import IO
from os import PathLike
from enum import Enum
from datetime import datetime, date, time

class VariantType(Enum):
    SUBSTITION = "subsitution"
    MISSENSE = "missense"

class Mutations():
    def __init__(self, mutations):
        self.mutations = mutations

class Nomenclature():
    def __init__(self, gnomen, cnomen, rnomen, pnomen, refseq):
        self.gnomen = gnomen
        self.cnomen = cnomen
        self.rnomen = rnomen
        self.pnomen = pnomen
        self.refseq = refseq

class MutationsParser():
    def _parse_mutation(self, mutation):
        print("test")
        mutation_dict = mutation.attrib
        mutation_class = Mutation(
            mutation_dict['id'],
            mutation_dict['version'],
            mutation_dict['organism'],
            mutation_dict['refAssembly'],
            mutation_dict['chr'],
            mutation_dict['geneSym'],
            mutation.find('Classification').attrib['val'],
            mutation.find('Pathogenic').attrib['val'], 
            mutation.find('Note').attrib['val']
        )

        mutation_class.variant = self._parse_variant(mutation.find('Variant'))
        occurences = mutation.find('Occurrences').getchildren()
        mutation_class.occurences = [self._parse_occurence(occurence) for occurence in occurences]

        return mutation_class

    def _parse_occurence(self, occurence):
        created = occurence.find('Created').attrib
        updated = occurence.find('Updated').attrib


        return Occurence(
            created['date'],
            created['time'],
            updated['date'],
            updated['time'],
            occurence.find('Patient').text,
            occurence.find('Family').text
        )


    def _parse_variant(self, variant):
        v_dict = variant.attrib
        if v_dict['type'] == "Substitution":
            return SubstitutionVariant(
                v_dict['type'],
                self._parse_nomenclature(variant),
                v_dict['pos'],
                v_dict['baseFrom'],
                v_dict['baseTo']
            )

        elif v_dict['type'] == "Deletion":
            return DeletionVariant(
                v_dict['type'],
                self._parse_nomenclature(variant),
                v_dict['from'],
                v_dict['to']
            )

    def _parse_nomenclature(self, variant):
        gnomen = variant.find('gNomen').attrib['val']
        nomenclature = variant.find('Nomenclature')
        refseq = nomenclature.attrib['refSeq']
        cnomen = nomenclature.find('cNomen').attrib['val']
        rnomen = nomenclature.find('rNomen').attrib['val']
        pnomen = nomenclature.find('pNomen').attrib['val']

        return Nomenclature(gnomen, cnomen, rnomen, pnomen, refseq)


    def parse_mut_file(self, mut_file: IO):
        xml_tree = etree.parse(mut_file)
        mutations_xml = xml_tree.getroot()
        
        # Parse mutations
        mutations = [self._parse_mutation(mutation) for mutation in mutations_xml.getchildren()]

        return Mutations(mutations)


    def parse_mut_file_from_path(self, path: PathLike):
        with open(path, 'r') as f:
            self.parse_mut_file(f.read())

class Mutation():
    def __init__(self, id, version, organism, reference_assembly, chromosome,
    gene_symbol, classification, pathogenic, note):
        self.id = id
        self.version = version
        self.organism = organism
        self.reference_assembly = reference_assembly
        self.chromosome = chromosome
        self.gene_symbol = gene_symbol
        self.classification = classification
        self.pathogenic = pathogenic
        self.note = note
        self.variant = None
        self.occurences = None

class Variant():
    def __init__(self, type, nomenclature):
        self.type = type
        self.nomenclature = nomenclature

class DeletionVariant(Variant):
    def __init__(self, type, nomenclature, from_, to):
        super(DeletionVariant, self).__init__(type, nomenclature)
        self.from_ = from_
        self.to = to

class SubstitutionVariant(Variant):
    def __init__(self, type, nomenclature, pos, base_from, base_to):
        super(SubstitutionVariant, self).__init__(type, nomenclature)
        self.pos = pos
        self.base_from = base_from
        self.base_to = base_to

class Occurence():
    def __init__(self, created_date_string, created_time_string,
    updated_date_string, updated_time_string, patient, family):
        self.created_datetime = self._parse_datetime(created_date_string,
        created_time_string)
        self.updated_datetie = self._parse_datetime(updated_date_string,
        updated_time_string)
        self.patient = patient
        self.family = family
        
    def _parse_datetime(self, date_string, time_string):
        date = datetime.strptime(date_string, "%Y-%m-%d").date()
        time = datetime.strptime(time_string, "%H:%M:%S").time()
        return datetime.combine(date, time)