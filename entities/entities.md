# Analyses de l'audio

## Liste des classes qui déterminent les sons à filtrer

Voici 9 classes qui correspondent à des labels de classification pour les éléments sonores à couper (par exemple, les bruits de bouche, les bégaiements, les mots de remplissage, etc.). L'identification de ces événements permeterons par exemple de configurer l'application pour déterminer quels sons spécifiques doivent être coupés, comme les bruits de bouche ou les mots de remplissage, tout en conservant ou non les bégaiements naturels de certaines personnes.

#### **Filler Words** (mots de remplissage / hésitation)

- event name : filler_word
- desc : mots ou phrases courtes qui ne contribuent pas au sens et sont souvent utilisés pour combler les pauses
- ex : "euh", "um", "vous savez", "en fait euh"

#### Stuttering (bégaiements)

- event name : stuttering
- desc : répétitions involontaires de sons, syllabes ou mots, interruptions prolongées du son dans un mot
- ex : "Je v-v-voudrais ça"

#### Repetitions (répétitions)

- event name : repetitions
- desc : corrections, reprises de mots, faux depart, les mots qui crochent accidentellement sans apporter de nouvelle information
- ex : "C'est vraiment, + vraiment, important", "de, + de", "the, + the", "I wouldn't, + uh, I definitely wouldn't", "we, + we"

#### Redundant Phrases (phrases superflues)

- event name : redundant_phrases
- desc : phrases qui n'ajoutent pas de valeur informative significative ou qui sont redondantes
- ex : "En fait, à la fin de la journée, il est ce qu'il est"

#### Background Noises (bruits de fond)

- event name : background_noises
- desc : sons non liés au discours principal, comme le bruit des machines, des personnes parlant en arrière-plan
- ex : "Bruits de construction en arrière-plan", "Throat_clearing", "child", "noise", "music"

#### Interjections (interjections)

- event name : interjections
- desc : expressions courtes qui peuvent interrompre le flux de la conversation
- ex : "Oh!", "Laughter"

#### Loud Breaths (respirations fortes)

- event name : loud_breaths
- desc : respirations audibles qui gênent dans un enregistrement audio
- ex : "[Son de respiration forte] Alors, où en étions-nous ?"

#### Mouth Clicks (clics de bouche)

- event name : mouth_clicks
- desc : bruits de clic ou autres sons faits avec la bouche, souvent captés par des microphones sensibles
- ex : "[Clic de bouche] Oui, je vois"

#### Long Silences (longs silences)

- event name : long_silences
- desc : pauses prolongées qui ne contribuent pas à la conversation ou qui donne une impression d'inactivité ou de lenteur
- ex : "[Silence de 4 secondes]"
