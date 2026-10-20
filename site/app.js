// Site des données : lit les fichiers du dépôt (manifestes, catalogue, critères, index de recherche).
// Rien n'est recopié : chaque tableau est reconstruit à partir des fichiers publiés.
(function () {
  const GH = 'https://github.com/branbriere/microcontroland-data/blob/main/';

  const T = {
    fr: {
      titre: 'Données ouvertes de Microcontrôland',
      sousTitre: 'Données brutes, documentation, protocoles et études d\'un système multi-agents embarqué sur sept ESP32-S3.',
      rechercher: 'Rechercher',
      placeholder: 'Rechercher : données, études, apprentissage, langue…',
      legendeCerveau: 'Exemple de cerveau Hinton : 18 neurones représentés (9 entrées, 6 cachés, 3 sorties), biais en pointillés. Celui d\'un citoyen de Microcontrôland compte 81 connexions, plus 75 dans un second cerveau qui ne sert que s\'il est président.',
      icDonnees: 'Données brutes', icEtudes: 'Études', icProtocoles: 'Pré-enregistrements',
      icDoc: 'Documentation', icCorrections: 'Corrections', icIndice: 'Critères de vie artificielle',
      indiceTitre: 'Critères de vie artificielle : ce que les données montrent',
      indiceNote: 'Grille v2 de 18 aptitudes (validée le 19 octobre 2026, révisée après lecture de sept publications). Les seuils chiffrés de chaque test seront écrits et datés avant le premier calcul. Le plafond est la note maximale possible avec la conception actuelle du système, pas un résultat. Les états s\'affichent à partir de l\'âge de la Curiosité du système (un stade de développement défini dans le firmware, jour 60 au plus tôt). Ce tableau mesure une proximité avec une grille ; il ne dit pas que les agents sont vivants ou conscients.',
      colAptitude: 'Aptitude', colEtat: 'État', colMesurable: 'Mesurable avec', colPlafond: 'Plafond', lienGrille: 'Lire la grille v2 : tests et publications',
      enAttente: 'en attente',
      donneesTitre: 'Données brutes',
      donneesNote: 'Un fichier par jour, jamais modifié après publication. Les jours du 9 au 14 octobre 2026 sont reconstitués à partir du journal publié (pas de données horaires). Vérifiez chaque fichier avec son empreinte SHA-256.',
      colDate: 'Date', colSource: 'Source', colTaille: 'Taille',
      srcPasserelle: 'passerelle', srcReconstitue: 'reconstitué',
      etudesTitre: 'Études', etudesNote: 'Programme de 21 études et statut de chacune (catalogue du dépôt).',
      colEtude: 'Étude', colStatut: 'Statut', colMoment: 'Calendrier',
      protocolesTitre: 'Protocoles et pré-enregistrements',
      protocolesNote: 'Déposés avant l\'analyse et archivés sur Zenodo, dont la date est vérifiable indépendamment.',
      docTitre: 'Documentation',
      correctionsTitre: 'Registre des incidents et des corrections',
      correctionsNote: 'Les incidents techniques et les corrections sont datés et documentés à part ; les fichiers publiés ne sont jamais modifiés. Les absences de données restent visibles dans chaque fichier brut (valeurs null, heures manquantes).', registreLien: 'Lire le registre des incidents et des corrections',
      etatTitre: 'État des archives scientifiques',
      etatCollecte: 'Dernière collecte', etatIntegrite: 'Intégrité des fichiers',
      etatReponses: 'Réponses des régions (dernier jour)', etatIncidents: 'Incidents et corrections documentés',
      etatRegistre: 'Accéder au registre', verifierTout: 'tout vérifier',
      integriteOk: (n, t) => `SHA-256 vérifié : ${n}/${t} conforme${n > 1 ? 's' : ''} au manifeste`,
      integriteKo: (n, t, l) => `SHA-256 : ${n}/${t} non conforme${n > 1 ? 's' : ''} (${l})`,
      verification: 'vérification…', dernierFichier: ' (dernier fichier ; « tout vérifier » pour les autres)',
      reponses: (m, t, h) => `${t - m}/${t} région-heures reçues` + (h ? `, ${h} heure${h > 1 ? 's' : ''} manquante${h > 1 ? 's' : ''}` : ''),
      pied: 'Données et documentation sous CC BY 4.0, code sous MIT. Bran Brière, chercheur indépendant. Aucun cookie. Seul service extérieur : la mesure d\'audience anonyme GoatCounter (aucune adresse IP enregistrée, totaux seulement, hébergée dans l\'Union européenne ; rien n\'est compté si votre navigateur demande « Ne pas suivre »).',
      chargement: 'chargement…', indisponible: 'fichier indisponible',
      aucun: 'Aucun résultat.',
      types: { doc: 'documentation', etude: 'étude', critere: 'critère', jour: 'données', protocole: 'protocole' }
    },
    en: {
      titre: 'Microcontrôland open data',
      sousTitre: 'Raw data, documentation, protocols and studies from a multi-agent system embedded on seven ESP32-S3 boards.',
      rechercher: 'Search',
      placeholder: 'Search: data, studies, learning, language…',
      legendeCerveau: 'Example of a Hinton brain: 18 neurons shown (9 inputs, 6 hidden, 3 outputs), biases dashed. A Microcontrôland citizen\'s brain has 81 connections, plus 75 in a second brain used only when the citizen is president.',
      icDonnees: 'Raw data', icEtudes: 'Studies', icProtocoles: 'Preregistrations',
      icDoc: 'Documentation', icCorrections: 'Corrections', icIndice: 'Artificial-life criteria',
      indiceTitre: 'Artificial-life criteria: what the data show',
      indiceNote: 'Grid v2 of 18 capacities (approved on 19 October 2026, revised after reading seven publications). The numerical threshold of each test will be written and dated before the first computation. The ceiling is the highest score possible with the current design of the system, not a result. States are displayed from the system\'s Age of Curiosity onwards (a developmental stage defined in the firmware, day 60 at the earliest). This table measures proximity to a grid; it does not state that the agents are alive or conscious.',
      colAptitude: 'Capacity', colEtat: 'State', colMesurable: 'Measurable with', colPlafond: 'Ceiling', lienGrille: 'Read grid v2: tests and publications',
      enAttente: 'pending',
      donneesTitre: 'Raw data',
      donneesNote: 'One file per day, never modified after publication. Days from 9 to 14 October 2026 are rebuilt from the published newspaper (no hourly data). Check each file against its SHA-256 hash.',
      colDate: 'Date', colSource: 'Source', colTaille: 'Size',
      srcPasserelle: 'gateway', srcReconstitue: 'rebuilt',
      etudesTitre: 'Studies', etudesNote: 'Programme of 21 studies and the status of each (repository catalogue).',
      colEtude: 'Study', colStatut: 'Status', colMoment: 'Schedule',
      protocolesTitre: 'Protocols and preregistrations',
      protocolesNote: 'Filed before analysis and archived on Zenodo, whose date can be verified independently.',
      docTitre: 'Documentation',
      correctionsTitre: 'Incidents and corrections log',
      correctionsNote: 'Technical incidents and corrections are dated and documented separately; published files are never modified. Data gaps remain visible in every raw file (null values, missing hours).', registreLien: 'Read the incidents and corrections log',
      etatTitre: 'State of the scientific archive',
      etatCollecte: 'Last collection', etatIntegrite: 'File integrity',
      etatReponses: 'Region responses (last day)', etatIncidents: 'Documented incidents and corrections',
      etatRegistre: 'Open the log', verifierTout: 'check all',
      integriteOk: (n, t) => `SHA-256 verified: ${n}/${t} match the manifest`,
      integriteKo: (n, t, l) => `SHA-256: ${n}/${t} do not match (${l})`,
      verification: 'checking…', dernierFichier: ' (latest file; "check all" for the rest)',
      reponses: (m, t, h) => `${t - m}/${t} region-hours received` + (h ? `, ${h} missing hour${h > 1 ? 's' : ''}` : ''),
      pied: 'Data and documentation under CC BY 4.0, code under MIT. Bran Brière, independent researcher. No cookies. Only external service: anonymous GoatCounter audience measurement (no IP address stored, totals only, hosted in the European Union; nothing is counted if your browser sends "Do Not Track").',
      chargement: 'loading…', indisponible: 'file unavailable',
      aucun: 'No results.',
      types: { doc: 'documentation', etude: 'study', critere: 'criterion', jour: 'data', protocole: 'protocol' }
    }
  };

  let lang = 'en';
  try { lang = localStorage.getItem('mcl-langue') || ''; } catch (e) { lang = ''; }
  if (lang !== 'fr' && lang !== 'en') lang = (navigator.language || '').toLowerCase().startsWith('fr') ? 'fr' : 'en';

  const donnees = { criteres: null, jours: [], catalogue: null, index: [] };
  const el = (tag, attrs, ...enfants) => {
    const e = document.createElement(tag);
    for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
    for (const c of enfants) e.append(c instanceof Node ? c : document.createTextNode(c == null ? '' : String(c)));
    return e;
  };
  const lien = (href, texte) => el('a', { href }, texte);
  const charger = url => fetch(url, { cache: 'no-cache' }).then(r => { if (!r.ok) throw new Error(url); return r.json(); });
  const ko = n => (n / 1024).toLocaleString(lang === 'fr' ? 'fr-FR' : 'en-GB', { maximumFractionDigits: 1 }) + (lang === 'fr' ? ' Ko' : ' KB');

  function appliquerLangue() {
    const t = T[lang];
    document.documentElement.lang = lang;
    document.documentElement.classList.toggle('fr', lang === 'fr');
    document.querySelectorAll('[data-l]').forEach(n => { n.textContent = t[n.dataset.l]; });
    document.getElementById('q').placeholder = t.placeholder;
    document.querySelectorAll('.langues button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
    rendre();
    chercher();
  }

  function rendreCriteres() {
    const tb = document.querySelector('#table-criteres tbody');
    tb.replaceChildren();
    const c = donnees.criteres;
    if (!c) { tb.append(el('tr', {}, el('td', { colspan: 5 }, T[lang].chargement))); return; }
    let bloc = '';
    for (const k of c.criteres) {
      if (k.bloc !== bloc) {
        bloc = k.bloc;
        tb.append(el('tr', { class: 'bloc' }, el('td', { colspan: 5 }, bloc + '. ' + c.blocs[bloc][lang])));
      }
      tb.append(el('tr', { id: k.id, class: k.enAvant ? 'en-avant' : '' },
        el('td', {}, k.n), el('td', {}, k[lang], k.note ? el('span', { class: 'note-critere' }, k.note[lang]) : ''),
        el('td', {}, el('span', { class: 'etat-attente' }, '… ' + T[lang].enAttente)),
        el('td', {}, el('span', { class: 'etiquette' }, c.mesurable[k.mesurable][lang])),
        el('td', { class: 'plafond' }, lang === 'fr' ? String(k.plafond).replace('.', ',') : String(k.plafond))));
    }
    const lg = document.getElementById('lien-grille');
    if (lg && c.document) lg.href = GH + c.document[lang];
  }

  function rendreJours() {
    const tb = document.querySelector('#table-donnees tbody');
    tb.replaceChildren();
    if (!donnees.jours.length) { tb.append(el('tr', {}, el('td', { colspan: 5 }, T[lang].chargement))); return; }
    for (const f of donnees.jours) {
      tb.append(el('tr', { id: 'jour-' + f.date },
        el('td', {}, lien(f.fichier, f.date)),
        el('td', {}, f.source === 'reconstitue' ? T[lang].srcReconstitue : T[lang].srcPasserelle),
        el('td', {}, f.firmware || '—'),
        el('td', {}, ko(f.octets)),
        el('td', { class: 'code' }, f.sha256)));
    }
  }

  function rendreEtudes() {
    const tb = document.querySelector('#table-etudes tbody');
    tb.replaceChildren();
    const c = donnees.catalogue;
    if (!c) { tb.append(el('tr', {}, el('td', { colspan: 4 }, T[lang].chargement))); return; }
    for (const e of c.etudes) {
      const titre = el('td', {}, e.programme ? lien(GH + e.programme[lang], e.titre[lang]) : e.titre[lang]);
      if (e.doi) titre.append(' · ', lien('https://doi.org/' + e.doi, 'DOI ' + e.doi));
      tb.append(el('tr', { id: 'etude-' + e.id }, el('td', {}, e.id), titre,
        el('td', {}, c.statuts[e.statut] ? c.statuts[e.statut][lang] : e.statut), el('td', {}, e.moment[lang])));
    }
    const lp = document.getElementById('liste-protocoles');
    lp.replaceChildren();
    for (const e of c.etudes.filter(x => x.protocole)) {
      lp.append(el('li', {}, lien(GH + e.protocole[lang], e.id + ' — ' + e.titre[lang]),
        e.doi ? el('span', { class: 'dim' }, ' · ', lien('https://doi.org/' + e.doi, 'DOI ' + e.doi)) : ''));
    }
    lp.append(el('li', {}, lien(GH + 'protocoles/README.md', lang === 'fr' ? 'Liste des dépôts, dates et empreintes' : 'List of filings, dates and checksums')));
  }

  function rendreDoc() {
    const ul = document.getElementById('liste-doc');
    ul.replaceChildren();
    for (const d of donnees.index.filter(x => x.type === 'doc' && x.lang === lang))
      ul.append(el('li', {}, lien(GH + d.chemin, d.titre), el('span', { class: 'dim' }, ' · ' + d.chemin)));
  }

  // État des archives : dernière collecte, empreintes SHA-256 recalculées par le navigateur, réponses des régions.
  const etat = { dernier: null, verif: null };
  async function sha256(url) {
    const buf = await (await fetch(url, { cache: 'no-cache' })).arrayBuffer();
    const h = await crypto.subtle.digest('SHA-256', buf);
    return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, '0')).join('');
  }
  async function verifier(fichiers) {
    etat.verif = null; rendreEtat();
    const faux = [];
    for (const f of fichiers) { try { if (await sha256(f.fichier) !== f.sha256) faux.push(f.date); } catch (e) { faux.push(f.date); } }
    etat.verif = { total: fichiers.length, faux };
    rendreEtat();
  }
  async function chargerDernier() {
    const f = donnees.jours.find(x => x.source !== 'reconstitue');
    if (!f) return;
    try {
      const j = await charger(f.fichier);
      const heures = j.heures || [];
      etat.dernier = { utc: j.genereUtc, date: f.date, total: heures.length * 6,
        muettes: heures.reduce((n, h) => n + (h.regions || []).filter(r => r === null).length, 0),
        manquantes: (j.heuresManquantes || []).length };
    } catch (e) { etat.dernier = { erreur: true }; }
    rendreEtat();
  }
  function rendreEtat() {
    const t = T[lang], d = etat.dernier, v = etat.verif;
    const col = document.getElementById('etat-collecte'), integ = document.getElementById('etat-integrite'), rep = document.getElementById('etat-reponses');
    if (!d) { col.textContent = rep.textContent = t.chargement; }
    else if (d.erreur) { col.textContent = rep.textContent = t.indisponible; }
    else {
      col.textContent = d.utc ? d.utc.replace('T', ' ').replace(/:\d\dZ$/, ' UTC') : d.date;
      rep.textContent = t.reponses(d.muettes, d.total, d.manquantes);
    }
    if (!v) { integ.textContent = t.verification; integ.className = ''; }
    else if (!v.faux.length) { integ.textContent = '✓ ' + t.integriteOk(v.total, v.total) + (v.total < donnees.jours.length ? t.dernierFichier : ''); integ.className = 'ok'; }
    else { integ.textContent = '✗ ' + t.integriteKo(v.faux.length, v.total, v.faux.join(', ')); integ.className = 'alerte'; }
    document.getElementById('verifier-tout').disabled = !donnees.jours.length || (v === null && etat.lance);
  }

  function rendreRegistre() {
    const a = document.getElementById('lien-registre');
    a.href = GH + (lang === 'fr' ? 'documentation/registre-incidents.md' : 'documentation/registre-incidents.en.md');
  }
  function rendre() { rendreCriteres(); rendreJours(); rendreEtudes(); rendreDoc(); rendreEtat(); rendreRegistre(); }

  // Recherche dans le navigateur, sans appel extérieur.
  const normal = s => (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  function entrees() {
    const t = T[lang], out = [];
    for (const d of donnees.index.filter(x => x.lang === lang))
      out.push({ type: d.type, titre: d.titre, url: GH + d.chemin, texte: d.texte });
    if (donnees.criteres) for (const k of donnees.criteres.criteres)
      out.push({ type: 'critere', titre: k.n + ' ' + k[lang], url: '#' + k.id, texte: k.fr + ' ' + k.en + ' ' + k.motsCles.join(' ') + ' ' + donnees.criteres.mesurable[k.mesurable][lang] });
    if (donnees.catalogue) for (const e of donnees.catalogue.etudes)
      out.push({ type: 'etude', titre: e.id + ' ' + e.titre[lang], url: '#etude-' + e.id, texte: e.titre.fr + ' ' + e.titre.en + ' ' + e.moment[lang] + (e.doi ? ' ' + e.doi : '') });
    for (const f of donnees.jours)
      out.push({ type: 'jour', titre: f.date + ' (' + (f.source === 'reconstitue' ? t.srcReconstitue : t.srcPasserelle) + ')', url: f.fichier, texte: f.date + ' ' + f.sha256 + ' ' + (f.firmware || '') + ' ' + f.source });
    return out;
  }

  function extrait(texte, mots) {
    const n = normal(texte);
    let i = -1;
    for (const m of mots) { i = n.indexOf(m); if (i >= 0) break; }
    if (i < 0) return '';
    const debut = Math.max(0, i - 60);
    return (debut > 0 ? '…' : '') + texte.slice(debut, i + 120).replace(/\s+/g, ' ') + '…';
  }

  function chercher() {
    const ul = document.getElementById('resultats');
    const q = normal(document.getElementById('q').value.trim());
    ul.replaceChildren();
    if (q.length < 2) return;
    const mots = q.split(/\s+/).filter(Boolean);
    const res = [];
    for (const e of entrees()) {
      const titre = normal(e.titre), texte = normal(e.texte);
      if (!mots.every(m => titre.includes(m) || texte.includes(m))) continue;
      const score = mots.reduce((s, m) => s + (titre.includes(m) ? 5 : 0) + (texte.split(m).length - 1), 0);
      res.push({ e, score });
    }
    res.sort((a, b) => b.score - a.score);
    if (!res.length) { ul.append(el('li', {}, el('a', { href: '#' }, T[lang].aucun))); return; }
    for (const { e } of res.slice(0, 12)) {
      const a = el('a', { href: e.url }, el('span', { class: 'type' }, T[lang].types[e.type] || e.type), ' ', e.titre);
      const x = e.type === 'doc' || e.type === 'protocole' ? extrait(e.texte, mots) : '';
      if (x) a.append(el('span', { class: 'extrait' }, x));
      ul.append(el('li', {}, a));
    }
  }

  document.querySelectorAll('.langues button').forEach(b => b.addEventListener('click', () => {
    lang = b.dataset.lang;
    try { localStorage.setItem('mcl-langue', lang); } catch (e) { /* stockage indisponible : sans importance */ }
    appliquerLangue();
  }));
  document.getElementById('q').addEventListener('input', chercher);
  document.getElementById('verifier-tout').addEventListener('click', () => { etat.lance = true; verifier(donnees.jours); });

  appliquerLangue();
  Promise.allSettled([
    charger('site/criteres.json').then(j => { donnees.criteres = j; }),
    charger('etudes/catalogue.json').then(j => { donnees.catalogue = j; }),
    charger('site/recherche.json').then(j => { donnees.index = j.documents; }),
    Promise.allSettled([charger('donnees/ere-001/manifeste.json'), charger('donnees/ere-001/reconstitue/manifeste.json')])
      .then(r => {
        const tous = r.filter(x => x.status === 'fulfilled').flatMap(x => x.value.fichiers);
        donnees.jours = tous.sort((a, b) => b.date.localeCompare(a.date));
      })
  ]).then(rendre).then(chercher).then(() => {
    // Au chargement : le dernier fichier publié par la passerelle est vérifié ; « tout vérifier » vérifie le reste.
    chargerDernier();
    etat.lance = true;
    verifier(donnees.jours.slice(0, 1));
  });
})();
