"""Generate 9 research summary pages with light educational design."""
import re

# Read a conditions sub-page to get the header/footer with correct ../  paths and dropdowns
with open('src/conditions/chronic-pain.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Extract header up to first <!-- Hero
header_end = source.index('<!-- Hero')
header_tpl = source[:header_end]

# Extract footer from <footer to end
footer_start = source.index('<footer')
footer_tpl = source[footer_start:]

# Fix: conditions dropdown links need to go from /research/ to /conditions/
# Currently they're relative (e.g., href="chronic-pain") which works in /conditions/ but not /research/
header_tpl = header_tpl.replace(
    'href="chronic-pain"', 'href="../conditions/chronic-pain"'
).replace(
    'href="scoliosis"', 'href="../conditions/scoliosis"'
).replace(
    'href="posture-correction"', 'href="../conditions/posture-correction"'
).replace(
    'href="joint-pain"', 'href="../conditions/joint-pain"'
).replace(
    'href="gait-running"', 'href="../conditions/gait-running"'
).replace(
    'href="hunchback-posture"', 'href="../conditions/hunchback-posture"'
).replace(
    'href="winged-scapulas"', 'href="../conditions/winged-scapulas"'
).replace(
    'href="diastasis-recti"', 'href="../conditions/diastasis-recti"'
).replace(
    'href="kids-teens"', 'href="../conditions/kids-teens"'
).replace(
    'href="athletes"', 'href="../conditions/athletes"'
).replace(
    'href="fascia"', 'href="../conditions/fascia"'
)

# Also fix mobile menu conditions links
header_tpl = re.sub(
    r'href="([a-z-]+)" class="block py-2 text-sm text-gray-400',
    lambda m: f'href="../conditions/{m.group(1)}" class="block py-2 text-sm text-gray-400'
    if m.group(1) in ['chronic-pain','scoliosis','posture-correction','joint-pain','gait-running','hunchback-posture','winged-scapulas','diastasis-recti','kids-teens','athletes','fascia']
    else m.group(0),
    header_tpl
)

articles = [
    {
        'slug': 'ankle-foot-mechanics',
        'title': 'Running Propulsion Comes from the Ground Up',
        'meta': 'Why ankle and foot mechanics matter for pain-free gait and posture. Research summary by Louis Ellery.',
        'subtitle': 'Why ankle &amp; foot mechanics matter for pain-free gait and posture',
        'findings': [
            ('Propulsion Source', 'Quadriceps and plantarflexors are key to body-mass propulsion and support during gait and running. These muscles generate the forces that move you forward.'),
            ('Force Transmission', 'Foot and ankle mechanics transmit forces up the kinetic chain. Misalignment or dysfunction at this level propagates upward through the knee, hip, and spine, affecting posture, gait symmetry, and injury risk.'),
            ('The Training Gap', 'Rehabilitation programs focused exclusively on hip and glute strengthening overlook ground-level mechanics, frequently resulting in incomplete or temporary improvements.'),
        ],
        'takeaway': 'An integrated, whole-body approach beginning from the ground up typically outperforms isolated joint or muscle focus. Correcting lower-leg mechanics provides more sustainable results for chronic pain rehabilitation.',
        'citation': 'Hamner SR, Seth A &amp; Delp SL (2010). "Muscle contributions to propulsion and support during running." <em>Journal of Biomechanics</em>. PMC2973845.',
    },
    {
        'slug': 'arm-swing-running',
        'title': 'Active Arm-Swing Reduces Torso Rotation',
        'meta': 'How arm-swing mechanics improve running efficiency and reduce injury risk. Research summary by Louis Ellery.',
        'subtitle': 'Why full-body coordination matters for running stability',
        'findings': [
            ('Reduced Torso Rotation', 'Runners who consciously engaged their arms in proper swing patterns had reduced torso angular motion around the spine\'s longitudinal axis — meaning less torsional stress through hips, pelvis, and spine.'),
            ('Improved Efficiency', 'This reduction in torso rotation improves overall movement efficiency and energy use, translating to less joint wear-and-tear, lower compensatory strain, and improved posture over time.'),
            ('Full-Body Integration', 'The findings support a full-body, integrated movement approach rather than isolating muscles. Coordinating arm-leg-torso patterns significantly influences spinal and lower-body load distribution.'),
        ],
        'takeaway': 'Many rehab protocols overlook arm swing and upper-body coordination when treating lower-body issues. This research shows neglecting upper-body movement perpetuates torsional and alignment stress.',
        'citation': 'Active Arm Swing During Running Improves Rotational Stability and Economy (2025). Available via PubMed Central.',
    },
    {
        'slug': 'hip-internal-rotation',
        'title': 'Limited Hip Internal Rotation &amp; Injury Risk',
        'meta': 'How hip and lower limb alignment affects low back pain risk. 2024 meta-analysis summary by Louis Ellery.',
        'subtitle': 'Association with low back &amp; lower limb injury risk',
        'findings': [
            ('Foot Structure &amp; Back Pain', 'Individuals with flat feet or excessive foot pronation showed significantly elevated risk for low back pain compared to those with normal foot arch structure. Over 100,000 participants were studied.'),
            ('Hip &amp; Knee Alignment', 'The research identified moderate-to-limited evidence linking increased hip internal rotation and knee internal rotation with low back pain development.'),
            ('Dynamic Over Static', 'Many studies examined alignment during walking and stance activities, emphasising that dynamic movement patterns — not just static posture — meaningfully correlate with back problems.'),
        ],
        'takeaway': 'These findings support a kinetic chain perspective: misalignment propagating from lower extremities (ankle to knee to hip to pelvis to spine) contributes to spinal stress and pain. This challenges isolated spine-focused treatment.',
        'citation': 'Abbasi S, Mousavi SH &amp; Khorramroo F (2024). <em>PLOS ONE</em> 19(10): e0311480.',
    },
    {
        'slug': 'gait-retraining-knee-pain',
        'title': 'Gait Retraining Eases Knee Pain',
        'meta': 'Evidence from meta-analysis showing gait retraining reduces knee joint loading and osteoarthritis symptoms.',
        'subtitle': 'Evidence from meta-analysis &amp; recent trials',
        'findings': [
            ('Reduced Knee Loading', 'A 2022 meta-analysis of 18 studies found significant reductions in knee joint loading and osteoarthritis symptoms when patients used gait retraining strategies with real-time feedback.'),
            ('Key Marker Improvement', 'Gait retraining led to meaningful reductions in the external knee adduction moment (EKAM) — the key marker for medial knee load and osteoarthritis risk.'),
            ('Lasting Benefits', 'Participants who adopted biomechanically optimised gait patterns experienced less knee pain, improved function, and reductions in load rates — benefits that endured at follow-up.'),
        ],
        'takeaway': 'The knee is rarely an isolated problem. Knee pain often originates from dysfunctional gait, pelvic/hip misalignment, or poor load distribution. By retraining gait mechanics, clients can reduce knee stress without reliance on medication or surgery.',
        'citation': 'Rynne R et al. (2022). "Effectiveness of gait retraining interventions in individuals with hip or knee osteoarthritis." Systematic review and meta-analysis.',
    },
    {
        'slug': 'movement-vs-standard-exercise',
        'title': 'Movement Retraining Outperforms Standard Exercise',
        'meta': 'Multicentre trial shows movement-based approaches beat standard exercise for chronic low back pain.',
        'subtitle': 'For chronic low back pain management',
        'findings': [
            ('Superior Outcomes', 'Cognitive Functional Therapy (CFT) — which emphasises movement retraining, graduated exposure, and reduced protective guarding — achieved superior improvements in pain, disability, mood, and movement confidence compared to standard exercise.'),
            ('Lasting Change', 'Improvements were sustained at 12-month follow-up, indicating durable, long-term behavioural change rather than temporary relief.'),
            ('Paradigm Shift', 'The research highlighted that changing someone\'s relationship with movement, posture, and breath has more impact than focusing on sets, reps, or isolated strengthening. Pain reduction directly correlated with changes in movement patterns.'),
        ],
        'takeaway': 'Movement retraining produces superior long-term outcomes. Pain is significantly influenced by movement confidence and graduated exposure. Whole-body retraining approaches align with best-practice chronic pain management.',
        'citation': 'Published in <em>British Journal of Sports Medicine</em> 54(13):782. Available at bjsm.bmj.com.',
    },
    {
        'slug': 'diaphragm-spinal-stability',
        'title': 'Diaphragm Position Increases Spinal Stability',
        'meta': 'How intra-abdominal pressure and diaphragm function stabilise the lumbar spine. Research summary.',
        'subtitle': 'The role of abdominal pressure in lumbar spine support',
        'findings': [
            ('Central Stabiliser', 'Intra-abdominal pressure and diaphragm function play a central role in stabilising the spine. When the diaphragm is well-positioned and the ribcage aligned with the pelvis, the body generates pressure that stiffens the lumbar spine.'),
            ('When It Goes Wrong', 'Ribcage flare or collapse causes the diaphragm to lose mechanical leverage. The result: reduced spinal stability, excessive back extensor activity, neck tension, pelvic tilt changes, and inefficient gait mechanics.'),
            ('Not About Bracing', 'Stability is not created by bracing the core or performing isolated abdominal exercises. Instead, stability emerges from breath-driven, 360-degree pressure and harmonious rib-pelvis alignment.'),
        ],
        'takeaway': 'The diaphragm functions as a core stabiliser, not merely a breathing muscle. Ribcage-pelvis alignment drives spinal mechanics. This is why breathing work is central to movement rehabilitation.',
        'citation': 'Published in <em>Spine</em>. Available at pubmed.ncbi.nlm.nih.gov/16023475.',
    },
    {
        'slug': 'gait-hip-pelvis-mechanics',
        'title': 'Gait Retraining Changes Hip &amp; Pelvic Mechanics',
        'meta': 'How targeted gait retraining reduces knee pain by correcting hip and pelvis control during movement.',
        'subtitle': 'How fixing your walk fixes your knee',
        'findings': [
            ('Motor Learning Works', 'Runners with patellofemoral pain received 8 sessions of gait coaching with mirror feedback. The result: reduced hip internal rotation, improved pelvic control, and meaningful pain reductions that persisted weeks later.'),
            ('New Motor Programs', 'The body learned a new motor program — a different way of moving — and pain decreased as a result. This demonstrates that lasting change occurs through motor learning rather than temporary cueing.'),
            ('It\'s Not About the Knee', 'Pelvic drop, hip rotation timing, and trunk mechanics dictate force absorption. When these elements improve through integrated retraining, the knee experiences less overload.'),
        ],
        'takeaway': 'Whole-body gait mechanics directly influence knee pain. Hip and pelvic sequencing outweighs localised knee exercises. Motor learning creates durable improvements that persist after coaching ends.',
        'citation': 'Available at pmc.ncbi.nlm.nih.gov/articles/PMC3501612.',
    },
    {
        'slug': 'fascia-load-adaptation',
        'title': 'Fascia Actively Contracts and Responds to Load',
        'meta': 'Research showing fascia is active contractile tissue that remodels through integrated movement, not stretching.',
        'subtitle': 'Mechanotransduction &amp; whole-body movement',
        'findings': [
            ('Active Tissue', 'Fascia functions as active, contractile tissue — not passive wrapping. Myofibroblasts within fascia generate tension and remodel collagen alignment. This tissue influences how force distributes throughout the body.'),
            ('Directional Load', 'Fascia adapts to directional load, not isolated stretching. The tissue remodels when the body experiences integrated, multi-planar tension that resembles natural movement such as walking, rotating, and maintaining whole-body tension.'),
            ('Interconnected System', 'Fascia links the ribcage, pelvis, and limbs, creating cascading mechanical effects. Restrictions in thoracolumbar fascia affect hip rotation. Pelvic imbalance influences shoulder function. Foot mechanics shape trunk stiffness.'),
        ],
        'takeaway': 'Structural change emerges from load application, not passive stretching. Chronic pain frequently links to fascial stiffness and restricted gliding. Integrated tension training supports fascial adaptation mechanisms.',
        'citation': 'Available at pmc.ncbi.nlm.nih.gov/articles/PMC6455047.',
    },
    {
        'slug': 'motor-control-vs-strengthening',
        'title': 'Motor Control Outperforms Strengthening',
        'meta': 'Systematic review shows motor control retraining beats standard strengthening for chronic low back pain.',
        'subtitle': 'For chronic low back pain resolution',
        'findings': [
            ('Altered Patterns', 'People with persistent pain typically exhibit altered movement patterns: reduced trunk rotation, poor timing between diaphragm and deep core muscles, pelvic compensation, and protective bracing.'),
            ('Coordination Over Strength', 'Motor control training improves coordination and movement sequencing rather than focusing on muscle size or strength. Participants showed greater reductions in pain intensity and disability versus muscle-building alone.'),
            ('Timing, Not Force', 'The deep stabilising system (diaphragm, transversus abdominis, pelvic floor, multifidus) operates based on timing — not maximum force. Getting these muscles to fire in the right sequence matters more than how strong they are.'),
        ],
        'takeaway': 'Chronic pain alters coordination, not just strength. Motor control retraining reduces pain more effectively than strengthening alone. Ribcage-diaphragm-pelvis timing is essential for lasting improvement.',
        'citation': 'Available at pubmed.ncbi.nlm.nih.gov/17060520.',
    },
]

for a in articles:
    # Build page header with correct title
    page_header = re.sub(
        r'<title>.*?</title>',
        f'<title>{a["title"]} | Functional Patterns Brisbane</title>',
        header_tpl
    )
    page_header = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{a["meta"]}">',
        page_header
    )
    # Remove the details/summary CSS that's condition-page specific
    page_header = re.sub(r'  <style>.*?</style>\n', '', page_header, flags=re.DOTALL)

    # Build findings HTML
    findings_html = ''
    for i, (ftitle, fdesc) in enumerate(a['findings']):
        findings_html += f'''
        <div class="bg-blue-50 border border-blue-100 rounded-xl p-6 mb-4">
          <h3 class="text-dark-900 font-semibold text-lg mb-2">{ftitle}</h3>
          <p class="text-gray-700 leading-relaxed">{fdesc}</p>
        </div>'''

    body = f'''<!-- Hero -->
  <section class="bg-dark-950 pt-20">
    <div class="px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
      <div class="container-narrow max-w-3xl">
        <p class="text-accent-500 text-xs font-semibold uppercase tracking-[0.2em] mb-3">Research Summary by Louis Ellery</p>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white leading-tight mb-3">{a['title']}</h1>
        <p class="text-gray-400 text-lg">{a['subtitle']}</p>
      </div>
    </div>
  </section>

  <!-- Article Body — Light Background -->
  <section class="bg-white px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
    <div class="container-narrow max-w-3xl">

      <h2 class="text-dark-900 text-2xl font-bold mb-8">Key Findings</h2>
      {findings_html}

      <div class="mt-12 mb-12">
        <h2 class="text-dark-900 text-2xl font-bold mb-4">What This Means</h2>
        <p class="text-gray-700 text-lg leading-relaxed">{a['takeaway']}</p>
      </div>

      <div class="bg-gray-50 rounded-xl p-6 border border-gray-200">
        <h3 class="text-dark-900 font-semibold text-sm uppercase tracking-wider mb-2">Research Citation</h3>
        <p class="text-gray-600 text-sm leading-relaxed">{a['citation']}</p>
      </div>

    </div>
  </section>

  <!-- CTA -->
  <section class="bg-dark-900 px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
    <div class="container-narrow text-center">
      <p class="text-accent-500 text-xs font-semibold uppercase tracking-[0.2em] mb-3">Apply the Research</p>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mb-4">See How This Applies to Your Body</h2>
      <p class="text-gray-300 mb-8 max-w-xl mx-auto">Book a 90-minute posture and gait assessment to understand how these principles relate to your specific movement patterns.</p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="../book" class="btn-primary">Book an Assessment</a>
        <a href="../results" class="btn-outline">See Our Results</a>
      </div>
    </div>
  </section>

  '''

    page = page_header + body + footer_tpl

    with open(f'src/research/{a["slug"]}.html', 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'Created {a["slug"]}.html')

print(f'Done — {len(articles)} research pages created')
