# -*- coding: utf-8 -*-
"""Generate impressum.html and datenschutz.html and their i18n entries.

Both legal pages follow the site's language switch, so every sentence lives in
this one table in all four languages. The HTML bodies are generated from the
same table, so a key can never drift away from its text.

    python tools/build-legal.py
"""
import io
import re
import sys

V = "v=20260924a"
LANGS = ("en", "de", "it", "ro")

# --------------------------------------------------------------------------- #
#  the strings: key -> (en, de, it, ro)
# --------------------------------------------------------------------------- #
S = {}

def add(key, en, de, it, ro):
    S[key] = (en, de, it, ro)

# ---------------------------------------------------------------- Impressum
add("imTitle",
    "Legal notice · Europe4strays", "Impressum · Europe4strays",
    "Note legali · Europe4strays", "Mențiuni legale · Europe4strays")
add("imH1", "Legal notice", "Impressum", "Note legali", "Mențiuni legale")
add("imLead",
    "Provider identification under the EU E-Commerce Directive and the national rules implementing it (§ 5 ECG Austria, § 5 DDG Germany, Legea 365/2002 Romania).",
    "Angaben zur Anbieterkennzeichnung gemäß der EU-E-Commerce-Richtlinie und den nationalen Umsetzungsvorschriften (§ 5 ECG Österreich, § 5 DDG Deutschland, Legea 365/2002 Rumänien).",
    "Informazioni sul fornitore ai sensi della direttiva UE sul commercio elettronico e delle norme nazionali di attuazione (§ 5 ECG Austria, § 5 DDG Germania, Legea 365/2002 Romania).",
    "Informații de identificare a furnizorului conform Directivei UE privind comerțul electronic și normelor naționale de punere în aplicare (§ 5 ECG Austria, § 5 DDG Germania, Legea 365/2002 România).")
add("imOrgT",
    "Site operator and responsible organisation", "Seitenbetreiber und verantwortliche Organisation",
    "Gestore del sito e organizzazione responsabile", "Operatorul site-ului și organizația responsabilă")
add("imForm",
    "Legal form: non-profit association under Romanian law (Asociație), NGO.",
    "Rechtsform: gemeinnütziger Verein nach rumänischem Recht (Asociație), NGO.",
    "Forma giuridica: associazione senza scopo di lucro di diritto romeno (Asociație), ONG.",
    "Formă juridică: asociație non-profit de drept român (Asociație), ONG.")
add("imRep",
    "Represented by its board and legal representatives: Mirela Mistodinis and Dragoș Mistodinis.",
    "Vertreten durch den Vorstand bzw. die gesetzlichen Vertreter: Mirela Mistodinis und Dragoș Mistodinis.",
    "Rappresentata dal consiglio direttivo e dai rappresentanti legali: Mirela Mistodinis e Dragoș Mistodinis.",
    "Reprezentată de consiliul director și de reprezentanții legali: Mirela Mistodinis și Dragoș Mistodinis.")
add("imContactT", "Contact", "Kontakt", "Contatti", "Contact")
add("imLblEmail", "Email:", "E-Mail:", "E-mail:", "E-mail:")
add("imLblWeb", "Website:", "Webseite:", "Sito web:", "Site web:")
add("imRegT", "Registration and identification", "Register und Identifikation",
    "Registrazione e identificazione", "Înregistrare și identificare")
add("imLblCourt", "Court of registration:", "Registrierungsgericht:",
    "Tribunale di registrazione:", "Instanța de înregistrare:")
add("imLblReg",
    "Register number (Registrul Asociațiilor și Fundațiilor):",
    "Registernummer (Registrul Asociațiilor și Fundațiilor):",
    "Numero di registro (Registrul Asociațiilor și Fundațiilor):",
    "Număr de înregistrare (Registrul Asociațiilor și Fundațiilor):")
add("imLblCif", "Romanian tax number (CIF):", "Rumänische Steuernummer (CIF):",
    "Codice fiscale romeno (CIF):", "Cod de înregistrare fiscală (CIF):")
add("imRespT", "Responsible for the content", "Verantwortlich für den Inhalt",
    "Responsabile dei contenuti", "Responsabil pentru conținut")
add("imResp", "Mirela Mistodinis, address as above.", "Mirela Mistodinis, Anschrift wie oben.",
    "Mirela Mistodinis, indirizzo come sopra.", "Mirela Mistodinis, adresa ca mai sus.")
add("imCredT", "Picture credits", "Bildnachweise", "Crediti fotografici", "Credite foto")
add("imCred",
    "The photographs come from Europe4strays and from our partner associations; each one is credited next to the picture.",
    "Die Fotos stammen von Europe4strays selbst sowie von den Partnervereinen und sind jeweils direkt an der Abbildung genannt.",
    "Le fotografie provengono da Europe4strays e dalle associazioni partner; ognuna è accreditata accanto all'immagine.",
    "Fotografiile provin de la Europe4strays și de la asociațiile partenere; fiecare este creditată lângă imagine.")
add("imCredSk", "Skayla Dog Rescue, Sweden", "Skayla Dog Rescue, Schweden",
    "Skayla Dog Rescue, Svezia", "Skayla Dog Rescue, Suedia")
add("imCredMap",
    "Map images: © OpenStreetMap contributors (ODbL)",
    "Kartenbilder: © OpenStreetMap-Mitwirkende (ODbL)",
    "Immagini delle mappe: © contributori di OpenStreetMap (ODbL)",
    "Imaginile hărților: © contribuitorii OpenStreetMap (ODbL)")
add("imCredFont",
    "Typefaces: Fraunces and Archivo under the SIL Open Font License, hosted on this server",
    "Schriften: Fraunces und Archivo, SIL Open Font License, auf diesem Server gehostet",
    "Caratteri: Fraunces e Archivo, SIL Open Font License, ospitati su questo server",
    "Fonturi: Fraunces și Archivo, SIL Open Font License, găzduite pe acest server")
add("imCredAi",
    "One short clip on the home page was animated from a real photograph using artificial intelligence. It is labelled as AI-animated at that point on the page.",
    "Ein kurzer Videoclip auf der Startseite wurde mit Hilfe künstlicher Intelligenz aus einem echten Foto animiert. Er ist an der entsprechenden Stelle als KI-animiert gekennzeichnet.",
    "Un breve video sulla home page è stato animato con l'intelligenza artificiale a partire da una foto reale. Nel punto corrispondente è contrassegnato come animazione IA.",
    "Un scurt videoclip de pe pagina principală a fost animat cu ajutorul inteligenței artificiale dintr-o fotografie reală. În locul respectiv este marcat ca animație IA.")
add("imLiabT", "Liability for content and links", "Haftung für Inhalte und Links",
    "Responsabilità per contenuti e link", "Răspunderea pentru conținut și linkuri")
add("imLiab",
    "We prepare the content of this site with care but cannot guarantee that it is complete or up to date. This site links to third-party websites, such as our partner associations and donation platforms; their content is the sole responsibility of those providers. No unlawful content was apparent when the links were placed. If we are made aware of a legal violation, we remove the link.",
    "Wir erstellen die Inhalte dieser Seite mit Sorgfalt, können aber keine Gewähr für ihre Vollständigkeit und Aktualität übernehmen. Diese Seite verlinkt auf Webseiten Dritter, etwa auf unsere Partnervereine und auf Spendenplattformen. Für deren Inhalte sind ausschließlich die jeweiligen Anbieter verantwortlich. Zum Zeitpunkt der Verlinkung waren dort keine rechtswidrigen Inhalte erkennbar. Werden wir auf Rechtsverletzungen aufmerksam gemacht, entfernen wir den betreffenden Link.",
    "Prepariamo i contenuti di questo sito con cura, ma non possiamo garantirne la completezza e l'attualità. Il sito rimanda a siti di terzi, come le nostre associazioni partner e le piattaforme di donazione; dei loro contenuti rispondono esclusivamente i rispettivi fornitori. Al momento dell'inserimento dei link non erano riconoscibili contenuti illeciti. Se veniamo informati di una violazione, rimuoviamo il link.",
    "Pregătim conținutul acestui site cu grijă, dar nu putem garanta că este complet și actual. Site-ul conține linkuri către site-uri terțe, precum asociațiile noastre partenere și platformele de donații; pentru conținutul lor răspund exclusiv furnizorii respectivi. La momentul creării linkurilor nu erau vizibile conținuturi ilegale. Dacă suntem informați despre o încălcare, eliminăm linkul.")
add("imPrivT", "Data protection", "Datenschutz", "Protezione dei dati", "Protecția datelor")
add("imPrivA",
    "How this site handles data is set out in the", "Wie diese Seite mit Daten umgeht, steht in der",
    "Come questo sito tratta i dati è spiegato nella", "Cum tratează acest site datele este explicat în")
add("imPrivB",
    "In short: this website sets no cookies and loads nothing from third-party servers when you open it.",
    "Kurz gesagt: Diese Webseite setzt keine Cookies und lädt beim Aufrufen nichts von Servern Dritter.",
    "In breve: questo sito non usa cookie e all'apertura non carica nulla da server di terzi.",
    "Pe scurt: acest site nu folosește cookie-uri și, la deschidere, nu încarcă nimic de pe servere terțe.")
add("imUpdated", "Last updated: September 2026", "Stand: September 2026",
    "Ultimo aggiornamento: settembre 2026", "Ultima actualizare: septembrie 2026")
add("lgAuth",
    "The German wording of this text is the authoritative one.",
    "Maßgeblich ist die deutsche Fassung dieses Textes.",
    "Fa fede la versione tedesca di questo testo.",
    "Versiunea în limba germană a acestui text este cea de referință.")

# ------------------------------------------------------------ Datenschutz
add("dpTitle", "Privacy policy · Europe4strays", "Datenschutzerklärung · Europe4strays",
    "Informativa sulla privacy · Europe4strays", "Politica de confidențialitate · Europe4strays")
add("dpH1", "Privacy policy", "Datenschutzerklärung",
    "Informativa sulla privacy", "Politica de confidențialitate")
add("dpLead",
    "Protecting your personal data matters to us. We treat personal data confidentially and in accordance with the law: above all the EU General Data Protection Regulation (GDPR), which applies directly in Romania, and the Romanian laws that complement it, Legea nr. 190/2018 and Legea nr. 506/2004.",
    "Der Schutz Ihrer persönlichen Daten ist uns ein wichtiges Anliegen. Wir behandeln personenbezogene Daten vertraulich und nach den gesetzlichen Vorschriften: vor allem nach der EU-Datenschutz-Grundverordnung (DSGVO), die in Rumänien unmittelbar gilt, und nach den rumänischen Gesetzen, die sie ergänzen, Legea Nr. 190/2018 und Legea Nr. 506/2004.",
    "La protezione dei vostri dati personali ci sta a cuore. Trattiamo i dati personali in modo riservato e secondo la legge: soprattutto il Regolamento generale UE sulla protezione dei dati (GDPR), direttamente applicabile in Romania, e le leggi romene che lo integrano, Legea nr. 190/2018 e Legea nr. 506/2004.",
    "Protecția datelor dumneavoastră personale este importantă pentru noi. Tratăm datele personale confidențial și în conformitate cu legea: în primul rând cu Regulamentul general UE privind protecția datelor (GDPR), aplicabil direct în România, și cu legile românești care îl completează, Legea nr. 190/2018 și Legea nr. 506/2004.")

add("dp1T", "1. The short version", "1. Das Wichtigste vorweg",
    "1. In breve", "1. Pe scurt")
add("dp1aT", "No cookies.", "Keine Cookies.", "Nessun cookie.", "Fără cookie-uri.")
add("dp1a",
    "This website sets no cookies. That is why there is no cookie banner.",
    "Diese Webseite setzt keine Cookies. Deshalb gibt es auch keinen Cookie-Banner.",
    "Questo sito non usa cookie. Per questo non c'è nessun banner sui cookie.",
    "Acest site nu folosește cookie-uri. De aceea nu există nici un banner pentru cookie-uri.")
add("dp1bT", "Nothing is loaded from third parties when you open a page.",
    "Beim Aufrufen wird nichts von Dritten geladen.",
    "All'apertura non viene caricato nulla da terzi.",
    "La deschidere nu se încarcă nimic de la terți.")
add("dp1b",
    "Fonts, images, maps and video thumbnails all sit on our own server. Opening a page or scrolling through it sends no request to Google or to anyone else.",
    "Schriften, Bilder, Karten und Vorschaubilder liegen alle auf unserem eigenen Server. Wenn Sie eine Seite öffnen oder durchscrollen, geht keine Anfrage an Google oder an andere Anbieter.",
    "Caratteri, immagini, mappe e anteprime dei video si trovano tutti sul nostro server. Aprire una pagina o scorrerla non invia alcuna richiesta a Google o ad altri fornitori.",
    "Fonturile, imaginile, hărțile și miniaturile video se află toate pe serverul nostru. Deschiderea sau derularea unei pagini nu trimite nicio cerere către Google sau alți furnizori.")
add("dp1cT", "No data collection.", "Keine Datensammlung.",
    "Nessuna raccolta di dati.", "Nicio colectare de date.")
add("dp1c",
    "On our own initiative we do not collect, store or process any personal data of visitors, so no names, addresses or email addresses. There is no contact form and no login on this site.",
    "Wir erheben, speichern und verarbeiten von uns aus keine personenbezogenen Daten der Besucher, also keine Namen, Adressen oder E-Mail-Adressen. Es gibt auf dieser Seite kein Kontaktformular und keine Anmeldung.",
    "Di nostra iniziativa non raccogliamo, conserviamo né trattiamo dati personali dei visitatori, quindi nessun nome, indirizzo o indirizzo e-mail. Su questo sito non c'è alcun modulo di contatto né alcuna registrazione.",
    "Din proprie iniţiativă nu colectăm, nu stocăm și nu prelucrăm date personale ale vizitatorilor, deci niciun nume, adresă sau adresă de e-mail. Pe acest site nu există formular de contact și nici cont de utilizator.")
add("dp1dT", "No tracking or analytics tools.", "Keine Tracking- oder Analysetools.",
    "Nessuno strumento di tracciamento o di analisi.", "Fără instrumente de urmărire sau analiză.")
add("dp1d",
    "We use no analytics software, and no Google Analytics either. We do not measure how often the site is visited, how long you stay or which region you come from.",
    "Wir setzen keine Analyse-Software ein, auch kein Google Analytics. Wir werten nicht aus, wie oft die Seite besucht wird, wie lange Sie bleiben oder aus welcher Region Sie kommen.",
    "Non utilizziamo software di analisi, nemmeno Google Analytics. Non rileviamo quante volte il sito viene visitato, quanto tempo restate o da quale regione arrivate.",
    "Nu folosim software de analiză, nici Google Analytics. Nu măsurăm cât de des este vizitat site-ul, cât timp rămâneți sau din ce regiune veniți.")
add("dp1eT", "No advertising, no profiling.", "Keine Werbung, kein Profiling.",
    "Nessuna pubblicità, nessuna profilazione.", "Fără publicitate, fără profilare.")
add("dp1e",
    "No personalised advertising is shown and no user profiles are created.",
    "Es wird keine personalisierte Werbung geschaltet und es werden keine Nutzerprofile erstellt.",
    "Non viene mostrata pubblicità personalizzata e non vengono creati profili utente.",
    "Nu se afișează publicitate personalizată și nu se creează profiluri de utilizator.")
add("dp1fT", "Donations stay anonymous to this site.", "Anonymität bei Spenden.",
    "Le donazioni restano anonime per questo sito.", "Donațiile rămân anonime pentru acest site.")
add("dp1f",
    "We do not record here who donated how much. The donation itself takes place entirely on the platform of the respective payment provider.",
    "Wir zeichnen auf dieser Webseite nicht auf, wer wie viel gespendet hat. Der eigentliche Spendenvorgang findet ausschließlich extern bei den jeweiligen Zahlungsdienstleistern statt.",
    "Su questo sito non registriamo chi ha donato quanto. La donazione avviene esclusivamente sulla piattaforma del rispettivo fornitore di pagamento.",
    "Pe acest site nu înregistrăm cine a donat cât. Donația în sine are loc exclusiv pe platforma furnizorului de plăți respectiv.")
add("dp1x",
    "Third parties only come into play if you click something yourself: an outgoing link or the play button of a video. Those cases are described one by one in sections 6 and 7.",
    "Daten Dritter kommen nur dann ins Spiel, wenn Sie selbst etwas anklicken: einen Link nach außen oder den Play-Knopf eines Videos. Diese Fälle sind unter Punkt 6 und 7 einzeln beschrieben.",
    "I terzi entrano in gioco solo se cliccate voi stessi qualcosa: un link verso l'esterno o il pulsante play di un video. Questi casi sono descritti uno per uno ai punti 6 e 7.",
    "Terții intră în joc doar dacă dați dumneavoastră clic pe ceva: un link către exterior sau butonul de play al unui videoclip. Aceste cazuri sunt descrise pe rând la punctele 6 și 7.")

add("dp2T", "2. Controller", "2. Verantwortliche Stelle",
    "2. Titolare del trattamento", "2. Operatorul de date")
add("dp2Rep",
    "Represented by Mirela Mistodinis and Dragoș Mistodinis. Further details in the",
    "Vertreten durch Mirela Mistodinis und Dragoș Mistodinis. Weitere Angaben im",
    "Rappresentata da Mirela Mistodinis e Dragoș Mistodinis. Ulteriori informazioni nelle",
    "Reprezentată de Mirela Mistodinis și Dragoș Mistodinis. Mai multe informații în")

add("dp3T", "3. Serving the website and server log files",
    "3. Bereitstellung der Webseite und Server-Logfiles",
    "3. Erogazione del sito e file di log del server",
    "3. Furnizarea site-ului și fișierele de jurnal ale serverului")
add("dp3a",
    "When you open our website, your browser has to connect to the server the site is stored on. In doing so it transmits technical information, which the host logs automatically:",
    "Wenn Sie unsere Webseite aufrufen, muss Ihr Browser eine Verbindung zum Server aufbauen, auf dem die Seite liegt. Dabei übermittelt er technische Informationen, die der Hoster automatisch protokolliert:",
    "Quando aprite il nostro sito, il browser deve collegarsi al server su cui si trova la pagina. Trasmette così informazioni tecniche che l'host registra automaticamente:",
    "Când deschideți site-ul nostru, browserul trebuie să se conecteze la serverul pe care se află pagina. În acest fel transmite informații tehnice, pe care gazda le înregistrează automat:")
add("dp3l1", "IP address of the accessing computer", "IP-Adresse des zugreifenden Rechners",
    "indirizzo IP del computer che accede", "adresa IP a computerului care accesează")
add("dp3l2", "browser type and version", "Browsertyp und Browserversion",
    "tipo e versione del browser", "tipul și versiunea browserului")
add("dp3l3", "operating system used", "verwendetes Betriebssystem",
    "sistema operativo utilizzato", "sistemul de operare utilizat")
add("dp3l4", "referrer URL, that is the page visited before",
    "Referrer-URL, also die zuvor besuchte Seite",
    "URL di provenienza, cioè la pagina visitata prima",
    "URL-ul de referință, adică pagina vizitată anterior")
add("dp3l5", "date and time of the server request", "Datum und Uhrzeit der Serveranfrage",
    "data e ora della richiesta al server", "data și ora cererii către server")
add("dp3l6", "name of the file requested", "Name der abgerufenen Datei",
    "nome del file richiesto", "numele fișierului solicitat")
add("dp3b",
    "This data is technically necessary in order to display the page to you at all, and it serves the stability and security of the server. It is not combined with other sources and it is not analysed. We ourselves are given no access to these logs, so we cannot trace anyone through them. The legal basis is Art. 6(1)(f) GDPR, our legitimate interest in operating the website correctly and securely.",
    "Diese Daten sind technisch notwendig, um Ihnen die Seite überhaupt anzeigen zu können, und dienen der Stabilität und Sicherheit des Servers. Sie werden nicht mit anderen Datenquellen zusammengeführt und nicht ausgewertet. Uns selbst werden diese Protokolle nicht zugänglich gemacht, wir können daraus also niemanden nachverfolgen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO, unser berechtigtes Interesse am fehlerfreien und sicheren Betrieb der Webseite.",
    "Questi dati sono tecnicamente necessari per potervi mostrare la pagina e servono alla stabilità e alla sicurezza del server. Non vengono combinati con altre fonti e non vengono analizzati. A noi stessi questi registri non sono accessibili, quindi non possiamo risalire a nessuno. La base giuridica è l'art. 6, par. 1, lett. f GDPR, il nostro legittimo interesse al funzionamento corretto e sicuro del sito.",
    "Aceste date sunt necesare din punct de vedere tehnic pentru a vă putea afișa pagina și servesc stabilității și securității serverului. Nu sunt combinate cu alte surse și nu sunt analizate. Nouă înșine aceste jurnale nu ne sunt accesibile, deci nu putem urmări pe nimeni prin ele. Baza juridică este art. 6 alin. 1 lit. f GDPR, interesul nostru legitim de a opera site-ul corect și în siguranță.")
add("dp3hT", "Host", "Hoster", "Host", "Gazdă")
add("dp3h",
    "The site runs as a static website on GitHub Pages. The provider is GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. GitHub processes the connection data listed above on our behalf in order to deliver the site and to fend off attacks. Data may be transferred to the USA; the transfer is based on the European Commission's adequacy decision for the EU-U.S. Data Privacy Framework, under which GitHub is certified. More in the",
    "Die Seite wird als statische Webseite bei GitHub Pages betrieben. Anbieter ist GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. GitHub verarbeitet die oben genannten Verbindungsdaten in unserem Auftrag, um die Seite auszuliefern und Angriffe abzuwehren. Dabei können Daten in die USA übermittelt werden; die Übermittlung stützt sich auf den Angemessenheitsbeschluss der Europäischen Kommission zum EU-U.S. Data Privacy Framework, unter dem GitHub zertifiziert ist. Näheres in der",
    "Il sito è ospitato come sito statico su GitHub Pages. Il fornitore è GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. GitHub tratta i dati di connessione sopra indicati per nostro conto, per erogare il sito e respingere attacchi. I dati possono essere trasferiti negli USA; il trasferimento si basa sulla decisione di adeguatezza della Commissione europea relativa all'EU-U.S. Data Privacy Framework, al quale GitHub è certificato. Maggiori dettagli nell'",
    "Site-ul este găzduit ca site static pe GitHub Pages. Furnizorul este GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, SUA. GitHub prelucrează datele de conexiune menționate mai sus în numele nostru, pentru a livra site-ul și pentru a respinge atacuri. Datele pot fi transferate în SUA; transferul se bazează pe decizia de adecvare a Comisiei Europene privind EU-U.S. Data Privacy Framework, la care GitHub este certificat. Mai multe detalii în")
add("dp3hLink", "GitHub privacy statement", "Datenschutzerklärung von GitHub",
    "informativa sulla privacy di GitHub", "politica de confidențialitate a GitHub")

add("dp4T", "4. Storage on your device", "4. Speicherung auf Ihrem Gerät",
    "4. Memorizzazione sul vostro dispositivo", "4. Stocarea pe dispozitivul dumneavoastră")
add("dp4a",
    "This website sets no cookies and embeds no advertising or counting pixels. Only a single item is stored on your device:",
    "Diese Webseite setzt keine Cookies und bindet keine Werbe- oder Zählpixel ein. Gespeichert wird auf Ihrem Gerät nur eine einzige Angabe:",
    "Questo sito non usa cookie e non incorpora pixel pubblicitari o di conteggio. Sul vostro dispositivo viene memorizzata una sola informazione:",
    "Acest site nu folosește cookie-uri și nu include pixeli publicitari sau de numărare. Pe dispozitivul dumneavoastră se stochează o singură informație:")
add("dp4lT", "Language choice", "Sprachauswahl", "Scelta della lingua", "Alegerea limbii")
add("dp4l",
    "(the entry e4s-lang in the browser's local storage). It holds nothing but which of the four languages you chose, for example „de“. It never leaves your device, contains no identifier and exists only so that the site opens in the same language next time.",
    "(Eintrag e4s-lang im lokalen Speicher des Browsers). Darin steht nur, welche der vier Sprachen Sie gewählt haben, zum Beispiel „de“. Diese Angabe verlässt Ihr Gerät nie, enthält keine Kennung und dient allein dazu, Ihnen die Seite beim nächsten Besuch in derselben Sprache zu zeigen.",
    "(la voce e4s-lang nella memoria locale del browser). Contiene soltanto quale delle quattro lingue avete scelto, per esempio „de“. Non lascia mai il vostro dispositivo, non contiene alcun identificativo e serve solo a mostrarvi il sito nella stessa lingua alla visita successiva.",
    "(intrarea e4s-lang în memoria locală a browserului). Conține doar care dintre cele patru limbi ați ales, de exemplu „de”. Nu părăsește niciodată dispozitivul dumneavoastră, nu conține niciun identificator și există doar pentru ca site-ul să se deschidă în aceeași limbă la următoarea vizită.")
add("dp4b",
    "This is storage strictly necessary for a service you explicitly requested and therefore requires no consent: under Art. 5(3) of the EU ePrivacy Directive 2002/58/EC, which Romania implements in Art. 4(5) and (6) of Legea nr. 506/2004, and likewise under § 25(2) no. 2 TDDDG for visitors from Germany and § 165(3) TKG 2021 for visitors from Austria. You can delete the entry at any time by clearing this site's data in your browser.",
    "Das ist eine technisch erforderliche Speicherung für einen von Ihnen ausdrücklich gewünschten Dienst und deshalb nicht einwilligungspflichtig: nach Art. 5 Abs. 3 der EU-ePrivacy-Richtlinie 2002/58/EG, in Rumänien umgesetzt in Art. 4 Abs. 5 und 6 Legea Nr. 506/2004, und ebenso nach § 25 Abs. 2 Nr. 2 TDDDG für Besucher aus Deutschland und § 165 Abs. 3 TKG 2021 für Besucher aus Österreich. Sie können den Eintrag jederzeit löschen, indem Sie in Ihrem Browser die Websitedaten für diese Seite entfernen.",
    "Si tratta di una memorizzazione tecnicamente necessaria per un servizio da voi espressamente richiesto e pertanto non richiede consenso: ai sensi dell'art. 5, par. 3 della direttiva UE ePrivacy 2002/58/CE, recepita in Romania dall'art. 4, commi 5 e 6 della Legea nr. 506/2004, e allo stesso modo del § 25, comma 2, n. 2 TDDDG per i visitatori dalla Germania e del § 165, comma 3 TKG 2021 per quelli dall'Austria. Potete cancellare la voce in qualsiasi momento eliminando i dati del sito nel vostro browser.",
    "Este o stocare strict necesară pentru un serviciu solicitat expres de dumneavoastră și, prin urmare, nu necesită consimțământ: conform art. 5 alin. (3) din Directiva UE ePrivacy 2002/58/CE, transpusă în România prin art. 4 alin. (5) și (6) din Legea nr. 506/2004, și la fel conform § 25 alin. 2 nr. 2 TDDDG pentru vizitatorii din Germania și § 165 alin. 3 TKG 2021 pentru cei din Austria. Puteți șterge intrarea oricând, eliminând datele acestui site din browserul dumneavoastră.")

add("dp5T", "5. Fonts and maps are hosted by us", "5. Schriften und Karten liegen bei uns",
    "5. Caratteri e mappe sono ospitati da noi", "5. Fonturile și hărțile sunt găzduite de noi")
add("dp5aT", "Fonts.", "Schriften.", "Caratteri.", "Fonturi.")
add("dp5a",
    "The typefaces Fraunces and Archivo are loaded from our own server. No connection to Google Fonts is made and your IP address is not transmitted to Google.",
    "Die verwendeten Schriften Fraunces und Archivo werden von unserem eigenen Server geladen. Es wird keine Verbindung zu Google Fonts aufgebaut und Ihre IP-Adresse wird dabei nicht an Google übermittelt.",
    "I caratteri Fraunces e Archivo vengono caricati dal nostro server. Non viene stabilita alcuna connessione a Google Fonts e il vostro indirizzo IP non viene trasmesso a Google.",
    "Fonturile Fraunces și Archivo sunt încărcate de pe serverul nostru. Nu se stabilește nicio conexiune cu Google Fonts și adresa dumneavoastră IP nu este transmisă către Google.")
add("dp5bT", "Maps.", "Karten.", "Mappe.", "Hărți.")
add("dp5b",
    "The two maps showing our location are still images stored on our server, rendered from OpenStreetMap material (© OpenStreetMap contributors). Displaying them loads nothing. Only when you click a map does Google Maps open in a new window, and from that moment the notes in section 6 apply.",
    "Die beiden Karten, die unseren Standort zeigen, sind unbewegliche Bilder, die auf unserem Server liegen. Sie stammen aus dem Kartenmaterial von OpenStreetMap (© OpenStreetMap-Mitwirkende). Beim Anzeigen wird nichts nachgeladen. Erst wenn Sie auf eine Karte klicken, öffnet sich Google Maps in einem neuen Fenster, und ab diesem Moment gelten die Hinweise unter Punkt 6.",
    "Le due mappe che mostrano la nostra sede sono immagini fisse che si trovano sul nostro server, ricavate dal materiale cartografico di OpenStreetMap (© contributori di OpenStreetMap). La loro visualizzazione non carica nulla. Solo se cliccate su una mappa si apre Google Maps in una nuova finestra e da quel momento valgono le indicazioni del punto 6.",
    "Cele două hărți care arată sediul nostru sunt imagini statice aflate pe serverul nostru, realizate din materialul cartografic OpenStreetMap (© contribuitorii OpenStreetMap). Afișarea lor nu încarcă nimic. Doar dacă dați clic pe o hartă se deschide Google Maps într-o fereastră nouă și din acel moment se aplică indicațiile de la punctul 6.")

add("dp6T", "6. External links to donation platforms, partners and social networks",
    "6. Externe Links zu Spendenplattformen, Partnern und sozialen Netzwerken",
    "6. Link esterni a piattaforme di donazione, partner e social network",
    "6. Linkuri externe către platforme de donații, parteneri și rețele sociale")
add("dp6a",
    "Our website links to external platforms and to the websites of our partner associations. As long as you do not click such a link, nothing is transmitted. If you click it, you leave our website and data is transferred to that provider, at least your IP address and the information that you came from our site. We have no influence over that.",
    "Unsere Webseite verlinkt auf externe Plattformen und auf die Seiten unserer Partnervereine. Solange Sie einen solchen Link nicht anklicken, wird nichts übertragen. Wenn Sie ihn anklicken, verlassen Sie unsere Webseite, und es werden Daten an den jeweiligen Anbieter übertragen, mindestens Ihre IP-Adresse und die Information, dass Sie von unserer Seite kommen. Darauf haben wir keinen Einfluss.",
    "Il nostro sito rimanda a piattaforme esterne e ai siti delle nostre associazioni partner. Fino a quando non cliccate su un link di questo tipo, non viene trasmesso nulla. Se lo cliccate, lasciate il nostro sito e vengono trasferiti dati al rispettivo fornitore, almeno il vostro indirizzo IP e l'informazione che provenite dal nostro sito. Su questo non abbiamo alcuna influenza.",
    "Site-ul nostru conține linkuri către platforme externe și către site-urile asociațiilor noastre partenere. Atât timp cât nu dați clic pe un astfel de link, nu se transmite nimic. Dacă dați clic, părăsiți site-ul nostru și se transferă date către furnizorul respectiv, cel puțin adresa dumneavoastră IP și informația că veniți de pe site-ul nostru. Asupra acestui lucru nu avem nicio influență.")
add("dp6bT", "a) PayPal", "a) PayPal", "a) PayPal", "a) PayPal")
add("dp6b",
    "Donation link. Provider: PayPal (Europe) S.à r.l. et Cie, S.C.A., 22–24 Boulevard Royal, L-2449 Luxembourg. PayPal processes your payment data, your name and your IP address under its own rules in order to carry out the donation.",
    "Spendenlink. Anbieter: PayPal (Europe) S.à r.l. et Cie, S.C.A., 22–24 Boulevard Royal, L-2449 Luxemburg. PayPal verarbeitet Ihre Zahlungsdaten, Ihren Namen und Ihre IP-Adresse nach den eigenen Richtlinien, um die Spende durchzuführen.",
    "Link per le donazioni. Fornitore: PayPal (Europe) S.à r.l. et Cie, S.C.A., 22–24 Boulevard Royal, L-2449 Lussemburgo. PayPal tratta i vostri dati di pagamento, il nome e l'indirizzo IP secondo le proprie regole per eseguire la donazione.",
    "Link de donație. Furnizor: PayPal (Europe) S.à r.l. et Cie, S.C.A., 22–24 Boulevard Royal, L-2449 Luxemburg. PayPal prelucrează datele dumneavoastră de plată, numele și adresa IP conform propriilor reguli, pentru a efectua donația.")
add("dp6cT", "b) Teaming", "b) Teaming", "b) Teaming", "b) Teaming")
add("dp6c",
    "Platform for regular micro-donations of 1 € a month. Provider: Fundación Teaming, Calle de Calabria 149, Entresuelo 1ª, 08015 Barcelona, Spain. Payment handling and the donor account are their own responsibility.",
    "Plattform für regelmäßige Kleinstspenden von 1 € im Monat. Anbieter: Fundación Teaming, Calle de Calabria 149, Entresuelo 1ª, 08015 Barcelona, Spanien. Zahlungsabwicklung und Spenderkonto liegen dort in eigener Verantwortung.",
    "Piattaforma per micro-donazioni regolari di 1 € al mese. Fornitore: Fundación Teaming, Calle de Calabria 149, Entresuelo 1ª, 08015 Barcellona, Spagna. La gestione dei pagamenti e il conto del donatore sono di loro responsabilità.",
    "Platformă pentru micro-donații regulate de 1 € pe lună. Furnizor: Fundación Teaming, Calle de Calabria 149, Entresuelo 1ª, 08015 Barcelona, Spania. Procesarea plăților și contul de donator sunt în responsabilitatea lor.")
add("dp6dT", "c) Amazon wishlist", "c) Amazon-Wunschliste",
    "c) Lista dei desideri Amazon", "c) Lista de dorințe Amazon")
add("dp6d",
    "For donations in kind. Provider: Amazon Europe Core S.à r.l., 38 avenue John F. Kennedy, L-1855 Luxembourg.",
    "Für Sachspenden. Anbieter: Amazon Europe Core S.à r.l., 38 avenue John F. Kennedy, L-1855 Luxemburg.",
    "Per donazioni in natura. Fornitore: Amazon Europe Core S.à r.l., 38 avenue John F. Kennedy, L-1855 Lussemburgo.",
    "Pentru donații în natură. Furnizor: Amazon Europe Core S.à r.l., 38 avenue John F. Kennedy, L-1855 Luxemburg.")
add("dp6eT", "d) Facebook and Instagram", "d) Facebook und Instagram",
    "d) Facebook e Instagram", "d) Facebook și Instagram")
add("dp6e",
    "We link to our own pages and to our partners' pages on Facebook and Instagram, and the „Write to Mirela“ button leads to our Facebook page. Provider: Meta Platforms Ireland Limited, 4 Grand Canal Square, Grand Canal Harbour, Dublin 2, Ireland. These are plain text links, not embedded content and not like buttons: nothing is transmitted to Meta before you click. If you are signed in to Meta, your visit there can be linked to your account.",
    "Wir verlinken auf unsere eigenen Seiten und auf die Seiten unserer Partner bei Facebook und Instagram, und der Knopf „Write to Mirela“ führt zu unserer Facebook-Seite. Anbieter: Meta Platforms Ireland Limited, 4 Grand Canal Square, Grand Canal Harbour, Dublin 2, Irland. Es sind reine Textlinks, keine eingebetteten Inhalte und keine Like-Buttons: Vor dem Klick wird nichts an Meta übertragen. Wenn Sie bei Meta angemeldet sind, kann Ihr Besuch dort Ihrem Konto zugeordnet werden.",
    "Rimandiamo alle nostre pagine e a quelle dei nostri partner su Facebook e Instagram, e il pulsante „Write to Mirela“ porta alla nostra pagina Facebook. Fornitore: Meta Platforms Ireland Limited, 4 Grand Canal Square, Grand Canal Harbour, Dublino 2, Irlanda. Sono semplici link testuali, non contenuti incorporati e non pulsanti „mi piace“: prima del clic non viene trasmesso nulla a Meta. Se siete connessi a Meta, la vostra visita può essere associata al vostro account.",
    "Facem legătura cu paginile noastre și cu cele ale partenerilor pe Facebook și Instagram, iar butonul „Write to Mirela” duce la pagina noastră de Facebook. Furnizor: Meta Platforms Ireland Limited, 4 Grand Canal Square, Grand Canal Harbour, Dublin 2, Irlanda. Sunt simple linkuri text, nu conținut încorporat și nici butoane de like: înainte de clic nu se transmite nimic către Meta. Dacă sunteți conectat la Meta, vizita dumneavoastră poate fi asociată contului.")
add("dp6fT", "e) Partner associations in Germany and Sweden",
    "e) Partnervereine in Deutschland und Schweden",
    "e) Associazioni partner in Germania e Svezia",
    "e) Asociații partenere în Germania și Suedia")
add("dp6f",
    "For questions about adoption we link to the websites of our independent partner associations Tierschutzgruppe Herzensmenschen e. V. (Germany) and Skayla Dog Rescue (Sweden). As soon as you visit those sites, their own privacy policies apply.",
    "Bei Fragen zur Adoption verlinken wir auf die Webseiten unserer selbstständigen Partnervereine Tierschutzgruppe Herzensmenschen e. V. (Deutschland) und Skayla Dog Rescue (Schweden). Sobald Sie diese Seiten besuchen, gelten die Datenschutzerklärungen der jeweiligen Vereine.",
    "Per le domande sull'adozione rimandiamo ai siti delle nostre associazioni partner indipendenti Tierschutzgruppe Herzensmenschen e. V. (Germania) e Skayla Dog Rescue (Svezia). Appena visitate quei siti, valgono le loro informative sulla privacy.",
    "Pentru întrebări despre adopție facem legătura cu site-urile asociațiilor noastre partenere independente Tierschutzgruppe Herzensmenschen e. V. (Germania) și Skayla Dog Rescue (Suedia). Imediat ce vizitați acele site-uri, se aplică politicile lor de confidențialitate.")
add("dp6gT", "f) Hunderunde", "f) Hunderunde", "f) Hunderunde", "f) Hunderunde")
add("dp6g",
    "We link to Hunderunde, who support us through the sale of dog food and accessories within animal welfare projects. They process your data when you visit their online shop on their own responsibility.",
    "Wir verlinken auf Hunderunde, die uns durch den Verkauf von Hundefutter und Zubehör im Rahmen von Tierschutzprojekten unterstützen. Sie verarbeiten Ihre Daten beim Besuch des Onlineshops in eigener Verantwortung.",
    "Rimandiamo a Hunderunde, che ci sostengono con la vendita di cibo e accessori per cani nell'ambito di progetti di protezione animale. Trattano i vostri dati durante la visita al loro negozio online sotto la propria responsabilità.",
    "Facem legătura cu Hunderunde, care ne sprijină prin vânzarea de hrană și accesorii pentru câini în cadrul unor proiecte de protecție a animalelor. Aceștia prelucrează datele dumneavoastră la vizitarea magazinului online pe propria răspundere.")
add("dp6hT", "g) Google Maps and OpenStreetMap", "g) Google Maps und OpenStreetMap",
    "g) Google Maps e OpenStreetMap", "g) Google Maps și OpenStreetMap")
add("dp6h",
    "Clicking a map opens Google Maps, clicking the map credit opens openstreetmap.org. Providers: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland, and OpenStreetMap Foundation, St John's Innovation Centre, Cowley Road, Cambridge CB4 0WS, United Kingdom.",
    "Ein Klick auf eine Karte öffnet Google Maps, ein Klick auf den Kartenhinweis öffnet openstreetmap.org. Anbieter: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland, bzw. OpenStreetMap Foundation, St John's Innovation Centre, Cowley Road, Cambridge CB4 0WS, Vereinigtes Königreich.",
    "Un clic su una mappa apre Google Maps, un clic sull'attribuzione apre openstreetmap.org. Fornitori: Google Ireland Limited, Gordon House, Barrow Street, Dublino 4, Irlanda, e OpenStreetMap Foundation, St John's Innovation Centre, Cowley Road, Cambridge CB4 0WS, Regno Unito.",
    "Un clic pe o hartă deschide Google Maps, un clic pe atribuirea hărții deschide openstreetmap.org. Furnizori: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irlanda, respectiv OpenStreetMap Foundation, St John's Innovation Centre, Cowley Road, Cambridge CB4 0WS, Regatul Unit.")

add("dp7T", "7. Videos: YouTube only after your click",
    "7. Videos: YouTube erst nach Ihrem Klick",
    "7. Video: YouTube solo dopo il vostro clic",
    "7. Videoclipuri: YouTube abia după clicul dumneavoastră")
add("dp7a",
    "The home page and the blog embed videos that are hosted on YouTube. At first we show only a thumbnail, which sits on our own server. The YouTube player is loaded only when you press the play button. Until then YouTube learns nothing about your visit.",
    "Auf der Startseite und im Blog sind Videos eingebunden, die bei YouTube liegen. Wir zeigen zunächst nur ein Vorschaubild, das auf unserem eigenen Server liegt. Erst wenn Sie auf den Play-Knopf drücken, wird der YouTube-Player geladen. Bis dahin erfährt YouTube nichts von Ihrem Besuch.",
    "Sulla home page e nel blog sono incorporati video ospitati su YouTube. Inizialmente mostriamo solo un'anteprima, che si trova sul nostro server. Il player di YouTube viene caricato solo quando premete il pulsante play. Fino a quel momento YouTube non sa nulla della vostra visita.",
    "Pe pagina principală și în blog sunt încorporate videoclipuri găzduite pe YouTube. La început afișăm doar o miniatură, care se află pe serverul nostru. Player-ul YouTube este încărcat abia când apăsați butonul de play. Până atunci YouTube nu află nimic despre vizita dumneavoastră.")
add("dp7b",
    "As soon as you play, your browser connects to YouTube. Your IP address and the information about which video you are watching are transmitted, and YouTube can store cookies and similar identifiers on your device. If you are signed in to Google, YouTube can link the view to your account. We use the youtube-nocookie.com variant, which sets fewer identifiers but does not prevent the connection itself.",
    "Sobald Sie abspielen, baut Ihr Browser eine Verbindung zu YouTube auf. Dabei werden Ihre IP-Adresse und die Information, welches Video Sie ansehen, übertragen, und YouTube kann Cookies und ähnliche Kennungen auf Ihrem Gerät speichern. Wenn Sie bei Google angemeldet sind, kann YouTube das Ansehen Ihrem Konto zuordnen. Wir verwenden die Variante youtube-nocookie.com, die weniger Kennungen setzt, die Verbindung selbst aber nicht verhindert.",
    "Appena avviate la riproduzione, il browser si collega a YouTube. Vengono trasmessi il vostro indirizzo IP e l'informazione su quale video state guardando, e YouTube può memorizzare cookie e identificativi simili sul vostro dispositivo. Se siete connessi a Google, YouTube può associare la visione al vostro account. Usiamo la variante youtube-nocookie.com, che imposta meno identificativi ma non impedisce la connessione.",
    "Imediat ce porniți redarea, browserul se conectează la YouTube. Se transmit adresa dumneavoastră IP și informația despre videoclipul pe care îl urmăriți, iar YouTube poate stoca cookie-uri și identificatori similari pe dispozitivul dumneavoastră. Dacă sunteți conectat la Google, YouTube poate asocia vizionarea contului dumneavoastră. Folosim varianta youtube-nocookie.com, care setează mai puțini identificatori, dar nu împiedică conexiunea în sine.")
add("dp7c",
    "Provider: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland; parent company Google LLC, USA, certified under the EU-U.S. Data Privacy Framework. The legal basis is your consent under Art. 6(1)(a) GDPR, which you give by clicking the play button. You can withdraw that consent at any time by reloading the page and not playing the video. More in the",
    "Anbieter: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland; Muttergesellschaft Google LLC, USA, zertifiziert unter dem EU-U.S. Data Privacy Framework. Rechtsgrundlage ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO, die Sie mit dem Klick auf den Play-Knopf erteilen. Sie können diese Einwilligung jederzeit widerrufen, indem Sie die Seite neu laden und das Video nicht abspielen. Näheres in der",
    "Fornitore: Google Ireland Limited, Gordon House, Barrow Street, Dublino 4, Irlanda; società madre Google LLC, USA, certificata secondo l'EU-U.S. Data Privacy Framework. La base giuridica è il vostro consenso ai sensi dell'art. 6, par. 1, lett. a GDPR, che date cliccando sul pulsante play. Potete revocarlo in qualsiasi momento ricaricando la pagina e non riproducendo il video. Maggiori dettagli nell'",
    "Furnizor: Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irlanda; societatea-mamă Google LLC, SUA, certificată conform EU-U.S. Data Privacy Framework. Baza juridică este consimțământul dumneavoastră conform art. 6 alin. 1 lit. a GDPR, pe care îl acordați prin clic pe butonul de play. Îl puteți retrage oricând reîncărcând pagina și nedând redare videoclipului. Mai multe detalii în")
add("dpPolPl", "Privacy policy:", "Datenschutzerklärung:",
    "Informativa sulla privacy:", "Politica de confidențialitate:")
add("dp7Link", "Google privacy policy", "Datenschutzerklärung von Google",
    "informativa sulla privacy di Google", "politica de confidențialitate a Google")

add("dp8T", "8. If you write to us", "8. Wenn Sie uns schreiben",
    "8. Se ci scrivete", "8. Dacă ne scrieți")
add("dp8a",
    "This website has no contact form. If you email us, we process your address and the content of your message in order to reply to you. The legal basis is Art. 6(1)(b) and (f) GDPR. We delete such messages once they are no longer needed, unless retention duties stand in the way.",
    "Diese Webseite hat kein Kontaktformular. Wenn Sie uns per E-Mail schreiben, verarbeiten wir Ihre Adresse und den Inhalt Ihrer Nachricht, um Ihnen zu antworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b und lit. f DSGVO. Wir löschen solche Nachrichten, sobald sie nicht mehr gebraucht werden, sofern keine Aufbewahrungspflichten entgegenstehen.",
    "Questo sito non ha un modulo di contatto. Se ci scrivete per e-mail, trattiamo il vostro indirizzo e il contenuto del messaggio per rispondervi. La base giuridica è l'art. 6, par. 1, lett. b e f GDPR. Cancelliamo tali messaggi appena non servono più, salvo obblighi di conservazione.",
    "Acest site nu are formular de contact. Dacă ne scrieți pe e-mail, prelucrăm adresa dumneavoastră și conținutul mesajului pentru a vă răspunde. Baza juridică este art. 6 alin. 1 lit. b și f GDPR. Ștergem astfel de mesaje imediat ce nu mai sunt necesare, dacă nu există obligații de păstrare.")
add("dp8b",
    "Our mailbox runs on Gmail, so incoming messages are processed on Google servers (Google Ireland Limited, Dublin, Ireland). If you write to us through Facebook Messenger, Meta Platforms Ireland Limited processes the message.",
    "Unser E-Mail-Postfach wird bei Gmail geführt. Eingehende Nachrichten werden daher auf Servern von Google verarbeitet (Google Ireland Limited, Dublin, Irland). Wenn Sie uns über Facebook Messenger schreiben, verarbeitet Meta Platforms Ireland Limited die Nachricht.",
    "La nostra casella di posta è su Gmail, quindi i messaggi in arrivo vengono trattati su server di Google (Google Ireland Limited, Dublino, Irlanda). Se ci scrivete tramite Facebook Messenger, il messaggio è trattato da Meta Platforms Ireland Limited.",
    "Cutia noastră de e-mail este la Gmail, așa că mesajele primite sunt prelucrate pe servere Google (Google Ireland Limited, Dublin, Irlanda). Dacă ne scrieți prin Facebook Messenger, mesajul este prelucrat de Meta Platforms Ireland Limited.")

add("dp9T", "9. Donations by bank transfer", "9. Spenden per Banküberweisung",
    "9. Donazioni con bonifico bancario", "9. Donații prin transfer bancar")
add("dp9a",
    "Our bank details are shown on the website. If you make a transfer, our bank passes us your name, your IBAN and the payment reference. We use this to allocate the donation, to reply to you if you wish, and to meet our bookkeeping obligations. The legal basis is Art. 6(1)(b) and (c) GDPR together with the Romanian retention periods for accounting records.",
    "Auf der Webseite sind unsere Bankverbindungen angegeben. Wenn Sie überweisen, erhalten wir über unsere Bank Ihren Namen, Ihre IBAN und den Verwendungszweck. Wir verwenden diese Angaben, um die Spende zuzuordnen, um Ihnen auf Wunsch zu antworten und um unsere Buchführungspflichten zu erfüllen. Rechtsgrundlage sind Art. 6 Abs. 1 lit. b und lit. c DSGVO in Verbindung mit den rumänischen Aufbewahrungsfristen für Buchhaltungsunterlagen.",
    "Le nostre coordinate bancarie sono indicate sul sito. Se effettuate un bonifico, la nostra banca ci trasmette il vostro nome, l'IBAN e la causale. Usiamo questi dati per attribuire la donazione, per rispondervi se lo desiderate e per adempiere agli obblighi contabili. La base giuridica è l'art. 6, par. 1, lett. b e c GDPR in combinazione con i termini di conservazione romeni per i documenti contabili.",
    "Datele noastre bancare sunt indicate pe site. Dacă faceți un transfer, banca noastră ne transmite numele dumneavoastră, IBAN-ul și detaliile plății. Folosim aceste date pentru a aloca donația, pentru a vă răspunde la cerere și pentru a îndeplini obligațiile contabile. Baza juridică este art. 6 alin. 1 lit. b și c GDPR, coroborat cu termenele românești de păstrare a documentelor contabile.")

add("dp10T", "10. Your rights", "10. Ihre Rechte", "10. I vostri diritti", "10. Drepturile dumneavoastră")
add("dp10a",
    "You have the right at any time to free information about the data stored about you, its origin, its recipients and the purpose of the processing (Art. 15 GDPR), as well as the right to rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), data portability (Art. 20) and objection (Art. 21). Consent once given can be withdrawn at any time under Art. 7(3) GDPR.",
    "Sie haben jederzeit das Recht auf unentgeltliche Auskunft über die zu Ihrer Person gespeicherten Daten, ihre Herkunft, ihre Empfänger und den Zweck der Verarbeitung (Art. 15 DSGVO) sowie das Recht auf Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21). Eine erteilte Einwilligung können Sie nach Art. 7 Abs. 3 DSGVO jederzeit widerrufen.",
    "Avete in qualsiasi momento diritto a informazioni gratuite sui dati memorizzati su di voi, sulla loro origine, sui destinatari e sulla finalità del trattamento (art. 15 GDPR), nonché diritto alla rettifica (art. 16), alla cancellazione (art. 17), alla limitazione del trattamento (art. 18), alla portabilità dei dati (art. 20) e di opposizione (art. 21). Un consenso dato può essere revocato in qualsiasi momento ai sensi dell'art. 7, par. 3 GDPR.",
    "Aveți oricând dreptul la informare gratuită despre datele stocate referitoare la dumneavoastră, originea lor, destinatarii și scopul prelucrării (art. 15 GDPR), precum și dreptul la rectificare (art. 16), ștergere (art. 17), restricționarea prelucrării (art. 18), portabilitatea datelor (art. 20) și opoziție (art. 21). Un consimțământ acordat poate fi retras oricând conform art. 7 alin. 3 GDPR.")
add("dp10b",
    "Because we neither collect nor store any data when you merely visit the site, a request for information will usually return „no data held“, unless you have written to us or donated.",
    "Da wir beim reinen Besuch der Seite keine Daten von Ihnen erheben oder speichern, wird eine Auskunftsanfrage bei uns in der Regel „keine Daten vorhanden“ ergeben, sofern Sie uns nicht geschrieben oder gespendet haben.",
    "Poiché con la semplice visita del sito non raccogliamo né conserviamo dati, una richiesta di accesso darà di norma come risultato „nessun dato presente“, a meno che non ci abbiate scritto o fatto una donazione.",
    "Deoarece la simpla vizitare a site-ului nu colectăm și nu stocăm date, o cerere de informare va avea în general rezultatul „nu există date”, cu excepția cazului în care ne-ați scris sau ați donat.")
add("dp10c",
    "Please address all such matters to the email address above. You may also complain to a data protection supervisory authority. The authority responsible for us is the Romanian ANSPDCP, B-dul G-ral. Gheorghe Magheru 28–30, 010336 Bucureşti, Romania. You may equally contact the authority where you live.",
    "Wenden Sie sich für alle diese Anliegen bitte an die oben genannte E-Mail-Adresse. Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren. Für uns zuständig ist die rumänische Behörde ANSPDCP, B-dul G-ral. Gheorghe Magheru 28–30, 010336 Bucureşti, România. Sie können sich auch an die Aufsichtsbehörde Ihres Wohnsitzes wenden.",
    "Per tutte queste questioni rivolgetevi all'indirizzo e-mail indicato sopra. Potete inoltre presentare reclamo a un'autorità di controllo per la protezione dei dati. Per noi è competente l'autorità romena ANSPDCP, B-dul G-ral. Gheorghe Magheru 28–30, 010336 Bucureşti, Romania. Potete anche rivolgervi all'autorità del vostro luogo di residenza.",
    "Pentru toate aceste solicitări vă rugăm să folosiți adresa de e-mail indicată mai sus. În plus, puteți depune o plângere la o autoritate de supraveghere a protecției datelor. Pentru noi este competentă autoritatea română ANSPDCP, B-dul G-ral. Gheorghe Magheru 28–30, 010336 Bucureşti, România. Vă puteți adresa și autorității de la domiciliul dumneavoastră.")
add("dpUpdated",
    "Last updated: September 2026. If anything on the website changes that affects data, we update this policy.",
    "Stand: September 2026. Wenn sich an der Webseite etwas ändert, das Daten betrifft, aktualisieren wir diese Erklärung.",
    "Ultimo aggiornamento: settembre 2026. Se cambia qualcosa nel sito che riguarda i dati, aggiorniamo questa informativa.",
    "Ultima actualizare: septembrie 2026. Dacă se schimbă ceva pe site care privește datele, actualizăm această politică.")

# --------------------------------------------------------------------------- #
#  page bodies, generated from the same table
# --------------------------------------------------------------------------- #
def esc(v):
    return v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# keys that already live in i18n.js (shared with the footer links)
EXT = {"navImprint": "Legal notice", "navPrivacy": "Privacy policy"}

def txt(k):
    if k in S:
        return esc(S[k][0])
    if k in EXT:
        return esc(EXT[k])
    sys.exit("unknown key: " + k)

def h(tag, k, cls=None):
    c = ' class="%s"' % cls if cls else ""
    return '    <%s%s data-i18n="%s">%s</%s>' % (tag, c, k, txt(k), tag)

def ul(items):
    out = ['    <ul>']
    for it in items:
        if isinstance(it, tuple):
            out.append('      <li><strong data-i18n="%s">%s</strong> <span data-i18n="%s">%s</span></li>'
                       % (it[0], txt(it[0]), it[1], txt(it[1])))
        else:
            out.append('      <li data-i18n="%s">%s</li>' % (it, txt(it)))
    out.append('    </ul>')
    return "\n".join(out)

def labelled(items):
    """<li><span data-i18n=label>Label:</span> value</li>"""
    out = ['    <ul>']
    for lab, val in items:
        out.append('      <li><span data-i18n="%s">%s</span> %s</li>' % (lab, txt(lab), val))
    out.append('    </ul>')
    return "\n".join(out)

def plink(k, href, klink, tail=".", extra=""):
    return ('    <p><span data-i18n="%s">%s</span> <a href="%s"%s data-i18n="%s">%s</a>%s</p>'
            % (k, txt(k), href, extra, klink, txt(klink), tail))

def pol(*links):
    """a 'Privacy policy: <a>Provider</a> · <a>Provider</a>' line under a provider"""
    a = " · ".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, n) for n, u in links)
    return '    <p class="lg-pol"><span data-i18n="dpPolPl">%s</span> %s</p>' % (txt("dpPolPl"), a)

def para_pair(kt, k):
    return ('    <p><strong data-i18n="%s">%s</strong> <span data-i18n="%s">%s</span></p>'
            % (kt, txt(kt), k, txt(k)))

ADDR_DE = ('      <p class="lg-addr">\n'
           '        <strong>Asociația pentru Protecția Animalelor „Europe4Strays”</strong><br>\n'
           '        Strada Mareșal Constantin Prezan nr. 10<br>\n'
           '        627210 Movilița, Județul Vrancea<br>\n'
           '        România\n'
           '      </p>')

IMPRESSUM_BODY = "\n".join([
    h("h2", "imOrgT"),
    '    <div class="lg-card">',
    ADDR_DE,
    h("p", "imForm").replace("    <p", "      <p"),
    h("p", "imRep").replace("    <p", "      <p"),
    '    </div>',
    h("h2", "imContactT"),
    labelled([("imLblEmail", '<a href="mailto:mirelamistodinis@gmail.com">mirelamistodinis@gmail.com</a>'),
              ("imLblWeb", '<a href="https://stelzerweb.at/europe4strays/">stelzerweb.at/europe4strays</a>')]) ,
    '    <ul><li>Facebook: <a href="https://www.facebook.com/europe4straysbyMM" target="_blank" rel="noopener">facebook.com/europe4straysbyMM</a></li></ul>',
    h("h2", "imRegT"),
    labelled([("imLblCourt", "Judecătoria Focșani, România"),
              ("imLblReg", "Seria A Nr. 1493156"),
              ("imLblCif", "38480968")]),
    h("h2", "imRespT"),
    h("p", "imResp"),
    h("h2", "imCredT"),
    h("p", "imCred"),
    ul(["imCredSk", "imCredMap", "imCredFont"]),
    '    <ul><li>Tierschutzgruppe Herzensmenschen e.&nbsp;V.</li><li>Hunderunde</li></ul>',
    h("p", "imCredAi"),
    h("h2", "imLiabT"),
    h("p", "imLiab"),
    h("h2", "imPrivT"),
    plink("imPrivA", "datenschutz.html", "navPrivacy", "."),
    h("p", "imPrivB"),
    h("p", "imUpdated", cls="lg-note"),
    h("p", "lgAuth", cls="lg-note"),
])

DATENSCHUTZ_BODY = "\n".join([
    h("h2", "dp1T"),
    '    <div class="lg-card">',
    ul([("dp1aT", "dp1a"), ("dp1bT", "dp1b"), ("dp1cT", "dp1c"),
        ("dp1dT", "dp1d"), ("dp1eT", "dp1e"), ("dp1fT", "dp1f")]).replace("    <", "      <"),
    '    </div>',
    h("p", "dp1x"),

    h("h2", "dp2T"),
    '    <div class="lg-card">',
    ADDR_DE.replace("      </p>", '        <br>E-Mail: <a href="mailto:mirelamistodinis@gmail.com">mirelamistodinis@gmail.com</a>\n      </p>'),
    ('      <p><span data-i18n="dp2Rep">%s</span> <a href="impressum.html" data-i18n="navImprint">%s</a>.</p>'
     % (txt("dp2Rep"), txt("navImprint"))),
    '    </div>',

    h("h2", "dp3T"),
    h("p", "dp3a"),
    ul(["dp3l1", "dp3l2", "dp3l3", "dp3l4", "dp3l5", "dp3l6"]),
    h("p", "dp3b"),
    h("h3", "dp3hT"),
    plink("dp3h", "https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement",
          "dp3hLink", ".", ' target="_blank" rel="noopener"'),

    h("h2", "dp4T"),
    h("p", "dp4a"),
    ul([("dp4lT", "dp4l")]),
    h("p", "dp4b"),

    h("h2", "dp5T"),
    para_pair("dp5aT", "dp5a"),
    para_pair("dp5bT", "dp5b"),

    h("h2", "dp6T"),
    h("p", "dp6a"),
    h("h3", "dp6bT"), h("p", "dp6b"),
    pol(("PayPal", "https://www.paypal.com/de/legalhub/paypal/privacy-full")),
    h("h3", "dp6cT"), h("p", "dp6c"),
    pol(("Teaming", "https://www.teaming.net/condiciones-legales/2/proteccion-datos")),
    h("h3", "dp6dT"), h("p", "dp6d"),
    pol(("Amazon", "https://www.amazon.de/gp/help/customer/display.html?nodeId=201909010")),
    h("h3", "dp6eT"), h("p", "dp6e"),
    pol(("Meta (Facebook)", "https://www.facebook.com/privacy/policy/"),
        ("Instagram", "https://privacycenter.instagram.com/policy")),
    h("h3", "dp6fT"), h("p", "dp6f"),
    pol(("Tierschutzgruppe Herzensmenschen", "https://tierschutzgruppe-herzensmenschen.de/datenschutz/")),
    h("h3", "dp6gT"), h("p", "dp6g"),
    pol(("Hunderunde", "https://hunderunde.shop/policies/privacy-policy")),
    h("h3", "dp6hT"), h("p", "dp6h"),
    pol(("Google", "https://policies.google.com/privacy"),
        ("OpenStreetMap", "https://osmfoundation.org/wiki/Privacy_Policy")),

    h("h2", "dp7T"),
    h("p", "dp7a"),
    h("p", "dp7b"),
    plink("dp7c", "https://policies.google.com/privacy", "dp7Link", ".", ' target="_blank" rel="noopener"'),

    h("h2", "dp8T"), h("p", "dp8a"), h("p", "dp8b"),
    h("h2", "dp9T"), h("p", "dp9a"),
    h("h2", "dp10T"), h("p", "dp10a"), h("p", "dp10b"),
    ('    <p><span data-i18n="dp10c">%s</span> <a href="https://www.dataprotection.ro/" target="_blank" rel="noopener">dataprotection.ro</a></p>' % txt("dp10c")),
    h("p", "dpUpdated", cls="lg-note"),
    h("p", "lgAuth", cls="lg-note"),
])

# --------------------------------------------------------------------------- #
#  write the pages: keep everything outside <div class="lg-body"> untouched
# --------------------------------------------------------------------------- #
def rewrite(path, h1_key, lead_key, title_key, body):
    s = io.open(path, encoding="utf-8").read()
    new_main = ('  <section class="lg-hero">\n'
                '    <div class="inner">\n'
                '      <p class="lg-kicker">Europe4strays</p>\n'
                '      <h1 class="lg-title" data-i18n="%s">%s</h1>\n'
                '      <p class="lg-lead" data-i18n="%s">%s</p>\n'
                '    </div>\n'
                '  </section>\n\n'
                '  <div class="lg-body">\n\n%s\n\n  </div>\n' % (h1_key, txt(h1_key), lead_key, txt(lead_key), body))
    s2 = re.sub(r'  <section class="lg-hero">.*?\n  </div>\n(?=</main>)', new_main, s, count=1, flags=re.S)
    if s2 == s:
        sys.exit("could not replace <main> content of " + path)
    s2 = re.sub(r"<title[^>]*>.*?</title>",
                '<title data-i18n="%s">%s</title>' % (title_key, txt(title_key)), s2, count=1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s2)
    print("%-18s %d data-i18n attributes" % (path, s2.count('data-i18n=')))

rewrite("impressum.html", "imH1", "imLead", "imTitle", IMPRESSUM_BODY)
rewrite("datenschutz.html", "dpH1", "dpLead", "dpTitle", DATENSCHUTZ_BODY)

# --------------------------------------------------------------------------- #
#  i18n.js: replace the generated block in every language
# --------------------------------------------------------------------------- #
START = "      /* --- legal pages, generated by tools/build-legal.py --- */"
END = "      /* --- end legal pages --- */"
t = io.open("i18n.js", encoding="utf-8").read()
t = re.sub(re.escape(START) + r".*?" + re.escape(END) + "\n", "", t, flags=re.S)

lines, out, lang, done = t.split("\n"), [], None, 0
bounds = {"    en: {": 0, "    de: {": 1, "    it: {": 2, "    ro: {": 3}
for ln in lines:
    if ln in bounds:
        lang = bounds[ln]
    out.append(ln)
    if lang is not None and ln.strip().startswith("navPrivacy:"):
        out.append(START)
        for k, vals in S.items():
            out.append('      %s: "%s",' % (k, vals[lang].replace("\\", "\\\\").replace('"', '\\"')))
        out.append(END)
        done += 1
        lang = None
if done != 4:
    sys.exit("i18n: inserted %d blocks, expected 4" % done)
io.open("i18n.js", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("i18n.js: %d keys x 4 languages" % len(S))
