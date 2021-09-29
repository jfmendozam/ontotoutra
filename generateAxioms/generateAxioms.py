#!/usr/bin/env python
"""Provides GenerateRDF class for ontology files.

GenerateRDF builds axioms for ontology files in OWL/RDF format,
compatible with Protégé and other ontology tools.
Study Case: OntoTouTra Ontology (http://tourdata.org)
"""

import os
import pandas as pd

__author__     = ["JF Mendoza", "Luz Santamaría"]
__copyright__  = "Copyright 2021, Universidad del Cauca"
__credits__    = ["Gustavo Ramírez", "Anabel Fraga"]
__license__    = "GPL"
__version__    = "1.0.1"
__maintainer__ = "JF Mendoza"
__email__      = "fmendoza@unicauca.edu.co"
__status__     = "Development"


class GenerateRDF:
    """ This class create axioms in format OWL/RDF.

    Parameters: 
    output_filename.
    
    Returns:
    None (output_filename).
    """

    def __init__(self, path, filename, encoding, owl_path, owl_filename, ott_prefix):
        self.path         = path
        self.filename     = filename
        self.encoding     = encoding
        self.owl_path     = owl_path
        self.owl_filename = owl_filename
        self.ott_prefix   = ott_prefix

#%%
    def csv2DF(self, filename, sep, encoding):
        """ Convert CSV file to dataframe.
    
        Parameters: 
           filename: Input CSV file.
           sep     : Separator character.
           encoding: Encoding system.

        Returns:
           Dataframe.
        """

        return pd.read_csv(filename, sep=sep, encoding=encoding)

#%%
    def getCountries(self):
        """ Get countries from ontology

            Parameters:
            None

            Return:
            Countries dataframe
        """

        owl_list = self.readTextFile(
            os.path.join(self.owl_path, self.owl_filename)
        )

        countries = []
        for i in range(len(owl_list)):
            if (
                owl_list[i].find('#Country"') != -1 and 
                owl_list[i - 1].find('owl:NamedIndividual') != -1
            ):
                start      = owl_list[i - 1].find('#') + 1
                end        = owl_list[i - 1].find('"', start)
                individual = owl_list[i - 1][start : end]

                i += 1
                while (owl_list[i].find('owl:NamedIndividual') == -1):
                    start = owl_list[i].find('>') + 1
                    end   = owl_list[i].find('<', start)
                    field = owl_list[i][start : end]

                    if (owl_list[i].find('alpha2Code') != -1):
                        alpha2 = field
                    elif (owl_list[i].find('alpha3Code') != -1):
                        alpha3 = field
                    elif (owl_list[i].find('countryID') != -1):
                        id = int(field)
                    elif (owl_list[i].find('countryName') != -1):
                        name = field

                    i += 1
                countries.append([id, individual, name, alpha2, alpha3])
        return pd.DataFrame(data=countries, columns=['id', 'individual', 'name', 'alpha2', 'alpha3'])


#%%
    def generateHotelReviews(self, output_filename):
        """ Generate hotel reviews.
    
        Parameters: 
        output_filename.
        
        Returns:
        None (output_filename).
        """

        df = pd.read_csv(
            os.path.join(self.path, self.filename),
            sep=';',
            encoding=self.encoding
        )
        countries_df = self.getCountries()

        with open(output_filename, 'w') as of:
            for index, row in df.iterrows():
                of.write('\n' * 3)
                
                # Comment
                of.write(
                    '    <!-- ' + self.ott_prefix + 'hotel_review_' + 
                    str(int(row.reviewID)) + ' -->\n\n'
                )

                # Open NamedIndividual
                of.write(
                    '    <owl:NamedIndividual rdf:about="' + 
                    self.ott_prefix + 'hotel_review_' + 
                    str(int(row.reviewID)) + '">\n'
                )

                # Class
                of.write(
                    '        <rdf:type rdf:resource="' + self.ott_prefix +
                    'HotelReview"/>\n'
                )

                # hasAccommodationType axiom
                of.write(
                    '        <hasAccommodationType rdf:resource="' + 
                    self.ott_prefix + 'acc_type_' + 
                    str(int(row.accommodationTypeID)) + '"/>\n'
                )

                # hasCountryParent axiom
                of.write(
                    '        <hasCountryParent rdf:resource="' + self.ott_prefix + 
                    countries_df[countries_df.id == int(row.countryID)]['individual'].values[0] +
                    '"/>\n'
                )

                # hasHotel axiom
                of.write(
                    '        <hasHotel rdf:resource="' + self.ott_prefix +
                    str(int(row.hotelID)) + '"/>\n'
                )
                
                # hotelID attribute
                of.write(
                    '        <hotelID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' +
                    str(int(row.hotelID)) + '</hotelID>\n'
                )

                # accommodationTypeID attribute
                of.write(
                    '        <accommodationTypeID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' +
                    str(int(row.accommodationTypeID)) + '</accommodationTypeID>\n'
                )

                # hotelReviewTitle attribute
                of.write(
                    '        <hotelReviewTitle xml:lang="es">' +
                    str("" if row.reviewTitle != row.reviewTitle else row.reviewTitle) + 
                    '</hotelReviewTitle>\n'
                )

                # hotelNegativeReview attribute
                of.write(
                    '        <hotelNegativeReview xml:lang="es">' +
                    str("" if row.negativeReview != row.negativeReview else row.negativeReview) + 
                    '</hotelNegativeReview>\n'
                )

                # hotelPositiveReview attribute
                of.write(
                    '        <hotelPositiveReview xml:lang="es">' +
                    str("" if row.positiveReview != row.positiveReview else row.positiveReview) + 
                    '</hotelPositiveReview>\n'
                )

                # hotelReviewAccommodationDate attribute
                of.write(
                    '        <hotelReviewAccommodationDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">' +
                    row.accommodationDate + 'T00:00:00' + 
                    '</hotelReviewAccommodationDate>\n'
                )

                # hotelReviewDate attribute
                of.write(
                    '        <hotelReviewDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">' +
                    row.reviewDate + 'T00:00:00' + '</hotelReviewDate>\n'
                )

                # hotelReviewID attribute
                of.write(
                    '        <hotelReviewID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' +
                    str(int(row.reviewID)) + '</hotelReviewID>\n'
                )

                # hotelReviewRating attribute
                of.write(
                    '        <hotelReviewRating rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' +
                    str(row.reviewRating) + '</hotelReviewRating>\n'
                )

                # hotelReviewUser attribute
                of.write(
                    '        <hotelReviewUser rdf:datatype="http://www.w3.org/2001/XMLSchema#string">' +
                    row.reviewUser + '</hotelReviewUser>\n'
                )

                # hotelReviewUserCountryID attribute
                of.write(
                    '        <hotelReviewUserCountryID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' +
                    str(int(row.countryID)) + '</hotelReviewUserCountryID>\n'
                )

                # Close NamedIndividual
                of.write('    </owl:NamedIndividual>\n')

#%%
    def generateAccommodationTypes(self, output_filename):
        """ Generate accommodation types.
    
        Parameters: 
        output_filename.
        
        Returns:
        None (output_filename).
        """

        df = pd.read_csv(
            os.path.join(self.path, self.filename),
            sep=';',
            encoding=self.encoding
        )

        with open(output_filename, 'w') as of:
            for index, row in df.iterrows():
                of.write('\n' * 3)
                
                # Comment
                of.write(
                    '    <!-- ' + self.ott_prefix + 'acc_type_' + 
                    str(int(row.accommodationTypeID)) + ' -->\n\n'
                )

                # Open NamedIndividual
                of.write(
                    '    <owl:NamedIndividual rdf:about="' + 
                    self.ott_prefix + 'acc_type_' + 
                    str(int(row.accommodationTypeID)) + '">\n'
                )

                # Class
                of.write(
                    '        <rdf:type rdf:resource="' + self.ott_prefix +
                    'AccommodationType"/>\n'
                )

                # accommodationTypeDescription attribute
                of.write(
                    '        <accommodationTypeDescription xml:lang="es">' + 
                    row.accommodationTypeName + '</accommodationTypeDescription>\n'
                )

                # accommodationTypeID attribute
                of.write(
                    '        <accommodationTypeID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + 
                    str(int(row.accommodationTypeID)) + '</accommodationTypeID>\n'
                )

                # Close NamedIndividual
                of.write('    </owl:NamedIndividual>')

    def generateHotelScores(self, output_filename):
        score_categories = {
            1 : 'personalScore', 
            2 : 'facilitiesAndServicesScore',
            3 : 'cleaningScore',
            4 : 'comfortScore',
            5 : 'qualityVsPriceScore',
            6 : 'locationScore',
            7 : 'freeWiFiScore' 
        }

        scores_df = pd.read_csv(
            os.path.join(self.path, self.filename),
            sep=';',
            encoding=self.encoding
        )

        ott_prefix = "http://tourdata.org/ontotoutra/ontotoutra.owl#"

        with open(output_filename, 'w') as of:
            for index, row in scores_df.iterrows():
                of.write('\n' * 3)
                of.write(
                    '    <!-- ' + ott_prefix + 
                    'hotel_score_' + 
                    str(int(row.hotelScoreID)) + 
                    ' -->\n\n'
                )
                of.write(
                    '    <owl:NamedIndividual rdf:about="' + 
                    ott_prefix +
                    'hotel_score_' + 
                    str(int(row.hotelScoreID)) +
                    '">\n'
                )
                of.write(
                    '        <rdf:type rdf:resource="'  + 
                    ott_prefix +
                    'HotelScore"/>\n'
                )
                of.write(
                    '        <hasScoreCategory rdf:resource="' +
                    ott_prefix +
                    score_categories[int(row.scoreCategoryID)] +
                    '"/>\n'
                )
                of.write(
                    '        <hotelID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' +
                    str(int(row.hotelID)) +
                    '</hotelID>\n'
                )
                of.write(
                    '        <hotelScoreID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' +
                    str(int(row.hotelScoreID)) +
                    '</hotelScoreID>\n'
                )
                of.write(
                    '        <score rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' +
                    str(row.score) +
                    '</score>\n'
                )
                of.write(
                    '        <scoreCategoryID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' +
                    str(int(row.scoreCategoryID)) +
                    '</scoreCategoryID>\n'
                )
                of.write('    </owl:NamedIndividual>\n')


    def generateServiceCategories(self):
        services_df = pd.read_csv(
            os.path.join(self.path, self.filename), 
            sep=';', 
            encoding=self.encoding
        )

        ott_prefix = "http://tourdata.org/ontotoutra/ontotoutra.owl#"

        for index, row in services_df.iterrows():
            print("\n\n")
            print("    <!-- " + ott_prefix + row.Individual + " -->")
            print("")
            print('    <owl:NamedIndividual rdf:about="' + ott_prefix + row.Individual + '">')
            print('        <rdf:type rdf:resource="' + ott_prefix + 'ServiceCategory"/>')
            print(
                '        <serviceCategoryID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + 
                str(row.serviceCategoryID) + 
                '</serviceCategoryID>'
            )
            print('        <serviceCategoryName xml:lang="es">' + row.serviceCategoryName + '</serviceCategoryName>')
            print('        <serviceCategoryName xml:lang="en">' + row.English + '</serviceCategoryName>')
            print('    </owl:NamedIndividual>')


    def generateServices(self):
        # Read csv and store it in dataframe
        services_df = self.csv2DF(
            os.path.join(self.path, self.filename), ';', self.encoding
        )

        ott_prefix = "http://tourdata.org/ontotoutra/ontotoutra.owl#"

        for index, row in services_df.iterrows():
            print("\n\n");
            print("    <!-- " + ott_prefix + 'service_' + str(row.serviceID) + " -->")
            print("")
            print(
                '    <owl:NamedIndividual rdf:about="' +
                ott_prefix +
                'service_' +  
                str(row.serviceID) +
                '">'
            )
            print('        <rdf:type rdf:resource="' + ott_prefix + 'Service"/>')
            print(
                '        <serviceID rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + 
                str(row.serviceID) + 
                '</serviceID>'
            )
            print('        <serviceName xml:lang="es">' + row.serviceName + '</serviceName>')
            print('    </owl:NamedIndividual>')

 
    def readTextFile(self, filename):
        # Read the ontology file and store it in a list
        input_file = open(filename, "r")
        owl_list = [line for line in input_file]
        input_file.close()
        return owl_list


    def addAxiom(self, individual, axiom, key_field, df, id_field, select_field, output_filename):
        # Read the ontology file and store it in a list
        owl_list = self.readTextFile(
            os.path.join(self.owl_path, self.owl_filename)
        )

        # Add the hasServiceCategory axiom
        with open(output_filename, 'w') as output_file:
            for i in range(len(owl_list)):
                # Write the owl-file line
                output_file.write(owl_list[i])

                # Is the axiom?
                if (
                    owl_list[i].find(individual) != -1 and 
                    owl_list[i - 1].find('owl:NamedIndividual') != -1
                ):               
                    # Get a field
                    i += 1
                    while (owl_list[i].find('owl:NamedIndividual') == -1):
                        if (owl_list[i].find(key_field) != -1):
                            # Get the key field
                            id_start = owl_list[i].find('>') + 1
                            id_end   = owl_list[i].find('<', id_start)
                            id       = owl_list[i][id_start: id_end]

                            # Write out the new axiom
                            for field in set(df[df[id_field] == int(id)][select_field].values):
                                output_file.write(axiom.format(field))
                            break
                        i += 1

#%%
def callGenerateServicesCategories():
    filename = 'serviceCategory.csv'
    gr = GenerateRDF(path, filename, encoding, owl_path, owl_filename, ott_prefix)
    gr.generateServiceCategories()

#%%
def callGenerateServices():
    filename = 'service.csv'
    gr = GenerateRDF(path, filename, encoding, owl_path, owl_filename, ott_prefix)
    gr.generateServices()

#%%
def callGenerateHotelScores():
    """ Call the generateHotelScores method.
    
    Parameters: 
    None.
    
    Returns:
    None (output_filename).
    """

    filename = 'hotelScore.csv'
    gr = GenerateRDF(path, filename, encoding, owl_path, owl_filename, ott_prefix)
    gr.generateHotelScores(output_filename = 'bla.txt')

#%%
def callGenerateAccommodationTypes():
    """ Call the generateAccommodationTypes method.

    Parameters:
    None.

    Returns:
    None (output_filename)
    """

    filename = 'accommodationType.csv'
    gr = GenerateRDF(path, filename, encoding, owl_path, owl_filename, ott_prefix)
    gr.generateAccommodationTypes(output_filename = 'bla.txt')

#%%
def callGenerateHotelReviews():
    """ Call the generateHotelReviews method.
    
    Parameters: 
    None.
    
    Returns:
    None (output_filename).
    """

    filename = 'hotelReview.csv'
    gr = GenerateRDF(path, filename, encoding, owl_path, owl_filename, ott_prefix)
    gr.generateHotelReviews(output_filename = 'bla.txt')

#%%
def callAxiom(filename, individual, axiom, key_field, id_field, select_field, output_filename):
    """ Call addAxiom method.
    
    Parameters: 
    None.
    
    Returns:
    None (output_filename).
    """

    gr = GenerateRDF(path, filename, encoding, owl_path, owl_filename, ott_prefix)

    gr.addAxiom(
        individual      = individual,
        axiom           = axiom,
        key_field       = key_field,
        df              = gr.csv2DF(os.path.join(path, filename), ';', encoding),
        id_field        = id_field,
        select_field    = select_field,
        output_filename = output_filename
    )

#%%
if __name__ == "__main__":
    owl_path     = '/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/'
    owl_filename = 'ontotoutra.owl'
    path         = '/home/jf/Documentos/education/phd/thesis/dev/ontologies/protege/mysql csv data/'
    encoding     = 'iso8859_2'
    ott_prefix   = "http://tourdata.org/ontotoutra/ontotoutra.owl#"

    # callGenerateServicesCategories()
    # callGenerateServices()
    # callGenerateHotelScores()
    # callGenerateAccommodationTypes()
    callGenerateHotelReviews()

    # callAxiom(
    #     filename        = 'service.csv', 
    #     individual      = '#Service"',
    #     axiom = '        <hasServiceCategory rdf:resource="http://tourdata.org/ontotoutra/ontotoutra.owl#{}"/>\n',
    #     key_field       = 'serviceID',
    #     id_field        = 'serviceID',
    #     select_field    = 'categoryService',
    #     output_filename = 'ott2.owl'
    # )

    # callAxiom(
    #     filename        = 'hotelService.csv', 
    #     individual      = '#Hotel"',
    #     axiom = '        <hasService rdf:resource="http://tourdata.org/ontotoutra/ontotoutra.owl#service_{}"/>\n',
    #     key_field       = 'hotelID',
    #     id_field        = 'hotelID',
    #     select_field    = 'serviceID',
    #     output_filename = 'ott2.owl'
    # )

    # callAxiom(
    #     filename        = 'hotelScore.csv', 
    #     individual      = '#Hotel"',
    #     axiom = '        <hasService rdf:resource="http://tourdata.org/ontotoutra/ontotoutra.owl#service_{}"/>\n',
    #     key_field       = 'hotelID',
    #     id_field        = 'hotelID',
    #     select_field    = 'serviceID',
    #     output_filename = 'ott2.owl'
    # )

    # callAxiom(
    #     filename        = 'hotelScore.csv', 
    #     individual      = '#HotelScore"',
    #     axiom = '        <hasHotelScore rdf:resource="http://tourdata.org/ontotoutra/ontotoutra.owl#{}"/>\n',
    #     key_field       = 'hotelID',
    #     id_field        = 'hotelID', 
    #     select_field    = 'hotelID',
    #     output_filename = 'ott2.owl'
    # )
    
