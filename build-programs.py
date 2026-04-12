"""Generate program sub-pages from bells-and-bands template."""
import os

with open('src/programs/bells-and-bands.html', 'r', encoding='utf-8') as f:
    template = f.read()

programs = [
    {
        'filename': 'rise-and-realign.html',
        'title': 'Rise &amp; Realign',
        'meta_title': 'Rise &amp; Realign — Morning Movement Class | Functional Patterns Brisbane',
        'meta_desc': 'Rise and Realign morning movement class in Bulimba. Rebuild posture, coordination, and gait mechanics. Wednesdays 6am, 6-week program.',
        'label': '6-Week Program',
        'h1_1': 'Rise &amp; Realign', 'h1_2': 'Morning Class',
        'hero_desc': 'Rebuild posture, coordination, and gait mechanics through structured, biomechanically-driven morning training. This is not a HIIT class.',
        'hero_img': 'training-lunge.jpg',
        'stat_day': 'Wed', 'stat_time': '6:00\u20137:00 AM',
        'price_per': '$60', 'price_label': 'Per Week',
        'weeks': '6', 'weeks_label': 'Weeks',
        'class_size': '10', 'class_label': 'Max Class Size',
        'overview_h2': 'Calm, Focused Morning Movement',
        'overview_p1': 'Rise &amp; Realign is a 6-week movement class focused on rebuilding posture, coordination, and gait mechanics. Every session is structured and biomechanically-driven \u2014 designed to create lasting change, not just a sweat.',
        'overview_p2': "If you're someone who trains regularly but still feels tight or unevenly loaded, this class addresses the patterns underneath. You'll learn movement that transfers directly into how you walk, stand, and move through your day.",
        'who': [
            ('Tightness Despite Training', 'You train regularly but still feel tight, restricted, or unevenly loaded through your body.'),
            ('Movement That Transfers', 'You want exercise that improves how you move in daily life \u2014 not just how you perform in a gym.'),
            ('Structured Coaching', 'You prefer precise, progressive coaching over random programming or high-intensity workouts.'),
        ],
        'includes': [
            '6 weeks of progressive group training (Wednesdays 6:00\u20137:00 AM)',
            'Posture, coordination, and gait mechanics training',
            'Weekly recaps and integration guidance',
            'Minimal-equipment drills for home practice',
            'Small class of max 10 participants for personalised attention',
        ],
        'schedule_line': 'Wednesdays 6:00\u20137:00 AM',
        'price_total': '$360 total ($60/week)',
        'instructor': 'Skye',
        'bio1': 'Skye holds an HBS1 certification in Functional Patterns, bringing 9 years of comprehensive Pilates teaching experience to her practice. Her transition to Functional Patterns came from wanting to address root causes of movement dysfunction rather than just managing symptoms.',
        'bio2': 'Her calm, methodical approach makes the early morning sessions approachable yet effective. Skye focuses on building awareness and control that carries into every aspect of daily life.',
        'cta_h2': 'Ready to Rise &amp; Realign?',
        'cta_p': 'Wednesdays at 6am in Bulimba. 6 weeks of structured movement training to rebuild your posture and coordination.',
    },
    {
        'filename': 'balance-and-symmetry.html',
        'title': 'Balance &amp; Symmetry',
        'meta_title': 'Balance &amp; Symmetry — Corrective Training | Functional Patterns Brisbane',
        'meta_desc': 'Balance and Symmetry corrective training in Bulimba. Address postural imbalances, scoliosis, and asymmetries. Wednesdays 6pm, 6-week program.',
        'label': '6-Week Corrective Program',
        'h1_1': 'Balance &amp;', 'h1_2': 'Symmetry',
        'hero_desc': 'Progressive corrective training to restore alignment and address root asymmetries. Myofascial release, gait mechanics, and structured strength work.',
        'hero_img': 'ball-slam.jpg',
        'stat_day': 'Wed', 'stat_time': '6:00\u20137:00 PM',
        'price_per': '$60', 'price_label': 'Per Week',
        'weeks': '6', 'weeks_label': 'Weeks',
        'class_size': '10', 'class_label': 'Max Class Size',
        'overview_h2': 'Restore Alignment from the Ground Up',
        'overview_p1': 'Balance &amp; Symmetry is a progressive 6-week corrective training program that addresses root asymmetries rather than symptoms. Using Functional Patterns methodology, each session builds on the last to restore alignment, strength, and efficient movement.',
        'overview_p2': 'The program follows a structured weekly progression: Weeks 1-2 focus on myofascial release, neutral stance, and foundational planks. Weeks 3-4 introduce lunge and hinge mechanics. Weeks 5-6 advance to cable correctives and integrated movement.',
        'who': [
            ('Scoliosis &amp; Postural Imbalances', 'You have mild scoliosis, visible asymmetry, or postural distortions you want to address structurally.'),
            ('Uneven Strength', 'You feel uneven despite consistent training \u2014 one side stronger, tighter, or more dominant.'),
            ('Ages 30-50, Committed', 'Adults ready to commit to 6 weeks of biomechanical retraining for lasting structural change.'),
        ],
        'includes': [
            '6 weeks of progressive corrective training (Wednesdays 6:00\u20137:00 PM)',
            'Structured weekly progression from foundations to advanced correctives',
            'Myofascial release and gait mechanics work',
            'Comprehensive workbook and homework program',
            'Small class of max 10 for personalised correction',
        ],
        'schedule_line': 'Wednesdays 6:00\u20137:00 PM',
        'price_total': '$360 total ($60/week)',
        'instructor': 'Harj',
        'bio1': 'Harj is a Functional Patterns Specialist with 5 years of training experience. His analytical approach and keen attention to detail make him exceptional at identifying and correcting subtle asymmetries that other practitioners miss.',
        'bio2': "Clients consistently praise his technical skill combined with patience and care. Harj rebuilds movement patterns from the ground up, ensuring each correction is understood and integrated before progressing.",
        'cta_h2': 'Ready for Balance &amp; Symmetry?',
        'cta_p': 'Wednesdays at 6pm in Bulimba. 6 weeks of progressive corrective training to restore your alignment.',
    },
    {
        'filename': 'functional-fundamentals.html',
        'title': 'Functional Fundamentals',
        'meta_title': 'Functional Fundamentals — Core &amp; Mobility | Functional Patterns Brisbane',
        'meta_desc': 'Functional Fundamentals with Sam. Core stability, mobility, and posture refinement. Thursdays 6pm in Bulimba, 6-week program.',
        'label': '6-Week Program',
        'h1_1': 'Functional', 'h1_2': 'Fundamentals',
        'hero_desc': 'Core stability, mobility, and posture refinement without compensations. Integrated drills, glute engagement, myofascial release, and alignment coaching.',
        'hero_img': 'training-posture.jpg',
        'stat_day': 'Thu', 'stat_time': '6:00\u20137:00 PM',
        'price_per': '$60', 'price_label': 'Per Week',
        'weeks': '6', 'weeks_label': 'Weeks',
        'class_size': '10', 'class_label': 'Max Class Size',
        'overview_h2': 'Build Stability Without Compensations',
        'overview_p1': "Functional Fundamentals is a structured 6-week series designed to improve functional core stability, unlock mobility, and refine posture \u2014 all without the compensations and wear-and-tear of typical fitness classes.",
        'overview_p2': 'Using Functional Patterns principles, Sam guides you through integrated mobility drills, core stability training, glute engagement work, and myofascial release. Every exercise is biomechanically sound and builds toward real-world movement competency.',
        'who': [
            ('Tight &amp; Restricted', 'You feel tight, restricted, or stuck in compensations despite stretching and regular exercise.'),
            ('Better Posture &amp; Core', 'You want improved posture and core stability that goes beyond planks and crunches.'),
            ('Step-by-Step Coaching', 'You prefer methodical, progressive coaching in a small group rather than generic fitness classes.'),
        ],
        'includes': [
            '6 weeks of progressive training (Thursdays 6:00\u20137:00 PM)',
            'Integrated mobility drills and core stability work',
            'Glute engagement and alignment coaching',
            'Myofascial release techniques',
            'Comprehensive workbook and take-home exercises',
        ],
        'schedule_line': 'Thursdays 6:00\u20137:00 PM',
        'price_total': '$360 total ($60/week)',
        'instructor': 'Sam',
        'bio1': 'Sam is a Human Biomechanics Specialist with HBS1 certification and 6 years of experience at Functional Patterns Brisbane. Known for his wealth of knowledge and holistic approach, Sam addresses health as a complex, multifactorial puzzle.',
        'bio2': "His attention to detail and genuine care for each client's progress sets him apart. Sam ensures every participant understands not just what to do, but why \u2014 building the body awareness that makes change last.",
        'cta_h2': 'Ready for Functional Fundamentals?',
        'cta_p': 'Thursdays at 6pm in Bulimba. 6 weeks of core stability, mobility, and posture refinement with Sam.',
    },
    {
        'filename': 'core-and-mobility.html',
        'title': 'Core &amp; Mobility',
        'meta_title': 'Core &amp; Mobility Series | Functional Patterns Brisbane',
        'meta_desc': 'Core and Mobility group program at Functional Patterns Brisbane. Build true core function and improve mobility through functional movement patterns.',
        'label': '6-Week Small Group Program',
        'h1_1': 'Core &amp;', 'h1_2': 'Mobility',
        'hero_desc': 'Build true core function and improve overall mobility through functional movement patterns. Focused on ribcage mechanics, hip mobility, stability and control.',
        'hero_img': 'gait-analysis.jpg',
        'stat_day': 'TBA', 'stat_time': 'Contact for Schedule',
        'price_per': '$360', 'price_label': 'Total',
        'weeks': '6', 'weeks_label': 'Weeks',
        'class_size': '10', 'class_label': 'Max Class Size',
        'overview_h2': 'True Core Function, Real Mobility',
        'overview_p1': "The Core &amp; Mobility Series goes beyond traditional core training. Instead of isolated exercises, you'll learn how your core actually functions during real movement \u2014 walking, rotating, breathing, and stabilising under load.",
        'overview_p2': "This program is built around ribcage mechanics, hip mobility, and the relationship between stability and control. Every session includes hands-on correction to ensure you're moving correctly, not just moving more.",
        'who': [
            ('Core Weakness &amp; Stiffness', 'Your core feels weak or disconnected, and stiffness limits how well you can move through daily activities.'),
            ('Ribcage &amp; Hip Issues', 'You have restricted ribcage mobility or hip stiffness that affects your posture and movement quality.'),
            ('Stability &amp; Control', 'You want to feel more stable, grounded, and in control of your body during movement and exercise.'),
        ],
        'includes': [
            '6 weeks of progressive group training',
            'Ribcage mechanics and hip mobility work',
            'Hands-on correction in every session',
            'Functional movement pattern training',
            'Small group format for personalised attention',
        ],
        'schedule_line': 'Contact for next available session',
        'price_total': '$360 total',
        'instructor': 'Our Team',
        'bio1': 'The Core &amp; Mobility Series is led by our experienced team of Functional Patterns practitioners. Each trainer holds at minimum Cert III &amp; IV in Fitness alongside their Functional Patterns certifications.',
        'bio2': 'With a focus on biomechanics and motor retraining, our practitioners ensure every participant receives the individual attention needed to make lasting progress in core function and mobility.',
        'cta_h2': 'Ready for Core &amp; Mobility?',
        'cta_p': '6 weeks of focused core and mobility training in a small group setting. Contact us for the next available session.',
    },
    {
        'filename': 'human-foundations.html',
        'title': 'Human Foundations Course',
        'meta_title': 'Human Foundations Course — 3-Day Intensive | Functional Patterns Brisbane',
        'meta_desc': 'Human Foundations Course: 3-day hands-on intensive with Functional Patterns. Learn corrective exercises and dynamic movements. $1,850 USD.',
        'label': '3-Day Intensive Course',
        'h1_1': 'Human Foundations', 'h1_2': 'Course',
        'hero_desc': 'A 3-day in-person intensive building on the FP 10-Week Online Program. Hands-on corrective exercises and dynamic movements with personalised feedback.',
        'hero_img': 'posture-assessment.jpg',
        'stat_day': '3', 'stat_time': '9:00 AM \u2013 3:00 PM',
        'price_per': '$1,850', 'price_label': 'USD Total',
        'weeks': '3', 'weeks_label': 'Days',
        'class_size': '~30', 'class_label': 'Participants',
        'overview_h2': 'Hands-On Training with the Experts',
        'overview_p1': "The Human Foundations Course is a 3-day in-person program that builds on the Functional Patterns 10-Week Online Program. It's designed for both individuals and professionals seeking practical tools to correct postural dysfunctions and improve movement.",
        'overview_p2': "Over three days, you'll learn to apply Functional Patterns Corrective Exercises and Dynamic Movements to resolve common postural and movement dysfunctions. Led by Fiachra Eviston and Louis Ellery, the course combines theory with intensive hands-on practice.",
        'who': [
            ('Fitness Professionals', 'Trainers, physiotherapists, and coaches who want to add corrective movement tools to their practice.'),
            ('Athletes', 'Athletes seeking to improve performance and prevent injuries through better biomechanics.'),
            ('Personal Transformation', "Anyone who's completed the 10-Week Online Course and wants hands-on learning with expert feedback."),
        ],
        'includes': [
            '3 full days of hands-on training (9am\u20133pm daily)',
            'Led by Fiachra Eviston &amp; Louis Ellery',
            'Corrective exercises and dynamic movement instruction',
            'Personalised feedback (~30 participants)',
            'Access to course materials',
            'Certificate of completion',
        ],
        'schedule_line': 'Contact for upcoming dates',
        'price_total': '$1,850 USD',
        'instructor': 'Louis &amp; Fiachra',
        'bio1': 'Louis Ellery is the owner of Functional Patterns Brisbane and a Human Biomechanics Specialist. A former physiotherapist who overcame multiple injuries through Functional Patterns, Louis brings deep expertise in chronic pain resolution and movement optimisation.',
        'bio2': 'Fiachra Eviston co-leads the course, bringing complementary skills in advanced corrective techniques. Together, they create an intensive learning environment with approximately 30 participants ensuring individual attention and tailored guidance.',
        'cta_h2': 'Reserve Your Spot',
        'cta_p': 'Contact hfcourse@functionalpatterns.com for upcoming dates. Prerequisites: completion of the FP 10-Week Online Course.',
    },
]

for p in programs:
    page = template

    # Head
    page = page.replace(
        '<title>Bells &amp; Bands \u2014 Women\u2019s Strength Class | Functional Patterns Brisbane</title>',
        f'<title>{p["meta_title"]}</title>'
    )
    page = page.replace(
        'Ladies-only Bells &amp; Bands class in Bulimba. Core strength and glute activation using dumbbells and resistance bands. Thursdays 10am, 6-week program. Book now.',
        p['meta_desc']
    )

    # Hero label
    page = page.replace('Ladies Only &bull; 6-Week Program', p['label'])
    # Hero image
    page = page.replace('kettlebell-swing.jpg" alt="Women\'s Bells and Bands strength class at Functional Patterns Brisbane"', f'{p["hero_img"]}" alt="{p["title"]} at Functional Patterns Brisbane"')
    # H1
    page = page.replace(
        'Bells &amp; Bands\n            <span class="text-accent-500">Women\'s Class</span>',
        f'{p["h1_1"]}\n            <span class="text-accent-500">{p["h1_2"]}</span>'
    )
    # Hero desc
    page = page.replace(
        'Core strength and glute activation using dumbbells and resistance bands \u2014 in a calm, supportive environment built for women.',
        p['hero_desc']
    )

    # Stats
    page = page.replace('<div class="stat-number">6</div>\n          <div class="stat-label">Weeks</div>',
                        f'<div class="stat-number">{p["weeks"]}</div>\n          <div class="stat-label">{p["weeks_label"]}</div>')
    page = page.replace('<div class="stat-number">$60</div>\n          <div class="stat-label">Per Week</div>',
                        f'<div class="stat-number">{p["price_per"]}</div>\n          <div class="stat-label">{p["price_label"]}</div>')
    page = page.replace('<div class="stat-number">10</div>\n          <div class="stat-label">Max Class Size</div>',
                        f'<div class="stat-number">{p["class_size"]}</div>\n          <div class="stat-label">{p["class_label"]}</div>')
    page = page.replace('<div class="stat-number">Thu</div>\n          <div class="stat-label">10:00\u201311:00 AM</div>',
                        f'<div class="stat-number">{p["stat_day"]}</div>\n          <div class="stat-label">{p["stat_time"]}</div>')

    # Overview
    page = page.replace('Strength Training Designed for Women', p['overview_h2'])
    page = page.replace(
        'Bells &amp; Bands is a ladies-only group class focused on building real core strength and glute activation using dumbbells and resistance bands. This isn\'t a generic fitness class \u2014 every exercise is selected to address the specific movement patterns women need most.',
        p['overview_p1']
    )
    page = page.replace(
        'In a calm, supportive environment, you\'ll work through progressive training that builds week on week. Whether you\'re returning from maternity leave, managing hypermobility, or simply want a structured approach to getting stronger \u2014 this class meets you where you are.',
        p['overview_p2']
    )

    # Who
    page = page.replace('Hypermobility or Joint Pain', p['who'][0][0])
    page = page.replace('Women dealing with hypermobility or joint pain who need strength work that stabilises rather than aggravates.', p['who'][0][1])
    page = page.replace('Postpartum Returners', p['who'][1][0])
    page = page.replace('Mothers returning to exercise after pregnancy who want guided, progressive training in a supportive space.', p['who'][1][1])
    page = page.replace('Beginners Welcome', p['who'][2][0])
    page = page.replace('Women new to strength training who want a structured introduction without feeling overwhelmed or out of place.', p['who'][2][1])

    # Includes - replace the list items
    old_includes = [
        '6 weeks of progressive group training sessions (Thursdays 10:00\u201311:00 AM)',
        'Core strength and glute activation programming using dumbbells and resistance bands',
        'At-home workout workbook so you can continue progress between sessions',
        'Weekly summary emails to keep you on track and reinforce key learnings',
        'Small class of max 10 participants for personalised attention',
    ]
    for i, old_item in enumerate(old_includes):
        if i < len(p['includes']):
            page = page.replace(old_item, p['includes'][i])

    # Schedule details card
    page = page.replace('Thursdays 10:00\u201311:00 AM</span>\n', f'{p["schedule_line"]}</span>\n')
    page = page.replace('$360 total ($60/week)', p['price_total'])

    # Instructor
    page = page.replace('Meet Keriann', f'Meet {p["instructor"]}')
    page = page.replace(
        'Keriann holds an HBS1 certification in Functional Patterns and a Bachelor of Health Science in Clinical Nutrition. Having recently returned from maternity leave herself, she brings first-hand understanding of the postpartum body and what it takes to rebuild strength safely.',
        p['bio1']
    )
    page = page.replace(
        'Her approach is patient, detail-oriented, and focused on building confidence through progressions that actually work. Keriann creates an environment where every woman feels supported and empowered to push their boundaries at their own pace.',
        p['bio2']
    )
    page = page.replace(
        f'Keriann \u2014 Bells and Bands instructor at FP Brisbane',
        f'{p["instructor"]} \u2014 {p["title"]} instructor at FP Brisbane'
    )

    # CTA
    page = page.replace('Ready to Join Bells &amp; Bands?', p['cta_h2'])
    page = page.replace(
        'Thursdays at 10am in Bulimba. 6 weeks of progressive strength training in a supportive, women-only environment.',
        p['cta_p']
    )

    with open(f'src/programs/{p["filename"]}', 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'Created {p["filename"]}')

print('All 5 pages created')
