"""01_assets.py: download, vet and upload the RAJA FR / Mondoffice IT image library.

Every entry below was opened and checked visually before being listed here
(no baked headline/price/promo text, no watermark, photos >= 400px wide).
Rejected candidates are kept in REJECTED for traceability and are never uploaded.

Usage:
    python3 01_assets.py --download-only   # fetch into assets/src/, no upload
    python3 01_assets.py                    # fetch + upload + write assets/manifest.json

Idempotent: downloads skip existing files, uploads dedupe by filename.
"""
import json, os, re, sys, urllib.error, urllib.request
from PIL import Image
from sb_mapi import SB
from sb_assets import Assets

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "src")
MANIFEST = os.path.join(HERE, "assets", "manifest.json")
SPACE_ID = 296080873997343

S7 = "https://raja.scene7.com/is/image/Raja/"
MO = "https://www.mondoffice.com/INTERSHOP/static/WFS/RAJA-MONDOFFICE-Site/-/RAJA-MONDOFFICE/it_IT/"
MO2 = "https://www.mondoffice.com/INTERSHOP/static/WFS/RAJA-Site/MONDOFFICE/RAJA-MONDOFFICE/it_IT/"
RAJA_LOGO = "https://www.raja.fr/INTERSHOP/static/WFS/RAJA-FR-Site/-/RAJA-FR/fr_FR/images/logo-raja-desktop.svg?v=3.1.39.19"
MO_LOGO = MO + "images/logo-mondoffice-desktop.svg?v=3.1.39.19"
DARK = "#222831"

# (filename, url, folder, kind, alt, label, notes)
# folder = (top, sub)
R_LOGO, R_CAT, R_VIS, R_PROD = ("RAJA FR", "Logos"), ("RAJA FR", "Catégories"), ("RAJA FR", "Visuels"), ("RAJA FR", "Produits")
M_LOGO, M_CAT, M_VIS, M_PROD = ("Mondoffice IT", "Logos"), ("Mondoffice IT", "Catégories"), ("Mondoffice IT", "Visuels"), ("Mondoffice IT", "Produits")
G_VIS = ("Groupe", None)

ASSETS = [
    # ---------- Logos ----------
    ("raja-logo-white.svg", RAJA_LOGO, R_LOGO, "logo", "Logo RAJA blanc avec triangle rouge", "", "Wordmark blanc + triangle rouge #FF3137, pour fond dégradé bleu/violet"),
    ("raja-logo-dark.svg", "derive:raja-logo-white.svg", R_LOGO, "logo-dark", "Logo RAJA gris foncé avec triangle rouge", "", "Variante pour fond clair: blanc remplacé par #222831, triangle rouge conservé"),
    ("raja-avis-verifies-white.png", S7 + "FR-AvisVerifies-Logo2-w?fmt=png-alpha", R_LOGO, "badge", "Logo Avis Vérifiés blanc", "", "Badge avis clients, version blanche pour fond foncé"),
    ("raja-avis-verifies.png", S7 + "FR-AvisVerifies-Logo2?fmt=png-alpha", R_LOGO, "badge", "Logo Avis Vérifiés", "", "Badge avis clients, version couleur pour fond clair"),
    ("mo-logo-white.svg", MO_LOGO, M_LOGO, "logo", "Logo Mondoffice bianco", "", "Wordmark Mondoffice bianco per header rosso"),
    ("mo-logo-dark.svg", "derive:mo-logo-white.svg", M_LOGO, "logo-dark", "Logo Mondoffice grigio scuro", "", "Variante per sfondo chiaro: bianco sostituito da #222831"),
    ("mo-trustpilot-white.svg", "https://cdn.trustpilot.net/brand-assets/4.3.0/logo-white.svg", M_LOGO, "badge", "Logo Trustpilot bianco", "", "Per top bar scura"),
    ("mo-trustpilot-dark.svg", "https://cdn.trustpilot.net/brand-assets/4.3.0/logo-black.svg", M_LOGO, "badge", "Logo Trustpilot scuro", "", "Per sfondo chiaro"),

    # ---------- RAJA categories (transparent cut-outs, native 184px) ----------
    *[(f"raja-cat-{slug}.png", f"{S7}ALL-cat-C-{code}?fmt=png-alpha", R_CAT, "category", alt, label, notes) for code, slug, label, alt, notes in [
        ("01", "caisses-carton", "Caisses carton, boîtes", "Caisse en carton brun ouverte", "Détourage PNG transparent"),
        ("02", "adhesifs", "Adhésifs, cerclage, collage", "Dévidoir avec rouleau d'adhésif brun", "Détourage PNG transparent"),
        ("03", "enveloppes-pochettes", "Enveloppes, pochettes", "Pochette d'expédition en carton", "Détourage PNG transparent"),
        ("04", "sacherie", "Sacherie, conditionnement", "Sachets plastique à fermeture zip", "Détourage PNG transparent"),
        ("05", "calage-protection", "Calage, protection", "Rouleau de film à bulles", "Détourage PNG transparent"),
        ("06", "etiquetage", "Etiquetage, signalisation", "Rouleau d'étiquettes flèches rouges", "Détourage PNG transparent"),
        ("07", "film-palettisation", "Film, palettisation", "Bobines de film étirable avec dévidoir", "Détourage PNG transparent"),
        ("08", "emballages-boutiques", "Emballages boutiques", "Sac kraft à poignées", "Détourage PNG transparent"),
        ("09", "machines-emballage", "Machines d'emballage", "Machine de calage papier", "Détourage PNG transparent"),
        ("10", "stockage", "Stockage", "Bac de rangement gris", "Détourage PNG transparent"),
        ("11", "manutention", "Manutention", "Transpalette rouge", "Détourage PNG transparent"),
        ("12", "fournitures-bureau", "Fournitures et mobilier de bureau", "Ramette de papier A4", "Détourage PNG transparent"),
        ("13", "equipements-securite", "Équipements et sécurité", "Table d'emballage équipée", "Détourage PNG transparent"),
        ("14", "entretien-hygiene", "Entretien, hygiène", "Sac poubelle noir", "Détourage PNG transparent"),
        ("15", "emballages-alimentaires", "Emballages alimentaires", "Bol kraft avec salade", "Détourage PNG transparent"),
        ("16", "protection-individuelle", "Protection individuelle", "Gant de travail picoté", "Détourage PNG transparent"),
    ]],
    ("raja-box-finder.png", S7 + "FR_homepage_BOX?fmt=png-alpha", R_CAT, "cutout", "Illustration de caisse carton avec cotes L, l, H", "Je trouve mes formats", "Illustration du module « Trouver mon carton » (lettres de cotes uniquement)"),

    # ---------- Mondoffice categories (product packshots, white bg) ----------
    *[(f"mo-cat-{slug}.jpg", f"{S7}{img}?wid=800", M_CAT, "category", alt, label, notes) for slug, img, label, alt, notes in [
        ("arredo-complementi", "asset5228714", "Arredo e Complementi", "Bancone reception con postazione cassa", "Packshot su fondo bianco"),
        ("arredo-linee-mobili", "MON_103953_1_xnl", "Arredo - Linee Mobili", "Scrivania angolare in legno chiaro con cassettiera", "Packshot su fondo bianco"),
        ("scrittura", "asset7248919", "Scrittura", "Penna con punta in feltro nera", "Packshot su fondo bianco, formato molto orizzontale"),
        ("sedie-poltrone", "oit6222760AA", "Sedie e Poltrone", "Poltrona ergonomica nera in rete", "Packshot su fondo bianco"),
        ("archivio", "oit6698055AB", "Archivio", "Registratore Mondoffice nero con dorso rosso", "Packshot su fondo bianco"),
        ("cancelleria-scuola", "oit7464553AA", "Cancelleria e Scuola", "Cassettiera da scrivania nera", "Packshot su fondo bianco"),
        ("carta", "oit2564347AA", "Carta e Scrittura", "Scatola di risme di carta A4 Mondoffice", "Packshot su fondo bianco"),
        ("cartucce-toner", "MON_28626_1_xnl", "Cartucce e Toner", "Tamburo per stampante laser", "Packshot su fondo bianco"),
        ("tecnologia-informatica", "MON_6002236_1_xnl", "Tecnologia e Informatica", "Smartwatch con cinturino nero", "Packshot su fondo bianco"),
        ("stampanti", "oit8863626AA", "Stampanti", "Stampante multifunzione laser nera", "Packshot su fondo bianco"),
        ("monouso", "oit5323437AB", "Piatti Posate e Bicchieri Monouso", "Kit posate monouso compostabili", "Packshot su fondo bianco"),
        ("bevande-alimenti", "oit7734391AA", "Bevande e Alimenti", "Confezione di capsule di caffè", "Packshot su fondo bianco (testo del packaging prodotto)"),
        ("igiene-pulizia", "oit9571310AA", "Igiene e Pulizia", "Confezione di salviette igienizzanti", "Packshot su fondo bianco (testo del packaging prodotto)"),
        ("sicurezza-dpi", "oit4444982AA", "Sicurezza e DPI", "Elmetto di protezione giallo", "Packshot su fondo bianco"),
        ("spedizioni-imballo", "asset7595891", "Spedizioni e Imballo", "Scatola postale in cartone aperta", "Packshot su fondo bianco"),
        ("infermeria", "oit8936833BA", "Infermeria aziendale", "Valigetta di pronto soccorso rossa", "Packshot su fondo bianco"),
    ]],

    # ---------- RAJA lifestyle ----------
    ("raja-hero-packaging.jpg", S7 + "ALL-LP-packaging-supplies-4-steps-top?scl=1&qlt=90", R_VIS, "lifestyle", "Mains qui ferment une caisse carton sur un bureau", "", "Bandeau très large, emballage d'un colis à la main"),
    ("raja-hero-boutique.jpg", S7 + "ALL-LP-shop-top?scl=1&qlt=90", R_VIS, "lifestyle", "Vendeuse remettant un sac rose à une cliente en boutique", "", "Bandeau très large, commerce de détail / mode"),
    ("raja-hero-warehouse-scanner.jpg", S7 + "ALL-LP-warehouse-top?scl=1&qlt=90", R_VIS, "lifestyle", "Préparatrice scannant des bacs de stockage colorés en entrepôt", "", "Bandeau très large, sujet à droite, flou à gauche (bonne zone texte)"),
    ("raja-hero-custom-packaging.jpg", S7 + "ALL-LP-custom-measure-top?scl=1&qlt=90", R_VIS, "lifestyle", "Personne dessinant un emballage sur ordinateur portable", "", "Bandeau très large, emballage sur mesure / design"),
    ("raja-hero-ecommerce-conveyor.jpg", S7 + "ALL-BC-ecommerce-top-2?scl=1&qlt=90", R_VIS, "lifestyle", "Opérateurs scannant des colis sur un convoyeur", "", "Vue plongeante logistique e-commerce"),
    ("raja-hero-eco-globe.jpg", S7 + "ALL-BC-ecoresponsible-top?scl=1&qlt=90", R_VIS, "lifestyle", "Globe terrestre posé dans un carton sur fond vert", "", "Visuel emballage éco-responsable"),
    ("raja-delivery-van.jpg", S7 + "2305-FR-LP-services-delivery?scl=1&qlt=90", R_VIS, "lifestyle", "Camionnette de livraison RAJA en ville", "", "Habillage du véhicule RAJA (logo, téléphone) visible, pas de texte promo ajouté"),
    ("raja-warehouse-pallet-truck.jpg", S7 + "ALL-HP-MEA-corners-warehouse?scl=1&qlt=90", R_VIS, "lifestyle", "Magasinière déplaçant des cartons avec un transpalette", "", "Entrepôt, carré"),
    ("raja-boutique-shopping-bag.jpg", S7 + "ALL-HP-MEA-corners-boutique?scl=1&qlt=90", R_VIS, "lifestyle", "Vendeuse tendant un sac cadeau rouge à une cliente", "", "Boutique, carré"),
    ("raja-corner-ecommerce.jpg", S7 + "ALL-hub-corners-ecommerce?scl=1&qlt=90", R_VIS, "lifestyle", "Livreur portant un carton dans un centre logistique", "", "Portrait"),
    ("raja-corner-handling-storage.jpg", S7 + "ALL-hub-corners-handling-storage?scl=1&qlt=90", R_VIS, "lifestyle", "Magasinier avec gilet orange et casque-micro en entrepôt", "", "Portrait"),
    ("raja-corner-pack-protect-ship.jpg", S7 + "ALL-hub-corners-pack-protect-ship?scl=1&qlt=90", R_VIS, "lifestyle", "Homme emballant un objet dans du papier kraft", "", "Portrait"),
    ("raja-corner-office-supply.jpg", S7 + "ALL-hub-corners-office-supply?scl=1&qlt=90", R_VIS, "lifestyle", "Femme utilisant un photocopieur au bureau", "", "Portrait"),
    *[(f"raja-range-{slug}.jpg", f"{S7}ALL-layer-ranges-{code}?scl=1&qlt=90", R_VIS, "lifestyle", alt, "", "Visuel de méga-menu, format bandeau 616x272") for code, slug, alt in [
        ("packaging", "packaging", "Femme fermant un carton avec un dévidoir en entrepôt"),
        ("warehouse", "warehouse", "Préparatrice scannant des bacs en entrepôt"),
        ("shop", "shop", "Vendeuse remettant un sac à des clientes en boutique"),
        ("ecommerce", "ecommerce", "Livreur portant un carton dans un centre de tri"),
        ("janitorial", "janitorial", "Agent d'entretien nettoyant un poste de travail"),
        ("PPE", "ppe", "Employé en gilet haute visibilité posant une chaîne de balisage en entrepôt"),
        ("office-supplies", "office-supplies", "Femme travaillant à un bureau lumineux"),
    ]],

    # ---------- Groupe (shared) ----------
    ("group-hygiene-cleaning.jpg", S7 + "ALL-LP-janitorial-top?scl=1&qlt=90", G_VIS, "lifestyle", "Mains gantées de jaune nettoyant un lavabo", "", "Bandeau très large, hygiène / entretien"),
    ("group-office-open-space.jpg", S7 + "ALL-BC-office-supply-top?scl=1&qlt=90", G_VIS, "lifestyle", "Équipe au travail dans un open space lumineux", "", "Bureau moderne"),
    ("group-warehouse-managers.jpg", S7 + "ALL-T-LP-large-accounts-1?scl=1&qlt=90", G_VIS, "lifestyle", "Deux responsables avec tablette dans les allées d'un entrepôt", "", "Grands comptes / logistique"),
    ("group-warehouse-tablet.jpg", S7 + "2305-ALL-LP-services-large-accounts?scl=1&qlt=90", G_VIS, "lifestyle", "Femme avec tablette indiquant des rayonnages d'entrepôt à un collègue", "", "Logistique, cadrage serré"),
    ("group-customer-service.jpg", S7 + "2305-ALL-LP-services-advice?scl=1&qlt=90", G_VIS, "lifestyle", "Conseillère souriante avec casque-micro", "", "Service client"),
    ("group-call-centre.jpg", S7 + "2609-FR-video-G0929-LP-01-placeholder?scl=1&qlt=90", G_VIS, "lifestyle", "Conseillers avec casques travaillant sur écrans dans un plateau", "", "Service client, bureau"),
    ("group-ebusiness-team.jpg", S7 + "ALL-LP-ebusiness-gen-visual-3?scl=1&qlt=90", G_VIS, "lifestyle", "Deux collègues regardant un écran ensemble", "", "Solutions e-business, presque carré"),

    # ---------- Mondoffice lifestyle ----------
    ("mo-hero-studi-professionali.webp", MO2 + "images/2026/2802/2802-top-banner.webp", M_VIS, "lifestyle", "Professionista alla scrivania con una cliente in studio", "", "Banner largo 1200x313, settore studi professionali"),
    ("mo-hero-pulizia.webp", MO2 + "images/2026/2804/2804-top-banner_2.webp", M_VIS, "lifestyle", "Addetti alle pulizie al lavoro in un ufficio", "", "Banner largo, cartello di pavimento bagnato in scena"),
    ("mo-hero-retail.webp", MO2 + "images/2026/2678/2678-top-banner.webp", M_VIS, "lifestyle", "Commessa alla cassa di un negozio di abbigliamento", "", "Banner largo, retail"),
    ("mo-hero-accoglienza.webp", MO2 + "images/2026/2726/2726-top-banner.webp", M_VIS, "lifestyle", "Ospiti alla reception di un hotel", "", "Banner largo, hospitality; scena centrale con ampi margini scuri"),
    ("mo-hero-manifatturiero.webp", MO2 + "images/2026/2737/2737-top-banner_2.webp", M_VIS, "lifestyle", "Tecnico con portatile davanti a bracci robotici gialli", "", "Banner largo, industria"),
    ("mo-arredo-area-break.webp", MO2 + "images/2026/2229/arredo.webp", M_VIS, "lifestyle", "Area break aziendale con tavolini e sedie colorate", "", "Arredo"),
    ("mo-food-eco-bowls.webp", MO2 + "images/2026/2229/eco.webp", M_VIS, "lifestyle", "Ciotole in cartone con insalate su tavolo di legno", "", "Packaging alimentare eco"),
    ("mo-retail-negozio.webp", MO2 + "images/2026/2678/2678-paragrafo-1_1.webp", M_VIS, "lifestyle", "Interno di un negozio di abbigliamento luminoso", "", "Retail"),
    ("mo-manifattura-operaio.webp", MO2 + "images/2026/2737/2737-paragrafo-1.webp", M_VIS, "lifestyle", "Operaio con elmetto e cuffie al lavoro su un macchinario", "", "Industria"),
    ("mo-postazione-ufficio.webp", MO2 + "images/2026/2664/2664-spazi_1.webp", M_VIS, "lifestyle", "Scrivania con monitor, stampante e webcam", "", "Postazione di lavoro"),
    *[(f"mo-arredo-{slug}.jpg", f"{MO2}images/ARREDO/{f}", M_VIS, "lifestyle", alt, "", "Ambientazione arredo ufficio 700x394") for slug, f, alt in [
        ("linea-pronto", "Linea-Pronto-22_V.jpg", "Postazione con scrivania chiara e cassettiera in un ufficio luminoso"),
        ("linea-meeting", "Linea-Meeting-22_V.jpg", "Ufficio con scrivania in legno, sedie operative e libreria"),
        ("linea-exclusive", "Linea-Exclusive-22_V.jpg", "Ufficio direzionale con scrivania e mobili neri e legno"),
        ("linea-vertigo", "Linea-Vertigo-22_V.jpg", "Ufficio con scrivania sagomata in legno scuro e armadi"),
    ]],
    *[(f"mo-arredo-{slug}.webp", f"https://www.mondoffice.com/INTERSHOP/static/WFS/RAJA-Site/MONDOFFICE/RAJA-MONDOFFICE/it_IT/img-arredo/{f}", M_VIS, "lifestyle", alt, "", "Ambientazione arredo ufficio 700x394") for slug, f, alt in [
        ("sit-stand", "sitstand_cov.webp", "Supporto regolabile per portatile su scrivania bianca"),
        ("disegno", "disegno_cov.webp", "Ufficio con scrivania chiara, sedia nera e mobili contenitori"),
    ]],
    ("mo-vetrina-packaging.webp", MO2 + "home/2026/09-SET/W26_9_DHP_b1_Vetrina_packaging.webp", M_VIS, "lifestyle", "Illustrazione di scatole su pallet, nastro adesivo e scatola con riempitivo", "Tutto per le spedizioni", "Illustrazione 3D su fondo arancio, senza testo"),
    ("mo-vetrina-dpi.webp", MO2 + "home/2026/09-SET/W26_9_DHP_b2_Vetrina_DPI.webp", M_VIS, "lifestyle", "Magazziniere sorridente con elmetto e giubbotto alta visibilità tra le scaffalature", "Sicurezza 360°", ""),
    ("mo-vetrina-tech.webp", MO2 + "home/2026/09-SET/W26_9_DHP_b3_Vetrina_tech.webp", M_VIS, "lifestyle", "Cuffie, tastiera, mouse e monitor su fondo blu", "La tecnologia che serve", "Flat lay tecnologia"),
    ("mo-vetrina-arredo.webp", MO2 + "home/2026/09-SET/W26_9_DHP_b4_Vetrina_Marreda.webp", M_VIS, "lifestyle", "Ufficio arredato con scrivania, sedia ergonomica e librerie in legno", "Selezione Mondoffice M'Arreda", "Ambientazione arredo"),
    *[(f"mo-sector-{slug}.webp", f"{MO}images/2026/2641/{f}", M_VIS, "lifestyle", alt, label, "Card settore 400x250") for slug, f, label, alt in [
        ("industria", "industry-overview-home_1.webp", "Forniture B2B per ogni settore", "Due tecnici con elmetto e giubbotto alta visibilità in fabbrica"),
        ("pulizia", "2641-pulizia.webp", "Imprese di pulizia", "Addetti alle pulizie in un ufficio"),
        ("retail", "2641-retail_2.webp", "Retail", "Cliente alla cassa di un negozio con shopper bianca"),
        ("studi-professionali", "2641-studi-prof.webp", "Studi professionali", "Professionista con cliente alla scrivania"),
        ("accoglienza", "2641-accoglienza_3.webp", "Accoglienza", "Ospiti alla reception di un hotel"),
        ("manifatturiero", "2641-manufatturiero_4.webp", "Manifatturiero", "Tecnico davanti a bracci robotici"),
        ("supporto", "Supporto.jpg", "Supporto", "Operatrice sorridente con cuffie in un call center"),
    ]],
    ("mo-blog-stampanti.webp", MO + "home/2026/BLOG/blog_stampanti.webp", M_VIS, "lifestyle", "Donna pensierosa tra due stampanti in ufficio", "Guida stampanti", "Contiene solo un punto interrogativo grafico"),
    ("mo-blog-organizzazione.webp", MO + "home/2026/BLOG/organizzazione_blog-home.webp", M_VIS, "lifestyle", "Donna alla scrivania con tazza e libri in un ufficio ordinato", "Organizzazione scrivania", ""),
    ("mo-blog-rifiuti.webp", MO + "home/2026/BLOG/gestionerifiuti_blog_home.webp", M_VIS, "lifestyle", "Tre contenitori per raccolta differenziata in ufficio", "Gestione rifiuti", ""),

    # ---------- Products ----------
    *[(f"raja-{slug}.jpg", f"{S7}{img}?wid=1000", R_PROD, "packshot", alt, name, "Packshot fond blanc") for slug, img, name, alt in [
        ("caisse-double-cannelure", "M_CAD_WEB_ACCESSORY_01", "Caisse carton standard double cannelure RAJA", "Caisse carton double cannelure ouverte avec produit calé"),
        ("caisse-simple-cannelure", "M_CAS_WEB_ACCESSORY_01", "Caisse carton brune simple cannelure RAJA", "Caisse carton brune ouverte contenant un casque audio"),
        ("boite-postale-rajapost", "M_RPT07B_R_A_075_F", "Boîte carton d'expédition RAJAPOST", "Boîte postale en carton brun entrouverte"),
        ("pochette-bulles", "M_PMBL0C_PACKSHOT_05", "Pochette matelassée bulles Éco blanche RAJA", "Pochette matelassée blanche à bulles"),
        ("devidoir-adhesif", "M_ADV291_D_A4_066_F", "Dévidoir adhésif de sécurité RAJA", "Dévidoir bleu avec rouleaux d'adhésif"),
        ("caisse-galia", "M_GALIA_A_DW_WEB_ACCESSORY_01", "Caisse carton Galia double cannelure", "Caisse Galia ouverte avec calage en chips"),
        ("caisse-montage-instantane", "M_CFA_WEB_ACCESSORY_01", "Caisse carton à montage instantané RAJA", "Caisse carton à fond automatique ouverte"),
        ("film-bulles", "M_MCB50A_G_FR", "Film bulles 50% recyclé RAJA", "Rouleaux de film à bulles"),
    ]],
    *[(f"mo-{slug}.jpg", f"{S7}{img}?wid=1000", M_PROD, "packshot", alt, name, "Packshot su fondo bianco") for slug, img, name, alt in [
        ("buste-foratura-universale", "oit2306067BA", "MONDOFFICE Busta a foratura universale A4", "Buste trasparenti a foratura universale"),
        ("cucitrice-a-pinza", "oit5010784AA", "MONDOFFICE Cucitrice a pinza blu", "Cucitrice a pinza blu"),
        ("carta-igienica-24", "oit2315672AC", "MONDOFFICE Carta igienica Standard (24 rotoli)", "Confezione da 24 rotoli di carta igienica"),
        ("asciugamani-piegati", "ofr2132347AB", "MONDOFFICE Asciugamani di carta piegati a V", "Scatola di asciugamani di carta piegati"),
        ("registratore-blu", "oit5879637AB", "MONDOFFICE Registratore archivio Classic, Blu", "Registratore nero con dorso blu"),
        ("bobina-multiuso", "ofr2429203AC", "MONDOFFICE Bobina di carta multiuso", "Bobina di carta multiuso"),
        ("registratore-verde", "oit5368213AB", "MONDOFFICE Registratore archivio Classic, Verde", "Registratore nero con dorso verde"),
        ("carta-igienica-48", "oit8475562AA", "MONDOFFICE Carta igienica Standard (48 rotoli)", "Confezioni di carta igienica impilate"),
    ]],
]

REJECTED = {
    "ALL-MB-best-prices": "baked 'BEST PRICES' promo text",
    "ALL-HP-MEA-corners-ecommerce": "280px only",
    "FR-LP-testimonials-customers-top": "baked headline",
    "FR-LP-G0925-madeineeurope-top-2": "baked 'Made in Europe' headline",
    "ALL-BC-food-top-3": "chalkboard menu with prices in scene",
    "ALL-BC-security-top": "safety poster text, covid masks",
    "M_ADP26_ADV291_CAD_FR / M_FEB13_FED201_CAD_01_FR": "'GRATUIT' promo badge baked in",
    "2641-e-com / 2803-top-banner": "baked UI chips (Ordini, Spedizioni, Resi)",
    "blog_ows_tws": "baked 'VS' graphic",
    "banner-header-blog-2025_6": "baked 'BLOG' text",
    "catalogue_footer.png": "catalogue cover with headline text",
    "il-nostro-mondo/*, 002-Scopri-Nostro-Mondo valori/benessere": "baked captions",
    "1795/1819/2378 top banners, 2641-value-eccellenza": "baked promo text / '35m' badge",
    "categorie/*.jpg (homepage tiles)": "92x92 only; replaced by scene7 product packshots",
}


def svg_size(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r'viewBox="\s*[\d.\-]+[ ,]+[\d.\-]+[ ,]+([\d.]+)[ ,]+([\d.]+)', t)
    return (round(float(m.group(1))), round(float(m.group(2)))) if m else (None, None)


def derive_dark(src, dest):
    t = open(src, encoding="utf-8").read()
    t = re.sub(r'(fill[=:]\s*"?)#(?:fff|FFF|ffffff|FFFFFF)\b', r"\g<1>" + DARK, t)
    open(dest, "w", encoding="utf-8").write(t)


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 200:
        return
    # Mondoffice static files live under one of two Intershop prefixes; try the other on 404.
    candidates = [url]
    if url.startswith(MO):
        candidates.append(MO2 + url[len(MO):])
    elif url.startswith(MO2):
        candidates.append(MO + url[len(MO2):])
    for i, u in enumerate(candidates):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            open(dest, "wb").write(data)
            return
        except urllib.error.HTTPError as e:
            if i == len(candidates) - 1:
                raise RuntimeError(f"{e.code} for {url}") from e


def dims(path):
    if path.endswith(".svg"):
        return svg_size(path)
    with Image.open(path) as im:
        return im.size


def main():
    os.makedirs(SRC, exist_ok=True)
    for fn, url, *_ in ASSETS:
        dest = os.path.join(SRC, fn)
        if url.startswith("derive:"):
            continue
        fetch(url, dest)
    for fn, url, *_ in ASSETS:
        if url.startswith("derive:"):
            derive_dark(os.path.join(SRC, url.split(":", 1)[1]), os.path.join(SRC, fn))
    if "--download-only" in sys.argv:
        for fn, *_ in ASSETS:
            print(fn, dims(os.path.join(SRC, fn)))
        return

    sb = SB(SPACE_ID, env_path=os.path.expanduser("~/dev/darwin/storyblok.env"))
    a = Assets(sb)
    folders = {}

    def folder_id(top, sub):
        if (top, None) not in folders:
            folders[(top, None)] = a.folder(top)
        if sub is None:
            return folders[(top, None)]
        if (top, sub) not in folders:
            folders[(top, sub)] = a.folder(sub, folders[(top, None)])
        return folders[(top, sub)]

    manifest = {}
    for fn, url, (top, sub), kind, alt, label, notes in ASSETS:
        path = os.path.join(SRC, fn)
        fid = folder_id(top, sub)
        title = label or os.path.splitext(fn)[0]
        surl = a.upload(path, fid, alt=alt, title=title)
        ex = a.existing()[fn]
        w, h = dims(path)
        orient = "square" if w and h and abs(w - h) / max(w, h) < 0.08 else ("landscape" if (w or 0) > (h or 0) else "portrait")
        brand = "raja" if fn.startswith("raja-") else "mondoffice" if fn.startswith("mo-") else "group"
        manifest[os.path.splitext(fn)[0]] = {
            "filename": surl, "id": ex["id"], "alt": alt, "brand": brand, "kind": kind,
            "label": label, "width": w, "height": h, "orientation": orient, "notes": notes,
            "folder": f"{top}/{sub}" if sub else top, "source": url if not url.startswith("derive:") else "derived",
        }
        print("ok", fn, surl)
    json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(manifest)} assets -> {MANIFEST}")


if __name__ == "__main__":
    main()
