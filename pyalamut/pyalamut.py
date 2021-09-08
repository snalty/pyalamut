from lxml import etree, html
from typing import IO
from os import PathLike
from .variants import DeletionVariant, DelinsVariant, DuplicationVariant, \
    InsertionVariant, SubstitutionVariant, Nomenclature
from datetime import datetime

class Mutations():
    """Simple class to hold mutations"""
    def __init__(self, mutations):
        self.mutations = mutations

class Occurence():
    def __init__(self, created_date_string, created_time_string,
    updated_date_string, updated_time_string, patient, family, rna_analysis,
    phenotype, comment):
        self.created_datetime = self._parse_datetime(created_date_string,
        created_time_string)
        self.updated_datetie = self._parse_datetime(updated_date_string,
        updated_time_string)
        self.patient = patient
        self.family = family
        self.rna_analyis = self._strip_html(rna_analysis)
        self.phenotype = self._strip_html(phenotype)
        self.comment = self._strip_html(comment)
        
    def _parse_datetime(self, date_string, time_string):
        date = datetime.strptime(date_string, "%Y-%m-%d").date()
        time = datetime.strptime(time_string, "%H:%M:%S").time()
        return datetime.combine(date, time)

    def _strip_html(self, html_string):
        parsed_html = html.fromstring(html_string)
        body = parsed_html.find('body')

        # Return none if text is empty
        if body.text_content() == "\n":
            return None
        
        return body.text_content()

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.patient})"

class Mutation():
    """
    Class representing an Alamaut Mutation

    Attributes
    ----------
    id : str
        Alamut variant id
    self.version : str
        Version number
    organism : str
        Variant organism
    reference_assembly : str
        Reference assembly of the variant
    chromosome : str
        Chromosome of the variant
    gene_symbol : str
        Gene symbol of the variant
    classification : str
        Classification of the variant
    pathogenic : bool
        Whether the variant was classified as pathogenic
    note : str
        Note on the variant
    """
    def __init__(self, id, version, organism, reference_assembly, chromosome,
    gene_symbol, classification, pathogenic, note):
        self.id = id
        self.version = version
        self.organism = organism
        self.reference_assembly = reference_assembly
        self.chromosome = chromosome
        self.gene_symbol = gene_symbol
        self.classification = classification
        self.pathogenic = {'yes': True, 'no': False, 'unknown': None}[pathogenic]
        self.note = note
        self.variant = None
        self.occurences = None

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.organism}, {self.reference_assembly}, {self.gene_symbol}), {self.variant.__repr__()}"

class MutationsParser():
    def _parse_mutation(self, mutation):
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
            occurence.find('Family').text,
            occurence.find('RNAAnalysis').text,
            occurence.find('Phenotype').text,
            occurence.find('Comment').text
        )

    def _parse_variant(self, variant):

        v_dict = variant.attrib
        if v_dict['type'] == "Substitution":
            return SubstitutionVariant(
                v_dict['type'],
                self._parse_nomenclature(variant),
                int(v_dict['pos']),
                v_dict['baseFrom'],
                v_dict['baseTo']
            )

        elif v_dict['type'] == "Deletion":
            return DeletionVariant(
                v_dict['type'],
                self._parse_nomenclature(variant),
                int(v_dict['from']),
                int(v_dict['to'])
            )

        elif v_dict['type'] == "Duplication":
            return DuplicationVariant(
                v_dict['type'],
                self._parse_nomenclature(variant),
                int(v_dict['from']),
                int(v_dict['to'])
            )

        elif v_dict['type'] == "Delins":
            return DelinsVariant(
                v_dict['type'],
                self._parse_nomenclature(variant),
                int(v_dict['from']),
                int(v_dict['to']),
                v_dict['inserted']
            )

        elif v_dict['type'] == "Insertion":
            return InsertionVariant(
                v_dict['type'],
                self._parse_nomenclature(variant),
                int(v_dict['from']),
                int(v_dict['to']),
                v_dict['inserted']
            )

        else:
            raise ValueError(f"Don't know how to parse variant type {v_dict['type']}")

    def _parse_nomenclature(self, variant_tree) -> Nomenclature:
        """[summary]

        Args:
            variant_tree (etree): An xml element tree containing the variant

        Returns:
            Nomenclature: Parsed nomenclature for the variant
        """        
        gnomen = variant_tree.find('gNomen').attrib['val']
        nomenclature = variant_tree.find('Nomenclature')
        refseq = nomenclature.attrib['refSeq']
        cnomen = nomenclature.find('cNomen').attrib['val']
        rnomen = nomenclature.find('rNomen').attrib['val']
        pnomen = nomenclature.find('pNomen').attrib['val']

        return Nomenclature(gnomen, cnomen, rnomen, pnomen, refseq)

    def parse_mut_file(self, mut_file: IO) -> Mutations:
        """
        Parse a mut file from an IO object

        Args:
            mut_file (IO): A file like object of an Alamut mut file

        Returns:
            Mutations: A class containing a list of parsed mutations
        """
        xml_tree = etree.parse(mut_file)
        mutations_xml = xml_tree.getroot()
        
        # Parse mutations
        mutations = [self._parse_mutation(mutation) for mutation in mutations_xml.getchildren()]

        return Mutations(mutations)


    def parse_mut_file_from_path(self, path: PathLike):
        with open(path, 'r') as f:
            self.parse_mut_file(f)