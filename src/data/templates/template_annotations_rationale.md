# FAIR Package Statement — annotatie-rationale & versiegeschiedenis

Companion-document bij `template_package_statement_annotated.yaml`.

De lean template is het **invulinstrument**: velden plus alleen de dragende
extractie-instructies (`DEFINITION` / `SOURCE` / `PITFALL` / `HOW`). Alles wat
géén invulsturing is — versiegeschiedenis, de herkomst van de extensies, en de
achterliggende redenaties — staat hier. Zo blijft de template gefocust op vullen
en verwatert de aandacht niet (zie *Annotatiediscipline* onderaan).

De inline markers `[ZIN-EXTENSION]`, `[ZIN-EXTENSION-V2]`, `[v4]` en `[v5]` zijn
uit de template gehaald. Voor het vullen doet de herkomst van een annotatie er
niet toe — een instructie is een instructie. Dit document is voortaan hun register.

---

## 1. Lijnage

- **Basistemplate:** The Hyve template v1 (het generieke FAIR package-statement-model).
- **ZIN-uitbreidingen:** velden en blokken die ZIN heeft toegevoegd voor
  signalering en voor niet-farmacologische / companion-diagnostic-casussen.
- **Annotatie-iteraties (v4, v5):** geen nieuwe velden, alleen scherpere
  invulinstructies, gekalibreerd op concrete casussen.

---

## 2. Herkomst van de extensies (wat de markers aanduidden)

### 2.1 ZIN-uitbreidingen (voorheen `[ZIN-EXTENSION]`)

Toevoegingen aan het basismodel voor de signaleringspipeline en de beoordelings­logica:

- **Surrogaat-gebaseerde beoordeling** — `emsmps.basis-uitkomst`,
  `emsmps.surrogaat-voor-uitkomst-id`. Legt vast of de conclusie op een primaire
  dan wel een surrogaatuitkomst rust.
- **Herbeoordelingstriggers** — `emsmps.herbeoordelingsconditie`,
  `emsmps.herbeoordelingstriggers` (elk met `label` + verplicht `type`:
  `literatuur` / `registratie` / `zorggebruik`). Voedt de pipeline die bepaalt
  wélk soort nieuwe evidence een herbeoordeling kan triggeren.
- **Aanvullende publicatie-identifiers** — `publications.doi` / `pmid` /
  `openalex-id`. Maken directe API-toegang tot abstracts/metadata mogelijk.
- **Subgroep-/subsetvelden** — `outcome-measurements.is-subset-analyse`,
  `subset-type`, `subset-toelichting`.

### 2.2 ZIN v2-uitbreidingen (voorheen `[ZIN-EXTENSION-V2]`)

Toegevoegd om een **companion diagnostic** te kunnen vastleggen die met een eigen
PICO en eigen evidence wordt beoordeeld, maar géén los positief/negatief
pakketadvies krijgt — hij fungeert als *voorwaarde* op het geneesmiddel:

- **`linked-diagnostics`** — subblok ónder een IIC-assessment. De diagnostiek
  blijft vastgeklonken aan het middel dat zij conditioneert; zij wordt geen aparte
  IIC met een geforceerde binaire conclusie.
- **Niet-binaire `conclusion-type`** — bv. `condition-on-intervention`.
- **Diagnostische-accuratesse-uitkomsten** — extra `type`-waarden in
  `outcome-measurements`: `concordance`, `overall percent agreement`,
  `sensitivity`, `specificity`, `positive/negative predictive value`,
  `cohens kappa`, `proportion-selected`.
- **Diagnostische vergelijkingsvelden** — `reference-test`, `index-test`,
  `sample-n` (in plaats van `cohort-ids` voor accuratessemetingen).
- **Test-treat-PICO's** — een diagnostiek-PICO waarin interventie en comparator
  dezelfde behandeling zijn, geleid door verschillende tests.

> **Ontwerpnotitie (niet over-generaliseren).** v2 is gebouwd op één enkele
> diagnostiek-casus en hergebruikt bewust bestaande veldvormen. Een apart
> top-level diagnostiek-objecttype wordt pas overwogen zodra een **tweede**
> diagnostiek-casus opduikt (*meet-dan-besluit*).

---

## 3. Versiegeschiedenis (changelogs)

### v2 — companion diagnostic (rationale)

Sommige pakketadviezen beoordelen meer dan de vergoede interventie. Een companion
diagnostic kan een eigen PICO en eigen evidence hebben, maar zónder los advies —
zij werkt als voorwaarde op het middel ("alleen test X kwalificeert tot
concordantie is aangetoond") plus een risicoanalyse ("verkennende analyse" /
"risicogericht pakketbeheer"). Het basismodel kon dit niet dragen: elk beoordeeld
object werd in een binair advies geperst en accuratesse-uitkomsten hadden geen
plek. v2 voegt minimaal toe:

1. Een `linked-diagnostics`-subblok onder een IIC (diagnostiek blijft aan het
   middel gekoppeld, wordt geen aparte IIC met verzonnen binaire conclusie).
2. Een niet-binaire `conclusion-type` voor die diagnostiek.
3. Diagnostische-accuratesse-meettypen in `outcome-measurements`.
4. Expliciete `publication-ids` op de diagnostiek (met pmid/doi) zodat de
   pipeline de diagnostiek-evidence kan monitoren/retractie-checken — publicaties
   die term-based retrieval op de *geneesmiddel*-config NIET vindt (ze noemen het
   middel vaak niet; empirisch bevestigd op **PMID 35970977, Rüschoff 2022**).

### v4 — kalibratie op een niet-farmacologisch standpunt (iMSR chronische pijn)

Stress-test van annotaties die rond sluisgeneesmiddelen waren geschreven.
Correcties/verduidelijkingen waar twee onafhankelijke fills van dezelfde PDF
divergeerden, of waar de annotatie actief misleidde. Geen velden toegevoegd of
verwijderd.

1. **`indication-ids`** — herstelde de basisduidelijkheid dat populaties tevens de
   indicaties zíjn (v3 had dit gestript, wat willekeurige fills gaf).
2. **`case-`/`serial-number`** — vastgepind op Zaaknummer/Volgnummer (colofon);
   "Onze referentie" landt NIET in de YAML; plus cross-check en één-nummer-fallback.
3. **`publications` DOI/PMID** — check éérst de referentielijst (DOI staat er vaak);
   DOI→PMID-resolutie mag, vrije-tekst-lookup (titel/auteur) niet.
4. **`cost-effective`** — `inconclusive` toegevoegd (was geforceerd True/False).
5. **`outcome-measurements`** — per-studie-effecten horen hier óók als de review
   niet poolde ("niet gepoold" ≠ "geen effectgrootte"); een waarde die in de
   conclusie wordt genoemd, moet hier terugkomen; de unit van een gestandaardiseerde
   maat is dimensieloos.
6. **BIA** — signaleer wanneer de budgetimpact niet betrouwbaar te modelleren is,
   in plaats van waarden te verzinnen om Current/Substitution/Total te vullen.
7. **`herbeoordelingstriggers`** — sleutel `tekst` → `label` (sluit aan op gevulde
   YAML's en het dashboard); `type` blijft verplicht.
8. **Klein** — datum = adviesbriefdatum (niet vaststelling/ingangsdatum); studies =
   de doorslaggevende/PICO-matchende studies; contactpersoon-bron verbreed.

### v5 — kalibratie op een tweede sluiscasus mét companion diagnostic (Enhertu / trastuzumab-deruxtecan, HER2-low)

Twee onafhankelijke fills van dezelfde PDF zijn ge-diff't; v5 scherpt de annotaties
op de punten waar de fills divergeerden of waar één fill een waarde fabriceerde.
Geen velden toegevoegd of verwijderd.

1. **Test-treat-PICO** — maak van de twee teststrategieën *aparte* interventie-entries
   (elk een eigen intervention-group); het testcontrast hoort in de gestructureerde
   velden, niet in een comment. *(Eén fill vouwde beide armen samen tot één group.)*
2. **BIA-diagnostiekkosten** — modelleer apart gerapporteerde diagnostiek-budgetimpact
   als een eigen `CostEstimation` (type `Additional`), niet ingevouwen of in een comment.
3. **BIA-diepte** — "signaleer het gat" (v4 #6) geldt alleen als data écht ontbreken;
   bevat het BIA-subrapport een volledige jaartabel, vul dan de complete reeks —
   stop niet bij de afgeronde samenvattingsgetallen uit de adviesbrief.
4. **Publicaties** — neem de titel **verbatim** over in de oorspronkelijke taal
   (geen parafrase/vertaling); verbatim titels sturen titel-gebaseerde retrieval.
5. **`serial-number` tie-break** — bij een bundel met meerdere subrapporten (elk met
   een Volgnummer) het Volgnummer van het Farmacotherapeutisch rapport gebruiken;
   de rest in een comment noteren.
6. **Accuratesse-discipline** — leg alleen expliciet vermelde getallen vast; leid
   geen concordantie af voor een dichotomie die de bron niet numeriek rapporteert.

### v6 — linked-diagnostic gepromoveerd tot eigenstandige IIC

**Wat:** het genestelde blok `intervention-indication-combination-assessments[].linked-diagnostics`
is opgeheven. Een companion diagnostic krijgt een eigen `IICAssessment` met
`iic-role: linked-diagnostic` en `depends-on-iic-id`.

**Waarom:** het genestelde blok dupliceerde velden die IIC en emsmp al dragen (`picots-id`,
`slr-id`, `outcome-measurement-ids`, triggers, conclusie) en kortsluitte de publicatieroute met
een eigen `publication-ids` — waardoor de diagnostiek-SLR in de Enhertu-fill v3 een **lege**
`literature-reference-list` had en de diagnostiekpapers modelmatig onbereikbaar waren. De rest
van dit datamodel is consequent **id-gerefereerd**; `linked-diagnostics` was de enige plek waar
een volledig sub-assessment werd *ingebed* in plaats van *gerefereerd*. Promotie brengt de
diagnostiek terug in het idioom van het model en laat de beleidsafhankelijkheid intact — nu als
expliciete referentie.

**De prijs, eerlijk benoemd:** de v2-nesting bestond om te vermijden dat de test een verzonnen
binaire conclusie zou krijgen. Promotie brengt die velden terug en zet ze op `null` onder een
expliciete rol-vlag (conditionele regels 1–3). Een `null` met een verklarende rol is eerlijk;
een gefabriceerde `Positive` is dat niet.

**Beleidsgrondslag** (bestudeerd: kader medische tests 2011; module SWP moleculaire diagnostiek
mei 2025; Eindbrief uitvoeringstraject moleculaire diagnostiek dec 2023):
- Medische tests zitten in het **open systeem**: naleving van SvWP wordt *stilzwijgend aangenomen*;
  ZIN-toetsing is een **gebeurtenis**, geen eigenschap. → veld `assessment-framing`.
- Beoordeling van diagnostiek bij **instroom** van een geneesmiddel valt expliciet **buiten** de
  scope van de module en loopt via *risicogericht pakketbeheer*. De Enhertu-"verkennende analyse"
  ís die route. → `assessment-framing: exploratory-risk-based` is beleidsconform.
- De test-beoordeling is **conditioneel op het middel** (stappenplan, stap 1). → `depends-on-iic-id`.
- SvWP voor een test = **klinisch nut** (gezondheidswinst van de test-plus-behandelstrategie);
  accuratesse is *een factor daarin*, niet het criterium.

**`basis-uitkomst` bij diagnostiek = `primary` (accuratesse), NIET `surrogate`.** Een surrogaat
schat een *onbekende* uitkomst (PFS → immature OS). Bij een companion diagnostic is de
gezondheidswinst **bekend en bewezen** — in de door de referentietest geselecteerde populatie.
Accuratesse schat die winst niet; zij toetst of het bewezen effect **overdraagbaar** is
(indirectness/transferability — GRADE's eigen term, en de term die de ZIN-module zelf gebruikt).
Codeer je het als `surrogate`, dan leidt de afleidlaag OS af als beslis-relevante uitkomst en
sorteren concordantiepapers via `uitkomstmaat_match: nee` naar de **onderkant** — precies de
publicaties waarvoor de diagnostiek-monitoring bestaat.

**Nieuw trigger-`type`: `beroepsgroep`.** Herkomst: het ZIN-raamwerk moleculaire diagnostiek
(CieBOD = "HOE er getest moet worden", CieMKNT = "WAT", CieBAG = aanspraak, NVVP-kwaliteitsstandaard).
Beslisregel: *niet* "kan hierover gepubliceerd worden?" maar **"zou een publicatie hierover ZIN
tot actie bewegen?"** Legt het advies de vraag bij de beroepsgroep, dan is het type `beroepsgroep`
— ook als het onderliggende bewijs in tijdschriften verschijnt. Gevolg voor Enhertu: de
diagnostiek-IIC heeft **nul** literatuur-triggers. Dat is correct, niet defect.

**Empirische validatie (blinde invuloefening).** Een naïeve sessie — alleen template + bronstukken,
geen kennis van het ontwerp — vulde het Enhertu-advies in. Uitkomst: **alle dragende beslissingen
convergeerden** met de referentie-fill (twee IIC's; richting van `depends-on-iic-id`; drie
conditionele regels; `basis-uitkomst: primary`; `conclusion-type: condition-on-intervention`;
4× `beroepsgroep`; SLR→LRL bedraad; test-treat-PICO met twee echt verschillende
interventiegroepen; nul dangling references). De trigger-typering werd bereikt **zonder** de
onderliggende beleidsredenering — die staat nergens in de template. De beslisregel codeert het
beleidsoordeel dus correct. Alle divergenties waren van één type — *structuur aanwezig,
invulinstructie afwezig* — en zijn in v6.1 als annotatie verwerkt. Bewijs: `validatie_v6/`.

### v6.1 — annotaties aangescherpt op basis van de blinde invuloefening

Tien wijzigingen, alle uit het invullogboek of uit de structurele diff:
gevolgenkaart onder `iic-role` · `assessment-type` ≠ sluis-procesterm · kritiek op het
*model* ≠ oordeel over de *interventie* (`cost-effective`) · `number-of-items` ≠ `len(references)` ·
eenheid/basis bij `costs` · **een beschikbare enum-waarde ís een invulinstructie**
(`proportion-selected`, `cohens kappa` horen niet in een comment) · `index-test` en
`reference-test` **mogen dezelfde test zijn** (validatie-/reproduceerbaarheidsstudie van de
referentietest zélf) · triggergranulariteit (één trigger per zelfstandig monitorbare gebeurtenis) ·
pre-gespecificeerde subgroepen als eigen `OutcomeMeasurement` · correctie van de claim dat
diagnostiekpapers het middel "veelal niet noemen".

**Afgewezen advies (met reden):** het logboek stelde voor een redactionele kruisverwijzing naar de
diagnostiek toe te staan in de `conclusion-text` van het geneesmiddel. Afgewezen: de verwijzing is
al **structureel en inverteerbaar** aanwezig (elke IIC waarvan `depends-on-iic-id` naar mij wijst,
is mijn linked-diagnostic), en proza in een verbatim-veld ondergraaft de regel *signaleren,
niet fabriceren*.

### v6.2 — laatste openstaande annotatie-advies + herstel van de validatie-referent

**Annotatie (één wijziging).** *Financieel arrangement is óók een `zorggebruik`-trigger.* Een
prijsafspraak met een doorlooptijd of herzieningsmoment is niet alleen `managed-entry-agreement-text`:
het arrangement lóópt af en wordt herzien op werkelijke budgetimpact. Alleen in het tekstveld
vastleggen verbergt een gedateerd, ingepland herbeoordelingsmoment voor de pipeline. De overlap tussen
de twee velden is bedoeld, geen dubbeling. *(Herkomst: de naïeve fill zette het arrangement uitsluitend
in het tekstveld; de referentie-fill deed allebei.)*

Hiermee zijn alle negen adviezen uit het invullogboek afgehandeld: zeven verwerkt in v6.1, één hier, en
één **afgewezen** (de redactionele kruisverwijzing in `conclusion-text` — zie v6.1, "Afgewezen advies";
die afwijzing staat).

**Herstel van de validatie-referent.** De blinde invuloefening is uitgevoerd tegen **v6.0**, dat bij het
plaatsen van v6.1 niet was gearchiveerd en dus in de repository ontbrak — terwijl het promptbestand in
`validatie_v6/` ernaar verwijst. v6.0 is alsnog geplaatst als `..._annotated_lean_v6.yaml`, en
`validatie_v6/README.md` legt de koppeling vast (met blob-SHA).

**Preciseringen die daaruit volgen — belangrijk voor het lezen van de v6-changelog:**
- Wat de blinde oefening valideerde, is de **v6.0-structuur** (`iic-role`, `depends-on-iic-id`, de drie
  conditionele nulls, test-treat-PICO, `beroepsgroep`). Die structuur is in v6.1 en v6.2 ongewijzigd —
  alle diffs sinds v6.0 zijn zuiver additief commentaar. De structurele conclusie draagt dus door.
- Wat zij **niet** valideerde, zijn de v6.1-annotaties zelf: die zijn de *uitkomst* van de oefening.
  Zeven ervan bestaan omdat de fill erop struikelde. "v6.1 is blind gevalideerd" is daarom een
  circulaire claim; correct is: "de v6-structuur is blind gevalideerd; de v6.1-annotaties zijn de
  remedie die daaruit volgde."
- Een echte toets van de annotaties splitst in twee routes. **Zeven van de elf zijn generiek** (o.a.
  `assessment-type` ≠ sluis-procesterm, `cost-effective`, `number-of-items`, `costs`-basis,
  triggergranulariteit, subgroepen, financieel arrangement) en worden vanzelf gemeten zodra een
  volgende fill tegen een referentie wordt ge-diff't — *diff-als-QA*, geen aparte oefening nodig. De
  **vier diagnostiek-specifieke** (gevolgenkaart `iic-role`; enum-waarde ís instructie; `index-test` =
  `reference-test`; de LRL-correctie) zijn niet toetsbaar op de fills die nu op de rol staan — die
  bevatten geen linked diagnostic. Zij wachten op een **tweede companion-diagnostic-casus**, conform
  de v2-ontwerpnotitie (*meet-dan-besluit*). Tot dan zijn ze expliciet ongetoetst.

---

### v6.3 — `number-of-items` bij gebundelde adviezen

**Annotatie (één wijziging).** De v6.1-annotatie bij `number-of-items` waarschuwt tegen het twee keer
schrijven van hetzelfde getal ("If you find yourself writing the same number twice, re-read this line").
Die waarschuwing is geschreven vanuit een advies met één beoordeling en één zoekactie. Bij een **gebundeld**
advies slaat zij om in een **vals alarm**: één advies heeft één doorlopende referentielijst, dus élke
`literature-reference-list` in dat advies krijgt hetzelfde documentbrede getal. v6.3 maakt het onderscheid
expliciet — herhaling **ácross** lijsten is correct, gelijkheid aan `len(references)` **bínnen** één lijst is
de fout waarvoor gewaarschuwd wordt — en verbiedt het optellen van het veld over lijsten heen.

*(Herkomst: de fill van het Standpunt Herbeoordeling PARP-remmers, zes beoordelingen met zes zoekacties. Alle
zes referentielijsten kregen `number-of-items: 96`. De invuller ging op grond van de annotatie twijfelen of er
iets misging, terwijl de vulling correct was. Vastgelegd als O44.)*

De vraag die hierbij opkwam — **waarvoor is dit veld eigenlijk bedoeld?** — is niet in deze changelog
beantwoord maar doorgezet naar de eigenaar van het basistemplate; zie **§6**.

## 4. Design-rationale (achterliggende principes)

**Meet-dan-besluit.** Meet eerst empirisch, beslis dan over architectuur.
Extrapoleer niet uit redenering alleen. Dit geldt voor de structuur (pas een nieuw
objecttype bij een tweede casus, zie v2-ontwerpnotitie) én voor de annotaties (voeg
een instructie pas toe als een fill aantoonbaar misging).

**Diff-als-QA.** Twee onafhankelijke fills van dezelfde PDF draaien en vergelijken
is een betrouwbare manier om annotatiegaten en template-ambiguïteit te vinden. Elke
annotatie-iteratie (v4, v5) is op precies deze manier ontstaan: niet uit theorie,
maar uit waargenomen divergentie. Voorbeelden uit de Enhertu-diff die v5 stuurden:

- *Zaaknummer vs. "Onze referentie":* de ene fill zette het brief-ID in `case-number`;
  de v4-annotatie ving dat af. → annotatie werkt.
- *Herbeoordelingstriggers zonder `type`:* de ene fill gebruikte kale strings; de
  v4-`type`-annotatie dwong de classificatie af. → annotatie werkt.
- *Test-treat-PICO samengevouwen:* de annotatie was beschrijvend, niet dwingend →
  v5 maakt hem imperatief (aanleiding voor wijziging #1 hierboven).
- *Gefabriceerde 98,2% neg/pos-concordantie:* niet in de bron; aanleiding voor de
  accuratesse-discipline (#6).

**Signaleren, niet fabriceren.** Markeer gaten en inconsistenties expliciet in
plaats van gestructureerde velden met plausibel-ogende waarden te vullen.
Verrijking ("te-verrijken") is een aparte, gepoorte stap — geen onderdeel van extractie.

**Colofon is gezaghebbend.** Zaaknummer en Volgnummer komen uit het colofon, niet
uit de adviesbrief-header of het "Onze referentie"-veld — een terugkerende
extractiefout in eerdere fills.

---

## 5. Annotatiediscipline (waarom dit document bestaat)

De geannoteerde template dreigde te bezwijken onder zijn eigen commentaar. Vlak vóór
het afsplitsen was **66% van de v5-template commentaar** (2,6 regels annotatie per
regel veld), en elke versie voegde alleen tóé — nooit gesnoeid. Risico's van te veel:

- **Verdunning van aandacht.** Bij 66% proza kan noch de LLM noch de mens zien welke
  annotaties dragend zijn; de twee die een fill echt sturen verdrinken tussen de
  naslag-annotaties. De annotaties die in de praktijk wérkten waren kort, imperatief
  en aan één concrete fout gekoppeld — lengte doet het werk niet, imperatieve
  specificiteit wel.
- **Compoundend contradictierisico.** Meer proza = meer oppervlak waar annotaties
  met elkaar of met `CLAUDE.md` gaan schuren naarmate de template evolueert.
- **Twee doelgroepen in één bestand.** Extractie-sturing (voor de LLM) en
  institutioneel geheugen (changelogs, casus-verhalen, marker-herkomst) hebben
  verschillende lezers. Dit document huisvest het tweede; de lean template het eerste.

Werkafspraken om de lijn niet opnieuw te laten groeien:

1. **Splitsing vastgehouden.** Changelogs, redenaties en marker-herkomst blijven hier;
   de template houdt alleen `DEFINITION`/`SOURCE`/`PITFALL`/`HOW`.
2. **Snoeien is toegestaan.** Een annotatie die geen enkele fill meer verandert, mag
   weg. Diff-als-QA is het meetinstrument: vallen fills over meerdere PDF's samen op
   een veld, dan is de annotatie daar waarschijnlijk niet dragend.
3. **Gewicht zichtbaar houden.** `PITFALL`/`HOW` (dragend) verdient in de praktijk
   meer gewicht dan `DEFINITION`/`SOURCE` (naslag); overweeg die laatste te dunnen als
   fills niet degraderen.

**Openstaand meetpunt (meet-dan-besluit).** De lean template staat nu op 62%
commentaar / 2,2:1 — de winst zit in het weghalen van de meta-laag, niet van de
extractie-sturing. Verder snoeien (bv. `DEFINITION`/`SOURCE` inkorten) kan, maar
ruilt mogelijk fill-kwaliteit in voor bondigheid. Dat is een test, geen aanname:
draai een fill met en zonder die annotaties en kijk of de kwaliteit zakt.

**Zelfkritiek op v5.** Van de zes v5-toevoegingen zijn er vijf fout-gedreven (elk
repareert een waargenomen divergentie of fabricage). **#2 (diagnostiekkosten als
eigen cost-estimation) is eerder een modelleervoorkeur dan een waargenomen fout** —
twee fills kozen verschillend, maar geen van beide was fout. Bij een volgende
snoeironde is dat de eerste kandidaat om te heroverwegen.

---

## 6. Open vragen aan de eigenaar van het basistemplate (The Hyve)

*Vragen die de ZIN-kant niet zelf kan beslissen omdat ze het **basismodel** betreffen, niet de
ZIN-uitbreidingen. Bewust hier en niet in een changelog: een changelog is een foto van wat er veranderde,
terwijl deze vragen open blijven staan tot ze beantwoord zijn.*

### 6.1 — Waarvoor is `number-of-items` bedoeld? *(open, sinds v6.3)*

De annotatie stelt dat het verschil tussen het documenttotaal en het aantal gevolgde publicaties
"informatief" is — maar niet **voor wie** of **waarvoor**.

Binnen de signaleringspipeline leest **geen enkele consument** dit veld. Geverifieerd tegen
`pipeline/fair_reader.py`: dat leest `populations`, `interventions`, `intervention-groups`, `outcomes`,
`outcome-groups`, `picots`, `outcome-measurements`, `emsmps`, de IIC-sectie, `publications` en
`package-statement` — de secties `systematic-literature-reviews` en `literature-reference-lists` worden **in
het geheel niet ingelezen**. De feitelijke functie van het veld is daarmee die van een **invulcontrole**:
voorkomen dat de invuller "alle referenties in het document" verwart met "de referenties die wij volgen".

Dat is op zichzelf een legitieme functie, maar het is een **andere** dan de annotatie suggereert, en het roept
de vraag op of het veld in het basismodel een gebruiker heeft die wij niet kennen. Twee mogelijke uitkomsten:

- **Er ís een consument buiten deze pipeline** — dan hoort die in de annotatie genoemd te worden.
- **Die is er niet** — dan is "de kloof is informatief" een claim zonder adressaat, en kan de annotatie worden
  teruggebracht tot wat zij feitelijk doet.

Niet zelf beslissen: dit is een vraag over het basismodel.
