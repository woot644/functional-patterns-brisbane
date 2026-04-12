"""Generate program pages by reading template and doing byte-level replacement."""
import re

with open('src/programs/bells-and-bands.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

# Extract header (everything up to <!-- Hero -->) and footer (from <!-- Footer --> to end)
header_end = tpl.index('<!-- Hero -->')
header = tpl[:header_end]

footer_start = tpl.index('<!-- Footer -->')
footer = tpl[footer_start:]

# Also extract the CTA section template
cta_start = tpl.index('<!-- CTA -->')
cta_section = tpl[cta_start:footer_start]

programs = {
    'rise-and-realign': {
        'title': 'Rise & Realign — Morning Movement Class | Functional Patterns Brisbane',
        'meta': 'Rise & Realign morning class in Bulimba. Rebuild posture, coordination, and gait mechanics. Wednesdays 6am, 6-week program.',
        'label': '6-Week Program',
        'h1': 'Rise &amp; Realign',
        'h1_accent': 'Morning Class',
        'desc': 'Rebuild posture, coordination, and gait mechanics through structured, biomechanically-driven morning training. This is not a HIIT class.',
        'img': 'training-lunge.jpg',
        'day': 'Wed', 'time': '6:00–7:00 AM', 'price': '$60', 'plabel': 'Per Week',
        'weeks': '6', 'wlabel': 'Weeks', 'size': '10', 'slabel': 'Max Class Size',
        'oh2': 'Calm, Focused Morning Movement',
        'op1': 'Rise &amp; Realign is a 6-week movement class focused on rebuilding posture, coordination, and gait mechanics. Every session is structured and biomechanically-driven — designed to create lasting change, not just a sweat.',
        'op2': 'If you train regularly but still feel tight or unevenly loaded, this class addresses the patterns underneath. Movement that transfers directly into how you walk, stand, and move through your day.',
        'who': [('Tightness Despite Training', 'You train regularly but still feel tight, restricted, or unevenly loaded.'),
                ('Movement That Transfers', 'Exercise that improves daily life movement — not just gym performance.'),
                ('Structured Coaching', 'Precise, progressive coaching over random programming or HIIT.')],
        'includes': ['6 weeks progressive group training (Wednesdays 6–7 AM)', 'Posture, coordination, and gait mechanics', 'Weekly recaps and integration guidance', 'Home practice drills', 'Max 10 participants'],
        'sched': 'Wednesdays 6:00–7:00 AM', 'ptotal': '$360 total ($60/week)',
        'trainer': 'Skye',
        'bio1': 'Skye holds an HBS1 certification in Functional Patterns with 9 years of comprehensive Pilates teaching experience. Her transition to FP came from wanting to address root causes rather than just managing symptoms.',
        'bio2': 'Her calm, methodical approach makes early morning sessions approachable yet effective. Skye builds awareness and control that carries into every aspect of daily life.',
        'cta_h': 'Ready to Rise &amp; Realign?',
        'cta_p': 'Wednesdays at 6am in Bulimba. 6 weeks of structured movement training.',
    },
    'balance-and-symmetry': {
        'title': 'Balance & Symmetry — Corrective Training | Functional Patterns Brisbane',
        'meta': 'Balance & Symmetry corrective training. Address postural imbalances and scoliosis. Wednesdays 6pm, 6-week program in Bulimba.',
        'label': '6-Week Corrective Program',
        'h1': 'Balance &amp;',
        'h1_accent': 'Symmetry',
        'desc': 'Progressive corrective training to restore alignment and address root asymmetries. Myofascial release, gait mechanics, and structured strength work.',
        'img': 'ball-slam.jpg',
        'day': 'Wed', 'time': '6:00–7:00 PM', 'price': '$60', 'plabel': 'Per Week',
        'weeks': '6', 'wlabel': 'Weeks', 'size': '10', 'slabel': 'Max Class Size',
        'oh2': 'Restore Alignment from the Ground Up',
        'op1': 'A progressive 6-week corrective training program addressing root asymmetries rather than symptoms. Each session builds on the last to restore alignment, strength, and efficient movement.',
        'op2': 'Structured weekly progression: Weeks 1-2 myofascial release and foundations. Weeks 3-4 lunge and hinge mechanics. Weeks 5-6 advanced cable correctives and integrated movement.',
        'who': [('Scoliosis &amp; Postural Imbalances', 'Mild scoliosis, visible asymmetry, or postural distortions to address structurally.'),
                ('Uneven Strength', 'One side stronger, tighter, or more dominant despite consistent training.'),
                ('Ages 30-50, Committed', 'Adults ready for 6 weeks of biomechanical retraining.')],
        'includes': ['6 weeks corrective training (Wednesdays 6–7 PM)', 'Structured progression: foundations to advanced', 'Myofascial release and gait mechanics', 'Workbook and homework program', 'Max 10 for personalised correction'],
        'sched': 'Wednesdays 6:00–7:00 PM', 'ptotal': '$360 total ($60/week)',
        'trainer': 'Harj',
        'bio1': 'Harj is a Functional Patterns Specialist with 5 years experience. His analytical approach and attention to detail make him exceptional at identifying subtle asymmetries.',
        'bio2': 'Clients praise his technical skill combined with patience and care. Harj rebuilds movement patterns from the ground up.',
        'cta_h': 'Ready for Balance &amp; Symmetry?',
        'cta_p': 'Wednesdays at 6pm in Bulimba. 6 weeks of corrective training.',
    },
    'functional-fundamentals': {
        'title': 'Functional Fundamentals — Core & Mobility | Functional Patterns Brisbane',
        'meta': 'Functional Fundamentals with Sam. Core stability, mobility, posture refinement. Thursdays 6pm in Bulimba, 6-week program.',
        'label': '6-Week Program',
        'h1': 'Functional',
        'h1_accent': 'Fundamentals',
        'desc': 'Core stability, mobility, and posture refinement without compensations. Integrated drills, glute engagement, myofascial release, and alignment coaching.',
        'img': 'training-posture.jpg',
        'day': 'Thu', 'time': '6:00–7:00 PM', 'price': '$60', 'plabel': 'Per Week',
        'weeks': '6', 'wlabel': 'Weeks', 'size': '10', 'slabel': 'Max Class Size',
        'oh2': 'Build Stability Without Compensations',
        'op1': 'A structured 6-week series to improve functional core stability, unlock mobility, and refine posture — without the compensations of typical fitness classes.',
        'op2': 'Sam guides you through integrated mobility drills, core stability training, glute engagement, and myofascial release. Every exercise is biomechanically sound.',
        'who': [('Tight &amp; Restricted', 'Stuck in compensations despite stretching and regular exercise.'),
                ('Better Posture &amp; Core', 'Core stability beyond planks and crunches.'),
                ('Step-by-Step Coaching', 'Methodical, progressive coaching in a small group.')],
        'includes': ['6 weeks progressive training (Thursdays 6–7 PM)', 'Integrated mobility and core stability', 'Glute engagement and alignment coaching', 'Myofascial release techniques', 'Workbook and take-home exercises'],
        'sched': 'Thursdays 6:00–7:00 PM', 'ptotal': '$360 total ($60/week)',
        'trainer': 'Sam',
        'bio1': 'Sam is a Human Biomechanics Specialist with HBS1 certification and 6 years at FP Brisbane. Known for his wealth of knowledge and holistic approach.',
        'bio2': 'His attention to detail and genuine care sets him apart. Sam ensures you understand not just what to do, but why.',
        'cta_h': 'Ready for Functional Fundamentals?',
        'cta_p': 'Thursdays at 6pm in Bulimba. 6 weeks with Sam.',
    },
    'core-and-mobility': {
        'title': 'Core & Mobility Series | Functional Patterns Brisbane',
        'meta': 'Core & Mobility group program. Build true core function and mobility through functional movement patterns.',
        'label': '6-Week Small Group',
        'h1': 'Core &amp;',
        'h1_accent': 'Mobility',
        'desc': 'Build true core function and improve overall mobility. Ribcage mechanics, hip mobility, stability and control with hands-on correction.',
        'img': 'gait-analysis.jpg',
        'day': 'TBA', 'time': 'Contact for Schedule', 'price': '$360', 'plabel': 'Total',
        'weeks': '6', 'wlabel': 'Weeks', 'size': '10', 'slabel': 'Max Class Size',
        'oh2': 'True Core Function, Real Mobility',
        'op1': 'Goes beyond traditional core training. Learn how your core functions during real movement — walking, rotating, breathing, stabilising under load.',
        'op2': 'Built around ribcage mechanics, hip mobility, and the relationship between stability and control. Hands-on correction every session.',
        'who': [('Core Weakness &amp; Stiffness', 'Core feels weak or disconnected, stiffness limits daily activities.'),
                ('Ribcage &amp; Hip Issues', 'Restricted ribcage or hip mobility affecting posture and movement.'),
                ('Stability &amp; Control', 'Want to feel grounded and in control during movement.')],
        'includes': ['6 weeks progressive group training', 'Ribcage mechanics and hip mobility', 'Hands-on correction every session', 'Functional movement patterns', 'Small group for personalised attention'],
        'sched': 'Contact for next session', 'ptotal': '$360 total',
        'trainer': 'Our Team',
        'bio1': 'Led by our experienced team of FP practitioners. Each holds Cert III &amp; IV in Fitness alongside Functional Patterns certifications.',
        'bio2': 'Focused on biomechanics and motor retraining, ensuring individual attention for lasting progress.',
        'cta_h': 'Ready for Core &amp; Mobility?',
        'cta_p': 'Contact us for the next available 6-week session.',
    },
    'human-foundations': {
        'title': 'Human Foundations Course — 3-Day Intensive | Functional Patterns Brisbane',
        'meta': 'Human Foundations Course: 3-day hands-on intensive. Corrective exercises and dynamic movements. $1,850 USD.',
        'label': '3-Day Intensive Course',
        'h1': 'Human Foundations',
        'h1_accent': 'Course',
        'desc': 'A 3-day in-person intensive building on the FP 10-Week Online Program. Hands-on corrective exercises with personalised feedback.',
        'img': 'posture-assessment.jpg',
        'day': '3', 'time': '9:00 AM – 3:00 PM', 'price': '$1,850', 'plabel': 'USD Total',
        'weeks': '3', 'wlabel': 'Days', 'size': '~30', 'slabel': 'Participants',
        'oh2': 'Hands-On Training with the Experts',
        'op1': 'A 3-day in-person program for individuals and professionals seeking practical tools to correct postural dysfunctions and improve movement.',
        'op2': 'Learn Functional Patterns Corrective Exercises and Dynamic Movements. Led by Fiachra Eviston and Louis Ellery with intensive hands-on practice.',
        'who': [('Fitness Professionals', 'Trainers, physios, coaches wanting corrective movement tools.'),
                ('Athletes', 'Improve performance and prevent injuries through better biomechanics.'),
                ('Personal Transformation', 'Completed 10-Week Online Course, want hands-on expert feedback.')],
        'includes': ['3 full days hands-on (9am–3pm)', 'Led by Fiachra Eviston &amp; Louis Ellery', 'Corrective exercises and dynamic movements', 'Personalised feedback (~30 participants)', 'Course materials and certificate'],
        'sched': 'Contact for upcoming dates', 'ptotal': '$1,850 USD',
        'trainer': 'Louis &amp; Fiachra',
        'bio1': 'Louis Ellery is the owner of FP Brisbane and a Human Biomechanics Specialist. Former physiotherapist who overcame multiple injuries through Functional Patterns.',
        'bio2': 'Fiachra Eviston co-leads with advanced corrective techniques. ~30 participants ensures individual attention.',
        'cta_h': 'Reserve Your Spot',
        'cta_p': 'Email hfcourse@functionalpatterns.com. Prerequisite: FP 10-Week Online Course.',
    },
}

def make_includes_html(items):
    html = ''
    for item in items:
        html += f'''            <li class="flex items-start gap-3">
              <span class="text-accent-500 mt-1 flex-shrink-0">&#10022;</span>
              <span class="text-gray-300">{item}</span>
            </li>\n'''
    return html

def make_who_html(who_list):
    html = ''
    for title, desc in who_list:
        html += f'''        <div class="card-dark">
          <span class="text-accent-500 text-2xl mb-3 block">&#10022;</span>
          <h3 class="text-white font-semibold mb-2">{title}</h3>
          <p class="text-gray-400 text-sm">{desc}</p>
        </div>\n'''
    return html

def make_details_html(p):
    return f'''              <div class="flex justify-between items-center border-b border-white/10 pb-3">
                <span class="text-gray-400">Schedule</span>
                <span class="text-white font-semibold">{p['sched']}</span>
              </div>
              <div class="flex justify-between items-center border-b border-white/10 pb-3">
                <span class="text-gray-400">Duration</span>
                <span class="text-white font-semibold">{p['weeks']} {p['wlabel']}</span>
              </div>
              <div class="flex justify-between items-center border-b border-white/10 pb-3">
                <span class="text-gray-400">Class Size</span>
                <span class="text-white font-semibold">{p['slabel']}: {p['size']}</span>
              </div>
              <div class="flex justify-between items-center border-b border-white/10 pb-3">
                <span class="text-gray-400">Price</span>
                <span class="text-white font-semibold">{p['ptotal']}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Location</span>
                <span class="text-white font-semibold text-right">45 Michael Street<br>Bulimba QLD</span>
              </div>'''

for slug, p in programs.items():
    body = f'''  <!-- Hero -->
  <section class="relative min-h-[60vh] flex items-center bg-dark-950 overflow-hidden pt-20">
    <div class="absolute inset-0">
      <img src="../images/{p['img']}" alt="{p['h1']} at Functional Patterns Brisbane" class="w-full h-full object-cover object-center">
      <div class="absolute inset-0 bg-gradient-to-r from-dark-950 via-dark-950/70 via-[35%] to-transparent"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-dark-950 via-transparent to-dark-950/30"></div>
    </div>
    <div class="relative px-4 sm:px-6 lg:px-8 py-16 sm:py-24 w-full">
      <div class="container-narrow">
        <div class="max-w-2xl">
          <p class="section-label">{p['label']}</p>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-[1.1] mb-6">
            {p['h1']}
            <span class="text-accent-500">{p['h1_accent']}</span>
          </h1>
          <p class="text-lg text-gray-300 mb-10 leading-relaxed max-w-lg">{p['desc']}</p>
          <div class="flex flex-col sm:flex-row gap-4">
            <a href="../book" class="btn-primary text-base py-4 px-8">Enquire Now</a>
            <a href="tel:0433801181" class="btn-outline">Call 0433 801 181</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Stats -->
  <section class="bg-dark-800 border-y border-white/5">
    <div class="container-narrow px-4 py-10 sm:py-12">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
        <div><div class="stat-number">{p['weeks']}</div><div class="stat-label">{p['wlabel']}</div></div>
        <div><div class="stat-number">{p['price']}</div><div class="stat-label">{p['plabel']}</div></div>
        <div><div class="stat-number">{p['size']}</div><div class="stat-label">{p['slabel']}</div></div>
        <div><div class="stat-number">{p['day']}</div><div class="stat-label">{p['time']}</div></div>
      </div>
    </div>
  </section>

  <!-- Overview -->
  <section class="section-dark">
    <div class="container-narrow">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div>
          <p class="section-label">Program Overview</p>
          <h2 class="text-3xl sm:text-4xl font-bold mb-6">{p['oh2']}</h2>
          <p class="text-gray-300 text-lg mb-6 leading-relaxed">{p['op1']}</p>
          <p class="text-gray-300 text-lg leading-relaxed">{p['op2']}</p>
        </div>
        <div><img src="../images/{p['img']}" alt="{p['oh2']}" class="rounded-2xl w-full"></div>
      </div>
    </div>
  </section>

  <!-- Who It's For -->
  <section class="section-charcoal">
    <div class="container-narrow">
      <div class="text-center mb-14">
        <p class="section-label">Is This For You?</p>
        <h2 class="text-3xl sm:text-4xl font-bold">Who This Program Is For</h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{make_who_html(p['who'])}
      </div>
    </div>
  </section>

  <!-- What's Included -->
  <section class="section-dark">
    <div class="container-narrow">
      <div class="grid lg:grid-cols-2 gap-12 items-start">
        <div>
          <p class="section-label">What's Included</p>
          <h2 class="text-3xl sm:text-4xl font-bold mb-8">Everything You Get</h2>
          <ul class="space-y-4">
{make_includes_html(p['includes'])}
          </ul>
        </div>
        <div>
          <div class="card-dark">
            <h3 class="text-white font-bold text-xl mb-6">Program Details</h3>
            <div class="space-y-4">
{make_details_html(p)}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Instructor -->
  <section class="section-charcoal">
    <div class="container-narrow">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div>
          <p class="section-label">Your Instructor</p>
          <h2 class="text-3xl sm:text-4xl font-bold mb-6">Meet {p['trainer']}</h2>
          <p class="text-gray-300 text-lg mb-4 leading-relaxed">{p['bio1']}</p>
          <p class="text-gray-300 text-lg leading-relaxed">{p['bio2']}</p>
        </div>
        <div><img src="../images/posture-assessment.jpg" alt="{p['trainer']} at FP Brisbane" class="rounded-2xl w-full"></div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="relative px-4 sm:px-6 lg:px-8 py-20 sm:py-24 overflow-hidden">
    <div class="absolute inset-0">
      <img src="../images/gait-analysis.jpg" alt="Training" class="w-full h-full object-cover opacity-15">
    </div>
    <div class="relative container-narrow text-center">
      <h2 class="text-3xl sm:text-4xl font-bold mb-4">{p['cta_h']}</h2>
      <p class="text-gray-300 text-lg mb-8 max-w-xl mx-auto">{p['cta_p']}</p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="../book" class="btn-primary text-base py-4 px-8">Enquire Now</a>
        <a href="tel:0433801181" class="btn-phone">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/></svg>
          0433 801 181
        </a>
      </div>
    </div>
  </section>

'''

    # Fix header for sub-pages (title + meta)
    sub_header = header.replace(
        '<title>Bells &amp; Bands \u2014 Women\u2019s Strength Class | Functional Patterns Brisbane</title>',
        f'<title>{p["title"]}</title>'
    ).replace(
        'Ladies-only Bells &amp; Bands class in Bulimba. Core strength and glute activation using dumbbells and resistance bands. Thursdays 10am, 6-week program. Book now.',
        p['meta']
    )

    page = sub_header + body + footer

    with open(f'src/programs/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'Created {slug}.html')

print('Done - all 5 pages')
