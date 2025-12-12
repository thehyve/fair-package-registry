import requests
import csv
import hashlib


def get_token(url):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "email": "albert.einstein@example.com",
        # "password": "password"
        "password": "zJdDvlpam#i9118W"
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    token = response.json().get("token")

    return token


def add_dataset(url, token, dataset_info):
    headers = {
        "Accept": "text/turtle",
        "Content-Type": "text/turtle",
        "Authorization": f"Bearer {token}"
    }
    
    body = f"""
            <> a dcat:Resource, dcat:Dataset;
        <http://www.w3.org/2000/01/rdf-schema#label> "Dataset" ;
        dcterms:title "{dataset_info['title']}" ;
        dcat:version "{dataset_info['version']}";
        dcterms:license <http://purl.org/NET/rdflicense/cc-zero1.0>;
        dcterms:description "{dataset_info['description']}";
        dcterms:conformsTo <http://localhost/profile/2f08228e-1789-40f8-84cd-28e3288c3604>,
            <http://localhost/profile/2f08228e-1789-40f8-84cd-28e3288c3604>;
        dcterms:language <http://id.loc.gov/vocabulary/iso639-1/en>;
        <https://w3id.org/fdp/fdp-o#metadataIdentifier> <#identifier>;
        dcterms:identifier "{dataset_info['identifier']}";
        dcterms:accessRights <http://publications.europa.eu/resource/authority/access-right/PUBLIC>;
        dcterms:publisher [ a foaf:Agent;
            dcterms:identifier "https://identifier.overheid.nl/tooi/id/zbo/zb000114", "https://www.zorginstituutnederland.nl/";
            foaf:name "Zorginstituut Nederland";
            <http://healthdataportal.eu/ns/health#publishernote> "Het Zorginstituut Nederland is zelfstandig bestuursorgaan dat ervoor zorgt dat de Nederlandse gezondheidszorg voor iedereen goed, toegankelijk en betaalbaar blijft, nu en in de toekomst";
            <http://healthdataportal.eu/ns/health#publishertype> <http://purl.org/adms/publishertype/NationalAuthority>;
            dcterms:spatial <http://publications.europa.eu/resource/authority/country/NLD>;
            foaf:homepage <https://www.zorginstituutnederland.nl/>;
            foaf:mbox <mailto:info@zin.nl>
            ];
        dcterms:isPartOf {dataset_info['isPartOf']};
        <http://semanticscience.org/resource/SIO_000628> </metrics/445c0a70d1e214e545b261559e2842f4>,
            </metrics/5d27e854a9e78eb3f663331cd47cdc13>;
        dcat:keyword {dataset_info['keywords']};
        dcat:theme <http://publications.europa.eu/resource/authority/data-theme/HEAL>;
        dcat:landingPage <https://www.zorginstituutnederland.nl/documenten/2023/10/24/standpunt---mammaprint-en-oncotype-dx-vergoede-zorg-voor-bepaalde-groep-vrouwen>;
        dcat:contactPoint [ a <http://www.w3.org/2006/vcard/ns#Kind>;
            <http://www.w3.org/2006/vcard/ns#fn> "Zorginstituut Nederland";
            <http://www.w3.org/2006/vcard/ns#hasEmail> <mailto:info@zinl.nl>;
            <http://www.w3.org/2006/vcard/ns#hasURL> <https://www.zorginstituutnederland.nl/service/contact>
            ];
        dcterms:spatial <http://publications.europa.eu/resource/authority/country/NLD>;
        <http://data.europa.eu/r5r/applicableLegislation> <http://example.org/unknown>;
        <http://healthdataportal.eu/ns/health#healthTheme> {dataset_info['healthThemes']};
        dcterms:creator [ a foaf:Agent;
            dcterms:identifier "http://zorginstituutnederland.nl";
            foaf:name "Zorginstituut Nederland";
            <http://healthdataportal.eu/ns/health#publishernote> "National Health Care Institute works to ensure that everyone in the Netherlands has access to good care, now and in the future.";
            <http://healthdataportal.eu/ns/health#publishertype> <http://purl.org/adms/publishertype/NationalAuthority>;
            dcterms:spatial <http://publications.europa.eu/resource/authority/country/NLD>;
            foaf:homepage <https://www.zorginstituutnederland.nl/>;
            foaf:mbox <mailto:info@zin.nl>
            ];
        dcterms:type <http://publications.europa.eu/resource/authority/dataset-type/TEST_DATA>;
        foaf:page {dataset_info['page']};
        <https://w3id.org/dpv#hasPurpose> <https://w3id.org/dpv#PublicBenefit> .


        <#accessRights> a dcterms:RightsStatement;
        dcterms:description "This resource has no access restriction" .

        <http://localhost/analyticsdistribution/> a ldp:DirectContainer, ldp:DirectContainer;
        dcterms:title "Analytics Distributions", "Analytics Distributions";
        ldp:hasMemberRelation <http://healthdataportal.eu/ns/health#analytics>, <http://healthdataportal.eu/ns/health#analytics>;
        ldp:membershipResource <>,
            <> .

        <http://localhost/datasetseries/> a ldp:DirectContainer, ldp:DirectContainer;
        dcterms:title "Dataset Series", "Dataset Series";
        ldp:hasMemberRelation dcat:inSeries, dcat:inSeries;
        ldp:membershipResource <>,
            <> .

        <http://localhost/distribution/> a ldp:DirectContainer, ldp:DirectContainer;
        dcterms:title "Distributions", "Distributions";
        ldp:hasMemberRelation dcat:distribution, dcat:distribution;
        ldp:membershipResource <>,
            <> .

        <http://localhost/sampledistribution/> a ldp:DirectContainer, ldp:DirectContainer;
        dcterms:title "Sample Distributions", "Sample Distributions";
        ldp:hasMemberRelation <http://www.w3.org/ns/adms#sample>, <http://www.w3.org/ns/adms#sample>;
        ldp:membershipResource <>,
            <> .

        <http://localhost/profile/2f08228e-1789-40f8-84cd-28e3288c3604> <http://www.w3.org/2000/01/rdf-schema#label>
            "Dataset Profile", "Dataset Profile" .

        </metrics/445c0a70d1e214e545b261559e2842f4>
        <http://semanticscience.org/resource/SIO_000628> <https://www.ietf.org/rfc/rfc3986.txt>;
        <http://semanticscience.org/resource/SIO_000332> <https://www.ietf.org/rfc/rfc3986.txt> .

        </metrics/5d27e854a9e78eb3f663331cd47cdc13>
        <http://semanticscience.org/resource/SIO_000628> <https://www.wikidata.org/wiki/Q8777>;
        <http://semanticscience.org/resource/SIO_000332> <https://www.wikidata.org/wiki/Q8777> .
    """

    response = requests.post(url, data=body, headers=headers)
    assert response.status_code == 201, f"Failed to add dataset: {response.text}"
    
    location = response.headers.get("Location")
    
    return location


def publish_dataset(location, token):

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = '{"current": "PUBLISHED"}'

    url = f"{location}/meta/state"
    response = requests.put(url, headers=headers, data=data)
    
    return response.status_code


def get_dataset_info(title, version, description, identifier, isPartOf, keywords, healthThemes, page):
    keyword_string = ', '.join([f'"{kw.strip()}"' for kw in keywords])
    health_theme_string = ', '.join([f'<{ht.strip()}>' for ht in healthThemes])
    
    dataset_info = {
        "title": title,
        "version": version,
        "description": description,
        "identifier": identifier,
        "isPartOf": f"<{isPartOf}>",
        "keywords": keyword_string,
        "healthThemes": health_theme_string,
        "page": f"<{page}>"
    }
    
    return dataset_info


def read_pakketadviezen_csv(filepath):
    """
    Reads the ZIN pakketadviezen CSV file and returns a list of dictionaries.
    Each dictionary represents a row with column headers as keys.
    """
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        return list(reader)


baseurl = "https://fdp-zin.dci.thehyve.nl/"

pakketadviezen = read_pakketadviezen_csv("../src/data/ZIN_pakketadviezen_2024_ChatGPT_20250917(2024 Pakketadviezen).csv")
# catalog_uri="http://localhost/catalog/932dbf1b-38af-4fb0-8118-ebfad5dedd23"
catalog_uri = "https://fdp-zin.dci.thehyve.nl/catalog/b4f2d88f-bd6e-44e7-a4a4-87861aab964d"

token = get_token(f"{baseurl}tokens")

# Publicatiedatum;Aandoening;ICD-10;Indicatie;Behandeling;RxNorm;
for row in pakketadviezen:
    
    keywords = [ row["Aandoening"].strip(), 
                # row["Indicatie"].strip(), 
                row["Behandeling"].strip(), 
                row["Geneesmiddel"].strip() ]
    health_theme = [ht.strip() for ht in row["Wikidata-geneesmiddel-URI"].split(";") if ht.strip()]
    health_theme += [ht.strip() for ht in row["Wikidata-Indicatie-URI"].split(";") if ht.strip()]
    
    dataset_info = get_dataset_info(
        title=row["Naam besluit"],
        version="0.0.1",
        description=row["Samenvatting"],
        identifier=hashlib.md5(row["Naam besluit"].encode()).hexdigest(),
        isPartOf=catalog_uri,
        keywords=keywords,
        healthThemes=health_theme,
        page=row["PDF_link"]
    )
    
    location = add_dataset(f"{baseurl}dataset", token, dataset_info)
    print(f"Dataset added at: {location}")
    status = publish_dataset(location, token)
    print(f"Publish status code: {status}")




