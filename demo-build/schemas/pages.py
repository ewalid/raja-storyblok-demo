"""Content types: locked campaign template, shared group block + its reference, site-config, and the
flexible default-page restricted to the RAJA sections."""
from .common import *

SECTIONS = ["RAJA · Sections"]

# ---------- flexible page (homes, free pages) ----------
patch("default-page", "body", restrict_components=True, restrict_type="groups", component_group_whitelist_names=SECTIONS,
      display_name="Contenu de la page", description="Toutes les sections RAJA. Glissez-déposez pour réordonner.")

# ---------- locked campaign template ----------
SEO = {
    "meta_title": text("Titre SEO", max_length=60, required=True, description="Affiché dans Google. 60 caractères max."),
    "meta_description": area("Meta description", max_length=160, required=True, description="Résumé affiché dans Google. 160 caractères max."),
    "og_image": image("Image de partage", description="Image utilisée sur LinkedIn / réseaux sociaux. 1200×630 conseillé."),
    "noindex": boolean("Ne pas indexer (noindex)", description="À cocher pour une page privée ou une campagne réservée à un lien."),
}
CAMPAIGN = {
    "objective": opt("Objectif", [("acquisition", "Acquisition nouveaux clients"), ("promo", "Promotion / déstockage"),
                                   ("seasonal", "Temps fort saisonnier (Black Friday, rentrée…)"), ("launch", "Lancement produit"),
                                   ("b2b", "Grands comptes")], "seasonal", description="Pour le reporting et les filtres de l'équipe Atlas."),
    "owner": text("Responsable", translatable=False, max_length=40, description="Qui pilote la campagne."),
    "sites": opts("Sites de diffusion", SITES, description="Sites qui reprennent cette campagne. Vide = tous les sites du groupe."),
    "starts_at": dt("Début", description="Pour le calendrier de campagne. La mise en ligne se programme avec « Publier plus tard »."),
    "ends_at": dt("Fin", description="Pour le calendrier de campagne."),
    "utm_campaign": text("utm_campaign", translatable=False, max_length=60, description="Identifiant de tracking, ex. bf-2026."),
}
GENERAL = {
    "hero": bloks("1 · En-tête de campagne", ["rj-hero", "rj-hero-mosaic"], minimum=1, maximum=1, required=True,
                  description="Obligatoire : un Hero (5 mises en page) ou une Mosaïque d'accueil."),
    "highlight": bloks("2 · Offre et réassurance", ["rj-promo-banner", "rj-usp-bar", "rj-headline-band"], maximum=2,
                       description="Optionnel : bandeau promo (code, compte à rebours) et/ou barre de réassurance."),
    "products": bloks("3 · Produits (Intershop)", ["rj-product-carousel", "rj-category-grid"], minimum=1, maximum=3, required=True,
                      description="Au moins un carrousel produits : les prix et le stock viennent d'Intershop."),
    "content": bloks("4 · Contenu éditorial", ["rj-split", "rj-promo-duo", "rj-card-slider", "rj-text", "rj-free-section",
                                               "rj-faq", "rj-reviews", "rj-shared-ref", "rj-selection-band", "rj-showcase-band"], maximum=6,
                     description="Optionnel : jusqu'à 6 sections éditoriales."),
    "closing": bloks("5 · Appel à l'action final", ["rj-cta-band"], maximum=1, description="Optionnel."),
}
sch, pos = {}, 0
for k, v in {**GENERAL, **SEO, **CAMPAIGN}.items():
    v = dict(v); v["pos"] = pos; pos += 1; sch[k] = v
for title, fields in [("SEO", SEO), ("Campagne", CAMPAIGN)]:
    sch[f"tab-{uuid.uuid5(uuid.NAMESPACE_DNS, 'rj-campaign-' + title)}"] = {"type": "tab", "display_name": title, "keys": list(fields), "pos": pos}
    pos += 1
comp("rj-campaign-page", "Page campagne (gabarit verrouillé)", sch, GROUP_PAGE, nestable=False, root=True, icon="block-doc",
     color="#6121f5", preview="meta_title",
     description="Gabarit groupe : structure fixe en 5 emplacements, blocs autorisés limités. Même gabarit pour tous les sites.")

# ---------- shared group block + reference ----------
comp("rj-shared-block", "Bloc partagé du groupe", {
    "body": dict(bloks("Sections partagées", [], minimum=1, maximum=3, pos=0,
                       description="La ou les sections réutilisées par les sites. Une modification ici est reprise partout à la publication."),
                 component_group_whitelist_names=SECTIONS, restrict_type="groups"),
    "notes": dict(area("Note interne", translatable=False, max_length=300, pos=1,
                       description="Pour l'équipe Atlas : usage, période, sites concernés. Jamais affiché sur le site.")),
}, GROUP_PAGE, nestable=False, root=True, icon="block-share", color="#276ef1",
    description="Contenu maître de l'équipe centrale, référencé par les sites (bloc « Bloc partagé du groupe »).")

comp("rj-shared-ref", "Bloc partagé du groupe (référence)", schema({
    "reference": f("option", "Bloc du groupe", source="internal_stories", folder_slug="group/blocs-partages/",
                   filter_content_type=["rj-shared-block"], required=True,
                   description="Choisissez un bloc maître de group/blocs-partages. Il s'affiche dans la langue du site (italien sur Mondoffice) et se met à jour automatiquement."),
}, style=False, mobile=False), GROUP_SECT, icon="block-share", color="#276ef1", preview="reference",
    description="Reprend un bloc créé par l'équipe centrale. Les sites ne le modifient pas : ils le traduisent et le planifient.")

# ---------- site-config (header + footer per site) ----------
comp("rj-nav-item", "Lien de navigation", {
    "label": text("Libellé", required=True, max_length=40, pos=0, description="Texte du lien."),
    "link": link("Lien", pos=1, description="Page Storyblok ou URL Intershop."),
    "highlight": boolean("Mettre en avant", pos=2, description="Fond légèrement plus clair, pour un temps fort (ex. Black Friday)."),
}, GROUP_ITEM, preview="label", icon="block-arrow-pointer")
ICONS = [("truck", "Livraison"), ("box", "Colis / stock"), ("gift", "Cadeau"), ("mail", "Newsletter"), ("tag", "Promo"),
         ("star", "Avis"), ("shield", "Garantie"), ("return", "Retour"), ("euro", "Prix"), ("leaf", "Éco-responsable"),
         ("headset", "Service client"), ("clock", "Délai")]
comp("rj-topbar-item", "Message de la barre supérieure", {
    "icon": dict(opt("Icône", ICONS, "truck", description="Pictogramme affiché avant le texte."), pos=0),
    "text": text("Texte", required=True, max_length=50, pos=1, description="Court : la barre fait une ligne."),
    "link": link("Lien (optionnel)", pos=2, description="Vide = texte non cliquable."),
}, GROUP_ITEM, preview="text", icon="block-text-c")
comp("rj-footer-column", "Colonne du pied de page", {
    "title": text("Titre", required=True, max_length=40, pos=0, description="Titre de la colonne (couleur de la marque)."),
    "links": bloks("Liens", ["rj-nav-item"], maximum=12, pos=1, description="Jusqu'à 12 liens."),
}, GROUP_ITEM, preview="title", icon="block-table-2")

HEADER = {
    "brand": opt("Marque (thème)", [("raja", "RAJA (bleu / violet)"), ("mondoffice", "Mondoffice (rouge)")], "raja", required=True,
                 description="Applique les couleurs de la marque à tout le site : en-tête, boutons, fonds « marque »."),
    "site_name": text("Nom du site", max_length=40, description="Utilisé si aucun logo n'est choisi, et dans le titre des pages."),
    "logo": image("Logo (blanc, pour l'en-tête)", description="SVG blanc conseillé, affiché sur la couleur de la marque."),
    "phone": text("Téléphone", max_length=24, description="Ex. 01 49 90 49 90"),
    "phone_hours": text("Horaires", max_length=40, description="Ex. (8h - 18h30)"),
    "rating_value": text("Note clients", max_length=12, description="Ex. 4,6/5"),
    "rating_label": text("Libellé de la note", max_length=30, description="Ex. Avis client"),
    "search_placeholder": text("Texte de la recherche", max_length=60, description="Texte grisé dans le champ de recherche."),
    "quick_order_label": text("Commande rapide", max_length=30, description="Ex. Achat express. Vide = masqué."),
    "account_label": text("Compte", max_length=24, description="Ex. Mon compte"),
    "products_label": text("Bouton catalogue", max_length=24, description="Ex. Nos produits. Ouvre le menu des catégories, fourni par Intershop."),
    "nav": bloks("Liens de navigation", ["rj-nav-item"], maximum=8, description="Liens marketing à côté du bouton catalogue. Le catalogue lui-même vient d'Intershop."),
}
TOPBAR = {
    "topbar": bloks("Messages de la barre supérieure", ["rj-topbar-item"], maximum=4, description="Barre sombre au-dessus de l'en-tête. Vide = pas de barre (cas de raja.fr)."),
    "topbar_rating": text("Note dans la barre", max_length=30, description="Ex. 4,4/5 Trustpilot. Vide = masquée."),
}
FOOTER = {
    "newsletter_title": text("Newsletter : titre", max_length=60, description="Vide = pas de bloc newsletter."),
    "newsletter_text": rich("Newsletter : texte", description="Une ou deux phrases."),
    "newsletter_placeholder": text("Newsletter : champ email", max_length=30, description="Ex. Adresse email *"),
    "newsletter_button": text("Newsletter : bouton", max_length=20, description="Ex. S'abonner"),
    "newsletter_success": text("Newsletter : message de confirmation", max_length=80, description="Affiché après l'inscription."),
    "catalogue_title": text("Catalogue : titre", max_length=40, description="Vide = pas de bloc catalogue."),
    "catalogue_subtitle": text("Catalogue : sous-titre", max_length=60, description="Ex. En ligne ou en version papier !"),
    "catalogue_text": rich("Catalogue : texte", description="Une phrase."),
    "catalogue_button": text("Catalogue : bouton", max_length=28, description=BTN_HELP),
    "catalogue_link": link("Catalogue : lien"),
    "catalogue_image": image("Catalogue : visuel", description="Couverture du catalogue (détourage conseillé)."),
    "footer_intro_title": text("Texte de présentation : titre", max_length=60, description="Ex. Pourquoi choisir RAJA ?"),
    "footer_intro": rich("Texte de présentation", description="Paragraphe SEO en haut du pied de page."),
    "footer_columns": bloks("Colonnes de liens", ["rj-footer-column"], maximum=6, description="Jusqu'à 6 colonnes."),
    "certifications": multiasset("Labels et certifications", description="Logos (EcoVadis, ISO…), affichés en bas du pied de page."),
    "legal_links": bloks("Liens légaux", ["rj-nav-item"], maximum=8, description="Mentions légales, CGV, cookies…"),
    "copyright": text("Copyright", max_length=60, description="Ex. © 2026 RAJA"),
}
sch, pos = {}, 0
for k, v in {**HEADER, **TOPBAR, **FOOTER}.items():
    v = dict(v); v["pos"] = pos; pos += 1; sch[k] = v
for title, fields in [("Barre supérieure", TOPBAR), ("Pied de page", FOOTER)]:
    sch[f"tab-{uuid.uuid5(uuid.NAMESPACE_DNS, 'rj-config-' + title)}"] = {"type": "tab", "display_name": title, "keys": list(fields), "pos": pos}
    pos += 1
comp("rj-site-config", "Configuration du site", sch, GROUP_PAGE, nestable=False, root=True, icon="block-wallet", color="#222831",
     preview="site_name", description="En-tête, navigation et pied de page d'un site. Une par dossier de site.")
