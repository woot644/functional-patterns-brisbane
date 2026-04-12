"""Generate individual condition pages for What We Treat."""

# Read a root-level page to extract header and footer with correct nav (including dropdowns)
with open('src/what-we-treat.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Extract header (up to first section after header)
header_marker = '<!-- Hero'
header_end = source.index(header_marker)
root_header = source[:header_end]

# Extract footer
footer_marker = '<!-- Footer -->'
if footer_marker not in source:
    footer_marker = '<footer'
footer_start = source.index(footer_marker)
root_footer = source[footer_start:]

# Now create a sub-page header by adjusting paths to ../
sub_header = root_header.replace('href="/', 'href="../').replace('href="how-we-work', 'href="../how-we-work').replace('href="what-we-treat', 'href="../what-we-treat').replace('href="results', 'href="../results').replace('href="programs', 'href="../programs').replace('href="team', 'href="../team').replace('href="book', 'href="../book').replace('href="contact', 'href="../contact').replace('href="online', 'href="../online').replace('href="conditions/', 'href="../conditions/').replace('href="../"', 'href="../"').replace('src="images/', 'src="../images/').replace('href="styles.css"', 'href="../styles.css"')

# Fix double ../
import re
sub_header = sub_header.replace('href="../../', 'href="../')
sub_header = sub_header.replace('href="../tel:', 'href="tel:')
sub_header = sub_header.replace('href="../https://', 'href="https://')

sub_footer = root_footer.replace('href="/', 'href="../').replace('href="how-we-work', 'href="../how-we-work').replace('href="what-we-treat', 'href="../what-we-treat').replace('href="results', 'href="../results').replace('href="programs', 'href="../programs').replace('href="team', 'href="../team').replace('href="book', 'href="../book').replace('href="contact', 'href="../contact').replace('href="online', 'href="../online').replace('href="conditions/', 'href="../conditions/').replace('href="emergency', 'href="../emergency')
sub_footer = sub_footer.replace('href="../tel:', 'href="tel:')
sub_footer = sub_footer.replace('href="../https://', 'href="https://')
sub_footer = sub_footer.replace('href="../mailto:', 'href="mailto:')

conditions = [
    {
        'slug': 'chronic-pain',
        'title': 'Chronic Pain Treatment Brisbane | Functional Patterns Brisbane',
        'meta': 'Resolve chronic back pain, neck pain, and sciatica through biomechanics-based movement training at Functional Patterns Brisbane.',
        'h1': 'Resolve', 'h1_accent': 'Chronic Pain',
        'label': 'Movement-Based Pain Resolution',
        'desc': "Chronic back pain is rarely just a 'back problem.' It's a movement problem. We find the dysfunction causing your pain and retrain your system.",
        'img': 'training-posture.jpg',
        'sections': [
            ("Why Pain Keeps Coming Back", "Most treatments address the symptom site — massage the sore spot, adjust the stiff joint, strengthen the weak muscle. But if the movement pattern that caused the problem hasn't changed, the pain returns.", "At FP Brisbane, we use slow-motion gait and posture analysis filmed from multiple angles to identify the asymmetries and compensations driving your pain. Then we correct them through functional strength training."),
            ("What We Treat", "Chronic back &amp; neck pain, sciatica &amp; nerve pain, post-surgical pain, recurring injuries, headaches, osteoarthritis, and pain that conventional treatments haven't resolved.", ""),
            ("Your Treatment Protocol", "Initial 90-minute assessment with slow-motion gait analysis, followed by 1-2 weekly 60-minute sessions. Training includes corrective exercises, myofascial release, rib-pelvis alignment, hip stability, and breathing mechanics. Progress measured through video analysis.", ""),
        ],
        'testimonial': ("After 15+ years of relentless pain and dysfunction I am close to completely pain free, in an impressive timeframe.", "Kate A"),
    },
    {
        'slug': 'scoliosis',
        'title': 'Scoliosis Treatment Brisbane — Without Surgery | Functional Patterns',
        'meta': 'Straighten your spine without surgery. Functional Patterns Brisbane uses gait analysis and corrective exercise to improve scoliosis.',
        'h1': 'Straighten', 'h1_accent': 'Scoliosis',
        'label': 'Non-Surgical Scoliosis Treatment',
        'desc': "Scoliosis isn't just a 'spine problem' — it's a whole-body movement problem. We use gait analysis and corrective exercise to improve curved spines without bracing or surgery.",
        'img': 'scoliosis-specialist.jpg',
        'sections': [
            ("Our Approach", "We treat scoliosis as a movement dysfunction, not just a structural diagnosis. Through gait analysis, myofascial release, and corrective training, we address the patterns that reinforce spinal curvature.", "Our treatment includes nervous system calming, gait and posture rebuilding, inflammation reduction, dietary protocols, and lifestyle interventions for stress and sleep."),
            ("Who We Help", "Adults with scoliosis and back/neck pain, post-surgery relapse cases, and children and teens with diagnosed scoliosis. Whether your curve is mild or significant, we work to improve symmetry and reduce pain.", ""),
            ("Real Results", "Our practitioners consistently achieve measurable improvements in spinal curvature, symmetry, and pain reduction. One client reduced their lumbar Cobb angle from 27° to 17° in 10 months with daily pain dropping from 7/10 to 0/10.", ""),
        ],
        'testimonial': ("After years of thinking there was nothing I could do to fix my back issues, this training has been hugely rewarding.", "Natalie"),
    },
    {
        'slug': 'posture-correction',
        'title': 'Posture Correction Brisbane | Functional Patterns Brisbane',
        'meta': 'Holistic movement-based posture correction in Brisbane. Address the root cause of poor posture, not just the symptoms.',
        'h1': 'Transform Your', 'h1_accent': 'Posture',
        'label': 'Movement-Based Posture Specialists',
        'desc': "You can't simply pull yourself into good posture. Braces and correctors weaken muscles further. We address WHY your posture is poor through biomechanical retraining.",
        'img': 'lordotic-kyphotic.jpg',
        'sections': [
            ("Why Posture Matters", "Correct posture means reduced pain through even weight distribution, improved breathing and lung capacity, increased energy through better circulation, improved digestion, and enhanced confidence and mental wellbeing.", ""),
            ("Our Approach", "We identify WHY posture is poor rather than forcing alignment. Your body positioning during walking, sitting, sleeping, and running creates cumulative misalignments. Like a Jenga tower — gravity acts on us all, and we need our muscles, joints, and bones stacked correctly.", "Breathing patterns also determine body structure. We assess whether to increase or decrease pressure in specific areas based on your individual mechanics."),
            ("Case Studies", "Matt: 8 months, went from chronic pain head-to-toe to completely pain-free. Natalie: 13 months, scoliosis pain from 8/10 to pain-free. Louis: 3-year transformation including 6kg muscle gain and complete pain elimination.", ""),
        ],
        'testimonial': ("After 8 months I can now move better, with more tension in my body and I'm completely pain free. Best I've ever felt in my life.", "Matt"),
    },
    {
        'slug': 'joint-pain',
        'title': 'Joint Pain Treatment Brisbane | Functional Patterns Brisbane',
        'meta': 'Fix hip, knee, shoulder and joint pain through movement correction at Functional Patterns Brisbane.',
        'h1': "It's a", 'h1_accent': 'Joint Effort',
        'label': 'Hip, Knee &amp; Shoulder Pain',
        'desc': "Joint pain comes from things rubbing on things that they shouldn't and leaning on things that they shouldn't. We find the dysfunctional patterns and fix them.",
        'img': 'training-lunge.jpg',
        'sections': [
            ("Our Approach", "Many people assume they have to either live with joint pain or stop exercising. We take a different approach — using targeted exercise to activate proper muscles and movement pathways so you can gain muscle while reducing pain.", ""),
            ("Conditions We Address", "Sports-related joint and knee pain, early degenerative hip disease, groin injuries, chronic shoulder pain, sacroiliac joint (SIJ) pain, pelvic floor dysfunction, and general chronic joint pain.", ""),
            ("Real Results", "Emma: overcame basketball injuries, pain-free within months. Charma: avoided hip replacement surgery, eliminated chronic hip pain after 17 months. Sivert: resolved groin injury in 3-4 sessions after six months of unsuccessful physio.", ""),
        ],
        'testimonial': ("Having worked with the team at FP Brisbane has changed my pain and mobility — without surgery! I can walk and exercise without pain.", "Nic"),
    },
    {
        'slug': 'gait-running',
        'title': 'Gait Analysis &amp; Running Brisbane | Functional Patterns Brisbane',
        'meta': 'Improve your gait cycle to decrease pain and reduce injury rate. Professional gait analysis at Functional Patterns Brisbane.',
        'h1': 'Improve Your', 'h1_accent': 'Gait &amp; Running',
        'label': 'Gait Cycle Optimisation',
        'desc': "If you could move with elite athleticism — running, walking, throwing efficiently — chronic pain would likely resolve. We optimise your gait to make that happen.",
        'img': 'gait-analysis.jpg',
        'sections': [
            ("How Gait Analysis Works", "When you run, problems become apparent: excessive dropping at impact, stiffness in specific areas, spinal curvature changes, and failure to rotate properly. We film from multiple angles in slow motion to identify every dysfunction.", ""),
            ("The Big Four", "We optimise four functions that form our biological blueprint: standing, walking, running, and throwing. Get good at these and watch your entire life change. We deconstruct elite movement mechanics and create corrective exercises targeting your specific dysfunctional points.", ""),
            ("Measurable Results", "Professional athlete: improved speed by 4.4 km/h with 4kg muscle gain in 6 months. Sciatica client: progressed from unable to run to running pain-free at 25 km/h. Cricket player: eliminated chronic knee, hip, neck and shoulder pain.", ""),
        ],
        'testimonial': ("Thanks to Louis and his training methods, I am now moving better, faster and with less pain than I ever have before.", "Aryan Jain"),
    },
    {
        'slug': 'hunchback-posture',
        'title': 'Hunchback Posture Treatment Brisbane | Functional Patterns',
        'meta': 'Fix hunchback posture (kyphosis) through movement-based treatment at Functional Patterns Brisbane. Not exercises — real structural change.',
        'h1': 'Fix', 'h1_accent': 'Hunchback Posture',
        'label': 'Kyphosis &amp; Thoracic Rounding',
        'desc': "Posture isn't a position. It's the result of how your body moves. Traditional exercises don't create lasting structural change because they don't rewire movement patterns.",
        'img': 'straighten-back.jpg',
        'sections': [
            ("What Is Hunchback Posture?", "Excessive thoracic kyphosis involving a rounded upper back, collapsed chest, forward head posture, ribcage compression, and upper/mid-back stiffness. Common causes include sedentary work, reduced natural movement, repetitive gym training, and injuries.", ""),
            ("Why Standard Treatments Fail", "Back strengthening, core stability, stretching, and ergonomic adjustments provide temporary relief but don't create lasting structural change. Isolated muscle work doesn't rewire movement patterns. The root causes are poor spine alignment during movement, loss of thoracic extension in gait, and ribcage compression.", ""),
            ("Our Treatment", "Three components: comprehensive posture and gait assessment, targeted retraining integrated into daily movement, and long-term integration addressing real-world demands — sitting, walking, training, working, and stress.", ""),
        ],
        'testimonial': ("I feel I have gained a sense of purpose and drive to develop and maintain better mobility, strength, and balance well into my older age.", "Irenie"),
    },
    {
        'slug': 'winged-scapulas',
        'title': 'Winged Scapula Correction Brisbane | Functional Patterns',
        'meta': 'Fix winged scapulas through integrated gait-based movement training at Functional Patterns Brisbane.',
        'h1': 'Correct', 'h1_accent': 'Winged Scapulas',
        'label': 'Scapular Dyskinesis',
        'desc': "Scapular winging occurs when muscles fail to integrate properly. We correct it through gait training — not isolated shoulder exercises.",
        'img': 'ball-slam.jpg',
        'sections': [
            ("What Causes Winging?", "When muscles fail to integrate, the scapula sits off the back and wings. Key muscles involved include the lats, levator scapulae, and trapezius. Over time, incorrect movement patterns deactivate certain muscles while overusing others. Rib cage compression from breathing dysfunction is another major contributor.", ""),
            ("Our Approach", "Learning to move your spine and rotate correctly during movement is a major factor in correcting scapular winging. We focus on gait training — standing, walking, and running mechanics — because these fundamental patterns reveal the real muscle imbalances.", "Integrating the body using the gait cycle as a guide consistently corrects winged scapulas."),
            ("Case Studies", "Kynan: achieved perfectly positioned shoulder blades using only FP techniques. Vanessa: 18 months, resolved nerve pain and winging. Murphy: 18 months, resolved persistent cricket bowling injury, now bowls faster and longer without pain.", ""),
        ],
        'testimonial': ("Coming back into bowling after that break there was a dramatic increase in comfort and overall ability to bowl.", "Murphy"),
    },
    {
        'slug': 'diastasis-recti',
        'title': 'Diastasis Recti Treatment Brisbane | Functional Patterns',
        'meta': "Diastasis recti isn't about weak abs — it's about pressure and movement patterns. Functional Patterns Brisbane can help.",
        'h1': 'Heal', 'h1_accent': 'Diastasis Recti',
        'label': 'Pressure &amp; Movement Patterns',
        'desc': "Diastasis recti and coning aren't about weak abs — they're about pressure and movement sequencing. You can have strong abs and still have diastasis because strength doesn't equal integration.",
        'img': 'training-posture.jpg',
        'sections': [
            ("What Diastasis Actually Is", "Not muscle separation — it's a pressure and movement sequencing problem. The separation results from dysfunction in rib cage positioning, pelvic orientation, diaphragm and core coordination, torso rotation, and load transfer during walking and standing.", ""),
            ("Our 6-Part Approach", "1) Rib cage position — restore internal tension without gripping. 2) Pelvic orientation — return neutral relationship with rib cage. 3) Diaphragm-TVA coordination — reintroduce natural pressurisation. 4) Oblique and sling integration. 5) Gait sequencing — retrain how ribs, pelvis, and feet coordinate. 6) Real-world movement tolerance.", ""),
            ("Pregnancy &amp; Postpartum", "During pregnancy: managing pressure changes, minimising coning, safe load handling. Postpartum: restoring tension through diaphragm coordination, sling system reinforcement, and progressive loading back to running or strength training.", ""),
        ],
        'testimonial': ("I no longer have pain in my left shoulder from other HIIT programs. I won't be seeing anyone else but FP for health, fitness or recovery ever again.", "Kathy"),
    },
    {
        'slug': 'kids-teens',
        'title': 'Kids &amp; Teens Biomechanics Brisbane | Functional Patterns',
        'meta': 'Biomechanics and posture training for children and teenagers at Functional Patterns Brisbane.',
        'h1': 'Kids &amp;', 'h1_accent': 'Teenagers',
        'label': 'Youth Biomechanics',
        'desc': "Catch structural issues early, address conditions like cerebral palsy, and improve athleticism, coordination and speed — all while their bodies are most adaptable.",
        'img': 'fp-brisbane-training.jpg',
        'sections': [
            ("Why Start Young?", "Children have a cleaner slate — fewer injuries and poor patterns. Higher neuroplasticity means their brains learn motor skills faster. Lower body mass makes movement learning easier. Less inhibition means they experiment more freely.", ""),
            ("What We Address", "Postural issues caught early before they become pain. Conditions like cerebral palsy and Scheuermann's kyphosis. Athletic performance — sprint speed, coordination, technique. Scapular winging and core development.", ""),
            ("Case Studies", "Xavier (age 9): core, posture, and scapular winging improvements in 10 weeks. Matthew (14): Scheuermann's kyphosis management with posture and self-confidence gains. Young gymnast: speed and technique improvements in just 2 sessions.", ""),
        ],
        'testimonial': ("The team at FP Brisbane have changed my life! I simply can't recommend FP Brisbane enough.", "Nic"),
    },
    {
        'slug': 'athletes',
        'title': 'Biomechanics for Athletes Brisbane | Functional Patterns',
        'meta': 'Improve athletic performance, speed, and injury prevention through biomechanics training at Functional Patterns Brisbane.',
        'h1': 'Athletes &amp;', 'h1_accent': 'Performance',
        'label': 'Speed, Power &amp; Longevity',
        'desc': "We improve the performance, speed and longevity of athletes by improving their biomechanics and gait cycle. Correcting dysfunction decreases injury rates while enhancing speed and efficiency.",
        'img': 'ball-slam.jpg',
        'sections': [
            ("Our Method", "Rather than copying how elite athletes train, we deconstruct their movement mechanics. We create corrective exercises targeting dysfunctional points combined with myofascial release. The methodology focuses on optimising the Big Four: standing, walking, running, and throwing.", ""),
            ("Notable Athletes", "Matthew Renshaw (professional cricketer): resolved chronic knee, hip, neck, and shoulder pain. James Bazley (cricketer): +4.4 km/h sprint speed, +4kg muscle, zero missed matches over 2 years. Aryan Jain: +4 km/h sprint speed, selected for Queensland 2nd XI.", ""),
            ("Measurable Gains", "Lewis (soccer): +3 km/h sprint speed (26→29), eliminated back pain. Brandon (cricket): eliminated shin splints, shoulder and neck pain, +3.5 km/h sprint speed, improved scoliosis management.", ""),
        ],
        'testimonial': ("Thanks to Louis and his training methods, I am now moving better, faster and with less pain than I ever have before.", "Aryan Jain"),
    },
    {
        'slug': 'fascia',
        'title': 'Fascia &amp; Chronic Fatigue Treatment Brisbane | Functional Patterns',
        'meta': 'The little-known solution to chronic pain, inflammation, and fatigue. Functional Patterns Brisbane addresses fascia through movement.',
        'h1': 'Fascia &amp;', 'h1_accent': 'Chronic Conditions',
        'label': 'Chronic Pain, Fatigue &amp; Inflammation',
        'desc': "Fascia forms a continuum throughout your body, transmitting information that influences body shape and function. Dysfunction in fascia drives chronic pain, fatigue, and inflammation.",
        'img': 'fascia-tension.jpg',
        'sections': [
            ("What Is Fascia?", "Tissue that responds to mechanical stimuli — forming a continuum that supports, divides, and connects body districts while transmitting mechano-metabolic information. It influences chronic pain, inflammation, fatigue, lymph flow, immune function, and even emotional stability.", ""),
            ("Fascia &amp; Movement", "When you move dysfunctionally, fascia adapts to those patterns — creating adhesions, restrictions, and pain. Functional Patterns emphasises natural human movements (standing, walking, running, throwing) to restore fascial health.", "We find that popular exercises like barbell deadlifts and back squats can reinforce dysfunction. Gait-based corrections restore the fascial system more effectively."),
            ("Conditions Influenced", "Chronic pain and inflammation, chronic fatigue and fibromyalgia, lymph flow and immune dysfunction, osteoporosis, digestive issues, body dysmorphia, and emotional instability.", ""),
        ],
        'testimonial': ("Functional Patterns Brisbane has, quite honestly, been life changing. They were able to give me a life back.", "Moto_Monk"),
    },
]

def make_section(title, p1, p2):
    html = f'''
  <section class="section-dark">
    <div class="container-narrow">
      <div class="max-w-3xl mx-auto">
        <h2 class="text-2xl sm:text-3xl font-bold mb-6">{title}</h2>
        <p class="text-gray-300 text-lg mb-4 leading-relaxed">{p1}</p>'''
    if p2:
        html += f'''
        <p class="text-gray-300 text-lg leading-relaxed">{p2}</p>'''
    html += '''
      </div>
    </div>
  </section>'''
    return html

def make_section_alt(title, p1, p2):
    html = f'''
  <section class="section-charcoal">
    <div class="container-narrow">
      <div class="max-w-3xl mx-auto">
        <h2 class="text-2xl sm:text-3xl font-bold mb-6">{title}</h2>
        <p class="text-gray-300 text-lg mb-4 leading-relaxed">{p1}</p>'''
    if p2:
        html += f'''
        <p class="text-gray-300 text-lg leading-relaxed">{p2}</p>'''
    html += '''
      </div>
    </div>
  </section>'''
    return html

for c in conditions:
    # Build the page body
    sections_html = ''
    for i, (title, p1, p2) in enumerate(c['sections']):
        if i % 2 == 0:
            sections_html += make_section(title, p1, p2)
        else:
            sections_html += make_section_alt(title, p1, p2)

    body = f'''<!-- Hero -->
  <section class="relative min-h-[60vh] flex items-center bg-dark-950 overflow-hidden pt-20">
    <div class="absolute inset-0">
      <img src="../images/{c['img']}" alt="{c['h1']} {c['h1_accent']} at Functional Patterns Brisbane" class="w-full h-full object-cover object-center opacity-40">
      <div class="absolute inset-0 bg-gradient-to-r from-dark-950 via-dark-950/70 via-[35%] to-transparent"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-dark-950 via-transparent to-dark-950/30"></div>
    </div>
    <div class="relative px-4 sm:px-6 lg:px-8 py-16 sm:py-24 w-full">
      <div class="container-narrow">
        <div class="max-w-2xl">
          <p class="section-label">{c['label']}</p>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-[1.1] mb-6">
            {c['h1']}
            <span class="text-accent-500">{c['h1_accent']}</span>
          </h1>
          <p class="text-lg text-gray-300 mb-10 leading-relaxed max-w-lg">{c['desc']}</p>
          <div class="flex flex-col sm:flex-row gap-4">
            <a href="../book" class="btn-primary text-base py-4 px-8">Book an Assessment</a>
            <a href="tel:0433801181" class="btn-outline">Call 0433 801 181</a>
          </div>
        </div>
      </div>
    </div>
  </section>

{sections_html}

  <!-- Testimonial -->
  <section class="section-light">
    <div class="container-narrow">
      <div class="max-w-3xl mx-auto text-center">
        <div class="flex justify-center gap-1 mb-6">
          <span class="text-accent-500 text-xl">&#9733;</span><span class="text-accent-500 text-xl">&#9733;</span><span class="text-accent-500 text-xl">&#9733;</span><span class="text-accent-500 text-xl">&#9733;</span><span class="text-accent-500 text-xl">&#9733;</span>
        </div>
        <blockquote class="text-dark-900 text-xl font-medium italic leading-relaxed mb-6">"{c['testimonial'][0]}"</blockquote>
        <p class="text-gray-600 font-semibold">— {c['testimonial'][1]}, Verified Google Review</p>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="relative px-4 sm:px-6 lg:px-8 py-20 sm:py-24 overflow-hidden">
    <div class="absolute inset-0">
      <img src="../images/gait-analysis.jpg" alt="Training" class="w-full h-full object-cover opacity-15">
    </div>
    <div class="relative container-narrow text-center">
      <p class="section-label">Ready to Start?</p>
      <h2 class="text-3xl sm:text-4xl font-bold mb-4">Book Your Assessment</h2>
      <p class="text-gray-300 text-lg mb-8 max-w-xl mx-auto">90 minutes to understand exactly why your pain exists, which patterns drive it, and what needs to change.</p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="../book" class="btn-primary text-base py-4 px-8">Book an Assessment</a>
        <a href="tel:0433801181" class="btn-phone">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/></svg>
          0433 801 181
        </a>
      </div>
    </div>
  </section>

  '''

    # Adjust header for this page's title
    page_header = sub_header.replace(
        '<title>What We Treat',
        f'<title>{c["title"]}'
    ).replace(
        'what-we-treat" class="nav-link text-white">',
        'what-we-treat" class="nav-link">'
    )
    # Fix meta description
    page_header = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{c["meta"]}">',
        page_header
    )

    page = page_header + body + sub_footer

    with open(f'src/conditions/{c["slug"]}.html', 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'Created {c["slug"]}.html')

print(f'Done — {len(conditions)} condition pages created')
