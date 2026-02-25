"""Action dataclass and curated action data for the Toddler Timeline Planner."""
from dataclasses import dataclass, field


VALID_SWIM_LANES = (
    "sleep", "feeding", "clothing", "health",
    "development", "travel", "childcare", "safety",
)


@dataclass
class Action:
    id: str
    swim_lane: str
    title: str
    big_picture: str
    steps: list[str]
    trigger_type: str          # "age" | "season"
    age_months: tuple[int, int] | None
    seasons: list[str] | None
    priority: str              # "essential" | "recommended" | "nice_to_have"


ALL_ACTIONS: list[Action] = [
    # ── SLEEP ─────────────────────────────────────────────────────────────────
    Action(
        id="sleep-nap-transition-signs",
        swim_lane="sleep",
        title="Watch for 2-to-1 nap transition signs",
        big_picture=(
            "Between 14-18 months most toddlers start resisting the morning nap. "
            "Signs include refusing to settle, taking ages to fall asleep, or the "
            "afternoon nap getting pushed so late it wrecks bedtime."
        ),
        steps=[
            "Week 1: Note which naps are being refused or shortened",
            "Week 2: If morning nap is consistently refused, push it 15 mins later each day",
            "Week 3: Keep pushing until it merges into a single midday nap around 12:00-12:30",
        ],
        trigger_type="age", age_months=(14, 16), seasons=None,
        priority="essential",
    ),
    Action(
        id="sleep-nap-one-nap",
        swim_lane="sleep",
        title="Complete the move to one nap a day",
        big_picture=(
            "By 15-18 months most toddlers are on one nap. The sweet spot is usually "
            "12:30-2:30pm. Expect a cranky transition period of 2-3 weeks. Bring bedtime "
            "earlier temporarily (6:30-7pm) to compensate."
        ),
        steps=[
            "Week 1: Set a consistent one-nap schedule starting at 12:30",
            "Week 2: If overtired, bring bedtime forward to 6:30pm",
            "Week 3: Adjust nap start time based on wake windows (4.5-5.5 hrs)",
            "Week 4: Settle into the new rhythm - push bedtime back to 7pm if coping well",
        ],
        trigger_type="age", age_months=(15, 18), seasons=None,
        priority="essential",
    ),
    Action(
        id="sleep-18mo-regression",
        swim_lane="sleep",
        title="Prepare for the 18-month sleep regression",
        big_picture=(
            "Around 18 months separation anxiety peaks, molars are coming through, "
            "and language development causes mental leaps. Night waking and bedtime "
            "battles are common. It usually passes in 2-6 weeks."
        ),
        steps=[
            "Keep bedtime routine rock-solid consistent",
            "Offer comfort but avoid creating new sleep crutches",
            "Give Calpol/Nurofen if teething is causing pain at night",
            "This too shall pass - don't panic-change the routine",
        ],
        trigger_type="age", age_months=(17, 20), seasons=None,
        priority="essential",
    ),
    Action(
        id="sleep-summer-bag",
        swim_lane="sleep",
        title="Switch to a lightweight summer sleeping bag",
        big_picture=(
            "When room temperature hits 20°C+, switch to a 0.5 or 1.0 tog sleeping bag. "
            "Overheating is a risk. Use a room thermometer to guide the choice."
        ),
        steps=[
            "Buy a 0.5 tog and 1.0 tog bag in the right size",
            "Monitor room temp nightly - 0.5 tog for 24°C+, 1.0 tog for 20-24°C",
            "Dress in just a nappy + short-sleeve vest underneath on hot nights",
        ],
        trigger_type="season", age_months=None, seasons=["summer"],
        priority="essential",
    ),
    Action(
        id="sleep-toddler-bed",
        swim_lane="sleep",
        title="Consider toddler bed transition",
        big_picture=(
            "If your toddler is climbing out of the cot, it's time to switch. "
            "Otherwise, there's no rush - the cot is safer. Most kids move between "
            "2-3 years. Use a bed guard and keep the room fully childproofed."
        ),
        steps=[
            "Only switch if climbing out - the cot is safer",
            "Set up the toddler bed in the same spot as the cot",
            "Use a bed guard and ensure the room is fully childproofed",
            "Keep the same bedtime routine to maintain consistency",
        ],
        trigger_type="age", age_months=(24, 30), seasons=None,
        priority="recommended",
    ),
    Action(
        id="sleep-winter-bag",
        swim_lane="sleep",
        title="Switch to a warmer winter sleeping bag",
        big_picture=(
            "As room temperatures drop below 18°C, move to a 2.5 tog sleeping bag. "
            "Avoid loose blankets in the cot. Layer with a long-sleeve bodysuit underneath."
        ),
        steps=[
            "Check you have a 2.5 tog bag in the current size",
            "Use a room thermometer - 2.5 tog for 16-20°C",
            "Layer with a long-sleeve bodysuit + sleepsuit underneath",
        ],
        trigger_type="season", age_months=None, seasons=["autumn"],
        priority="essential",
    ),

    # ── FEEDING ───────────────────────────────────────────────────────────────
    Action(
        id="feeding-drop-daytime-bottles",
        swim_lane="feeding",
        title="Start dropping daytime bottles",
        big_picture=(
            "By 12-14 months, aim to transition from bottles to open cups or straw cups "
            "for all drinks. Start with daytime bottles - offer milk in a cup at meal times. "
            "Prolonged bottle use can affect teeth and speech development."
        ),
        steps=[
            "Week 1: Replace the mid-morning bottle with milk in an open cup",
            "Week 2: Replace the afternoon bottle with a straw cup",
            "Week 3: Offer water in cups between meals",
        ],
        trigger_type="age", age_months=(14, 15), seasons=None,
        priority="essential",
    ),
    Action(
        id="feeding-drop-bedtime-bottle",
        swim_lane="feeding",
        title="Drop the bedtime bottle",
        big_picture=(
            "The bedtime bottle is usually the last to go. Replace it with milk in a cup "
            "as part of the bedtime routine, before teeth brushing. This protects against "
            "tooth decay from milk pooling overnight."
        ),
        steps=[
            "Week 1: Offer milk in a cup 30 mins before bed, before brushing teeth",
            "Week 2: If resisted, try warm milk in a favourite cup",
            "Week 3: The bottle should be fully gone - stay firm",
        ],
        trigger_type="age", age_months=(15, 17), seasons=None,
        priority="essential",
    ),
    Action(
        id="feeding-fussy-phase",
        swim_lane="feeding",
        title="Navigate the fussy eating phase",
        big_picture=(
            "Between 16-20 months toddlers commonly become very selective eaters. "
            "This is developmental (neophobia - fear of new foods). Keep offering "
            "variety without pressure. It can take 15+ exposures before a food is accepted."
        ),
        steps=[
            "Offer 1 safe food they like alongside new foods at each meal",
            "Let them see you eating the same food - modelling works",
            "Don't force, bribe, or make a fuss - keep mealtimes relaxed",
            "Offer rejected foods again in different forms (raw, cooked, in a sauce)",
        ],
        trigger_type="age", age_months=(16, 20), seasons=None,
        priority="recommended",
    ),
    Action(
        id="feeding-cutlery",
        swim_lane="feeding",
        title="Introduce cutlery skills",
        big_picture=(
            "Around 18 months, start encouraging fork use (easier than a spoon for stabbing). "
            "Pre-load the fork for them at first. Expect a lot of mess. By 24 months most "
            "toddlers can manage a fork and are getting better with a spoon."
        ),
        steps=[
            "Start with a chunky toddler fork - pre-load it with food",
            "Let them practise with thick foods (banana, pasta, cheese)",
            "Introduce a spoon with thick foods like porridge or yoghurt",
            "Accept the mess - lay a mat under the highchair",
        ],
        trigger_type="age", age_months=(18, 22), seasons=None,
        priority="recommended",
    ),
    Action(
        id="feeding-self-feeding",
        swim_lane="feeding",
        title="Encourage independent self-feeding",
        big_picture=(
            "By 24 months most toddlers can self-feed reasonably well with a fork and spoon. "
            "Portion sizes should be roughly 1/4 of an adult portion. Offer 3 meals and "
            "2 snacks per day at regular times."
        ),
        steps=[
            "Let them serve themselves from small dishes where possible",
            "Praise attempts at self-feeding, not the amount eaten",
            "Establish regular meal and snack times to build routine",
        ],
        trigger_type="age", age_months=(22, 26), seasons=None,
        priority="recommended",
    ),
    Action(
        id="feeding-milk-intake",
        swim_lane="feeding",
        title="Right-size milk intake",
        big_picture=(
            "Too much milk (over 350ml/day) can fill toddlers up and reduce appetite for solids. "
            "It can also reduce iron absorption. Full-fat cow's milk is fine from 12 months. "
            "Aim for about 300ml per day across all dairy."
        ),
        steps=[
            "Track total milk intake including yoghurt and cheese",
            "Aim for roughly 300ml whole milk per day",
            "If appetite for food is poor, reduce milk and offer water instead",
        ],
        trigger_type="age", age_months=(14, 18), seasons=None,
        priority="recommended",
    ),

    # ── CLOTHING & GEAR ───────────────────────────────────────────────────────
    Action(
        id="clothing-spring-layers",
        swim_lane="clothing",
        title="Get spring outdoor gear sorted",
        big_picture=(
            "Spring weather is unpredictable. Lightweight layers, a puddle suit, wellies, "
            "and a sun hat cover most scenarios. Check sizes - feet grow fast at this age."
        ),
        steps=[
            "Buy lightweight layering tops and a waterproof puddle suit",
            "Get wellies in current size (measure feet first)",
            "Sun hat for brighter days",
            "Measure feet - book a shoe fitting if walking confidently",
        ],
        trigger_type="season", age_months=None, seasons=["spring"],
        priority="essential",
    ),
    Action(
        id="clothing-summer-gear",
        swim_lane="clothing",
        title="Get summer sun and swim gear",
        big_picture=(
            "UV swimsuit, swim nappies, SPF 50 sun cream, and a sun hat with neck flap "
            "are essentials. Also get a lightweight 0.5-1 tog sleeping bag for warm nights."
        ),
        steps=[
            "Buy a UV swimsuit (long-sleeved) and swim nappies",
            "Stock up on SPF 50 sun cream - apply 30 mins before going out",
            "Get a wide-brim sun hat with neck flap",
            "Buy lightweight summer clothes in current + next size up",
        ],
        trigger_type="season", age_months=None, seasons=["summer"],
        priority="essential",
    ),
    Action(
        id="clothing-autumn-warmth",
        swim_lane="clothing",
        title="Transition to autumn/winter wardrobe",
        big_picture=(
            "Time for warmer layers, a waterproof jacket, and checking shoe sizes. "
            "Feet grow rapidly at this age - measure every 6-8 weeks."
        ),
        steps=[
            "Buy a waterproof jacket and warm layers",
            "Measure feet and get shoes fitted if due",
            "Check sleeping bag size - may need to go up a size",
            "Look for next-size-up winter clothes in sales",
        ],
        trigger_type="season", age_months=None, seasons=["autumn"],
        priority="essential",
    ),
    Action(
        id="clothing-winter-gear",
        swim_lane="clothing",
        title="Winter-proof the wardrobe",
        big_picture=(
            "Snowsuit or pramsuit for outdoor time, warm sleeping bag (2.5 tog), "
            "and layered clothing. Avoid loose blankets in the cot."
        ),
        steps=[
            "Get a snowsuit/pramsuit in current size",
            "Ensure 2.5 tog sleeping bag fits properly",
            "Stock up on long-sleeve bodysuits and warm layers",
            "Warm hat, mittens, and warm socks or booties for outdoor trips",
        ],
        trigger_type="season", age_months=None, seasons=["winter"],
        priority="essential",
    ),
    Action(
        id="clothing-shoe-check",
        swim_lane="clothing",
        title="Regular shoe size check",
        big_picture=(
            "Toddler feet grow incredibly fast - up to 2 sizes in 6 months. "
            "Ill-fitting shoes can affect how they walk. Get professionally measured "
            "every 6-8 weeks once they're walking confidently."
        ),
        steps=[
            "Book a shoe fitting at a children's shoe shop",
            "Check current shoes aren't too tight (thumb-width gap at toe)",
            "Buy one pair of well-fitted shoes - they'll outgrow them quickly",
        ],
        trigger_type="age", age_months=(14, 26), seasons=None,
        priority="recommended",
    ),

    # ── HEALTH & MEDICAL ─────────────────────────────────────────────────────
    Action(
        id="health-15mo-review",
        swim_lane="health",
        title="Health visitor developmental review",
        big_picture=(
            "Around 15 months your health visitor should check in on developmental "
            "progress - walking, communication, social skills. This is a good time "
            "to raise any concerns. Contact your health visiting team if not scheduled."
        ),
        steps=[
            "Check if your health visitor review is booked",
            "Note any questions about development, sleep, or feeding",
            "Bring the red book (PCHR) to the appointment",
        ],
        trigger_type="age", age_months=(15, 16), seasons=None,
        priority="essential",
    ),
    Action(
        id="health-dental-registration",
        swim_lane="health",
        title="Register with an NHS dentist",
        big_picture=(
            "NHS dental care is free for under-18s. Register and book a first check-up "
            "by 18 months. The dentist will check tooth development and give advice on "
            "brushing and diet. Use fluoride toothpaste (1000ppm+) from 12 months."
        ),
        steps=[
            "Find a local NHS dentist accepting children - check NHS.uk",
            "Book the first appointment",
            "Start brushing twice daily with a smear of fluoride toothpaste if not already",
        ],
        trigger_type="age", age_months=(16, 19), seasons=None,
        priority="essential",
    ),
    Action(
        id="health-teething-molars",
        swim_lane="health",
        title="Prepare for canines and molars",
        big_picture=(
            "The canine teeth and first molars typically come through between 16-24 months. "
            "Molars are particularly painful. Stock up on pain relief and teething aids."
        ),
        steps=[
            "Stock up on Calpol and Nurofen (alternate every 3 hours if needed)",
            "Get teething rings that can be chilled in the fridge",
            "Expect disrupted sleep and fussiness - be patient",
            "Offer cold foods like chilled cucumber or frozen fruit in a mesh feeder",
        ],
        trigger_type="age", age_months=(16, 24), seasons=None,
        priority="essential",
    ),
    Action(
        id="health-2-year-review",
        swim_lane="health",
        title="Schedule the 2-year developmental review",
        big_picture=(
            "The 2-year integrated review combines the health visitor check and early "
            "years assessment. It covers communication, motor skills, social development, "
            "and behaviour. This is an important milestone check."
        ),
        steps=[
            "Contact your health visiting team to book the review",
            "Fill in any pre-appointment questionnaires (ASQ)",
            "Note any concerns about speech, behaviour, or development to discuss",
            "Bring the red book (PCHR)",
        ],
        trigger_type="age", age_months=(23, 26), seasons=None,
        priority="essential",
    ),
    Action(
        id="health-vaccinations-check",
        swim_lane="health",
        title="Check vaccination schedule is up to date",
        big_picture=(
            "By 13 months your toddler should have had MMR, Hib/MenC booster, and "
            "pneumococcal booster. Check the red book. If any were missed, contact "
            "your GP to catch up."
        ),
        steps=[
            "Check the red book for completed vaccinations",
            "If any are missing, call the GP surgery to book catch-up jabs",
            "Note the next scheduled vaccination (pre-school boosters at 3y4m)",
        ],
        trigger_type="age", age_months=(14, 15), seasons=None,
        priority="essential",
    ),

    # ── DEVELOPMENT & MILESTONES ──────────────────────────────────────────────
    Action(
        id="dev-walking-confidence",
        swim_lane="development",
        title="Support confident walking",
        big_picture=(
            "Most toddlers walk independently between 12-18 months. Once walking, "
            "they need practice on different surfaces and gradients. Barefoot indoors "
            "is best for foot development. Outdoors, get properly fitted first shoes."
        ),
        steps=[
            "Encourage barefoot walking indoors on different textures",
            "Practice walking on grass, sand, and gentle slopes",
            "Get first shoes professionally fitted once walking outdoors confidently",
            "Celebrate and encourage - don't rush, every child's timeline is different",
        ],
        trigger_type="age", age_months=(14, 17), seasons=None,
        priority="essential",
    ),
    Action(
        id="dev-first-words",
        swim_lane="development",
        title="Encourage first words and communication",
        big_picture=(
            "Between 14-18 months, first words emerge alongside pointing and gesturing. "
            "Narrate your day, read together, and respond to all communication attempts. "
            "Expect 10-50 words by 18 months (understanding far more than they can say)."
        ),
        steps=[
            "Narrate what you're doing throughout the day",
            "Read together daily - point at pictures and name them",
            "Respond to pointing and gestures with words",
            "Don't correct - just model the right word back ('yes, that's a dog!')",
        ],
        trigger_type="age", age_months=(14, 18), seasons=None,
        priority="essential",
    ),
    Action(
        id="dev-word-explosion",
        swim_lane="development",
        title="Support the word explosion",
        big_picture=(
            "Between 16-20 months, vocabulary often takes off rapidly. Toddlers start "
            "combining gestures with words and understanding simple instructions. "
            "This is also when frustration and tantrums increase as they can't yet "
            "express everything they want to say."
        ),
        steps=[
            "Expand on their words: if they say 'car', say 'yes, a big red car!'",
            "Give simple choices: 'banana or apple?'",
            "Follow simple instructions together: 'let's get your shoes'",
            "Be patient with frustration - acknowledge their feelings with words",
        ],
        trigger_type="age", age_months=(16, 20), seasons=None,
        priority="essential",
    ),
    Action(
        id="dev-tantrums",
        swim_lane="development",
        title="Prepare for tantrums and big emotions",
        big_picture=(
            "Tantrums typically start around 18 months and peak around 2 years. "
            "They happen because toddlers feel big emotions but can't regulate them yet. "
            "Stay calm, keep them safe, and name their feelings."
        ),
        steps=[
            "Stay calm - your regulation teaches them regulation",
            "Name the emotion: 'you're feeling frustrated because...'",
            "Offer comfort once the storm passes",
            "Avoid giving in to prevent tantrums - that teaches the wrong lesson",
        ],
        trigger_type="age", age_months=(18, 26), seasons=None,
        priority="essential",
    ),
    Action(
        id="dev-two-word-combos",
        swim_lane="development",
        title="Encourage two-word combinations",
        big_picture=(
            "Between 20-24 months, toddlers start putting two words together: "
            "'more milk', 'daddy gone', 'big truck'. Pretend play also emerges - "
            "feeding teddies, talking on toy phones. These are great signs."
        ),
        steps=[
            "Model two-word phrases: 'milk gone', 'shoes on'",
            "Encourage pretend play with dolls, kitchen sets, phones",
            "Read stories with simple sentences and pause for them to fill in words",
            "Ask simple questions: 'where's teddy?', 'what's that?'",
        ],
        trigger_type="age", age_months=(20, 24), seasons=None,
        priority="recommended",
    ),
    Action(
        id="dev-physical-skills",
        swim_lane="development",
        title="Develop physical skills - running, climbing, kicking",
        big_picture=(
            "Between 20-26 months, toddlers get faster, bolder, and more coordinated. "
            "They can run (unsteadily at first), kick a ball, climb stairs with support, "
            "and jump with both feet by around 24 months."
        ),
        steps=[
            "Visit playgrounds regularly for climbing, sliding, swinging",
            "Practise kicking and throwing balls in the garden or park",
            "Practise stairs together (holding hands, one step at a time)",
            "Allow safe risk-taking - let them climb and explore",
        ],
        trigger_type="age", age_months=(20, 26), seasons=None,
        priority="recommended",
    ),

    # ── TRAVEL & HOLIDAYS ─────────────────────────────────────────────────────
    Action(
        id="travel-book-holiday",
        swim_lane="travel",
        title="Book your summer beach holiday",
        big_picture=(
            "Book flights and accommodation 3-4 months ahead for the best options. "
            "Check passport validity - apply/renew via HMPO (currently 4-6 weeks). "
            "Choose a child-friendly destination with a shallow beach and nearby pharmacy."
        ),
        steps=[
            "Check your toddler's passport is valid (apply via HMPO if needed)",
            "Book flights - consider nap-time flights for easier travel",
            "Book child-friendly accommodation with a cot and blackout options",
            "Research the destination: nearest hospital, pharmacy, supermarket",
        ],
        trigger_type="season", age_months=None, seasons=["spring"],
        priority="essential",
    ),
    Action(
        id="travel-gear-prep",
        swim_lane="travel",
        title="Get travel gear sorted",
        big_picture=(
            "Two months before the trip, get the key gear: travel car seat or check "
            "airline policy, UV pop-up tent for the beach, travel blackout blind "
            "(Gro Anywhere Blind), and swim nappies."
        ),
        steps=[
            "Buy or borrow a travel car seat (check airline compatibility)",
            "Get a UV pop-up tent for beach shade",
            "Buy a Gro Anywhere Blind (portable blackout blind for hotel rooms)",
            "Stock up on swim nappies in current size",
        ],
        trigger_type="season", age_months=None, seasons=["spring"],
        priority="essential",
    ),
    Action(
        id="travel-packing",
        swim_lane="travel",
        title="Pack the holiday essentials",
        big_picture=(
            "One month before: build your pack list. Travel pharmacy is critical "
            "(Calpol, Nurofen, plasters, thermometer, Piriton). Entertainment for "
            "the flight, and don't forget the EHIC/GHIC card."
        ),
        steps=[
            "Travel pharmacy: Calpol, Nurofen, plasters, thermometer, Piriton, sun cream",
            "Check EHIC/GHIC card is valid",
            "Download CBeebies episodes and pack sticker books for the flight",
            "Pack favourite comforter/toy, snacks, change of clothes in hand luggage",
        ],
        trigger_type="season", age_months=None, seasons=["summer"],
        priority="essential",
    ),
    Action(
        id="travel-on-holiday",
        swim_lane="travel",
        title="Holiday routine and sun safety",
        big_picture=(
            "On the trip, try to stick to nap and bedtime routines as much as possible. "
            "Reapply sun cream every 2 hours and after swimming. Keep out of direct sun "
            "between 11am-3pm. Allow extra time for everything."
        ),
        steps=[
            "Maintain nap time and bedtime routine as closely as possible",
            "Use the UV tent and blackout blind to replicate home sleep environment",
            "Apply sun cream every 2 hours and after water",
            "Stay in shade 11am-3pm - use the pop-up tent on the beach",
        ],
        trigger_type="season", age_months=None, seasons=["summer"],
        priority="essential",
    ),

    # ── CHILDCARE & SOCIAL ────────────────────────────────────────────────────
    Action(
        id="childcare-toddler-groups",
        swim_lane="childcare",
        title="Start toddler groups or music classes",
        big_picture=(
            "Toddler groups, music sessions (e.g. Jo Jingles, Monkey Music), and "
            "library rhyme time are great for socialisation and building routine. "
            "At this age it's about exposure and fun, not structured learning."
        ),
        steps=[
            "Search for local toddler groups on Facebook or your council website",
            "Try a music class like Jo Jingles, Monkey Music, or similar",
            "Check your local library for free rhyme time sessions",
            "Aim for 1-2 regular weekly activities to build a routine",
        ],
        trigger_type="age", age_months=(14, 18), seasons=None,
        priority="recommended",
    ),
    Action(
        id="childcare-nursery-settling",
        swim_lane="childcare",
        title="Plan nursery settling-in sessions",
        big_picture=(
            "If starting nursery, plan 2-4 weeks of settling-in sessions. Start with "
            "short stays (1-2 hours) building up to full sessions. Separation anxiety "
            "is normal at this age - a confident goodbye routine helps."
        ),
        steps=[
            "Book settling-in sessions 2-4 weeks before the start date",
            "Start with 1-2 hour visits, building up gradually",
            "Develop a goodbye routine: quick kiss, wave, and leave confidently",
            "Send a comfort item (favourite toy or muslin) with them",
        ],
        trigger_type="age", age_months=(14, 20), seasons=None,
        priority="recommended",
    ),
    Action(
        id="childcare-parallel-play",
        swim_lane="childcare",
        title="Understand parallel play is normal",
        big_picture=(
            "Between 18-24 months, toddlers play alongside other children but not "
            "cooperatively with them. This is completely normal developmental behaviour. "
            "Sharing is not yet an expected skill - don't worry about it."
        ),
        steps=[
            "Arrange regular playdates for exposure to other children",
            "Don't force sharing - model it by narrating: 'I'm sharing my biscuit with you'",
            "Have duplicate popular toys available to reduce conflicts",
            "Praise any spontaneous sharing but don't punish lack of it",
        ],
        trigger_type="age", age_months=(18, 24), seasons=None,
        priority="recommended",
    ),
    Action(
        id="childcare-preschool-research",
        swim_lane="childcare",
        title="Research pre-school options",
        big_picture=(
            "From age 2 some children start pre-school (especially if you're eligible "
            "for the 2-year-old funded childcare offer). Start researching local options "
            "and visiting settings. Check eligibility for 15 or 30 hours funded childcare."
        ),
        steps=[
            "Research local pre-schools and nurseries - check Ofsted reports",
            "Check eligibility for 2-year-old funded childcare on gov.uk",
            "Visit 2-3 settings and ask about their approach and routine",
            "Apply/register early - popular settings have waiting lists",
        ],
        trigger_type="age", age_months=(22, 26), seasons=None,
        priority="recommended",
    ),

    # ── SAFETY & CHILDPROOFING ────────────────────────────────────────────────
    Action(
        id="safety-walking-recheck",
        swim_lane="safety",
        title="Re-check childproofing for a walker",
        big_picture=(
            "Once your toddler walks confidently, re-check everything at their new "
            "height. They can now reach surfaces, pull things off tables, and access "
            "areas that were previously safe. Anchor all heavy furniture to walls."
        ),
        steps=[
            "Walk through every room at toddler height - what can they reach?",
            "Anchor bookcases, dressers, and TV to the wall with anti-tip straps",
            "Install stair gates top and bottom if not already done",
            "Put corner guards on sharp furniture edges",
            "Move breakables, medicines, and cleaning products out of reach",
        ],
        trigger_type="age", age_months=(14, 16), seasons=None,
        priority="essential",
    ),
    Action(
        id="safety-climbing-phase",
        swim_lane="safety",
        title="Prepare for the climbing phase",
        big_picture=(
            "Around 18-20 months toddlers discover climbing. They will climb chairs, "
            "sofas, tables, and stairs. Move chairs away from countertops and windows. "
            "Window locks are essential - ensure all upstairs windows have restrictors."
        ),
        steps=[
            "Install window restrictors on all upstairs windows",
            "Move chairs and step stools away from kitchen counters",
            "Check stair gates are still secure and properly fitted",
            "Supervise around furniture they can climb on",
        ],
        trigger_type="age", age_months=(18, 21), seasons=None,
        priority="essential",
    ),
    Action(
        id="safety-reaching-higher",
        swim_lane="safety",
        title="Move hazards higher as reach increases",
        big_picture=(
            "By 20-24 months toddlers can reach higher surfaces by climbing on things "
            "and standing on tiptoes. Medicines, cleaning products, sharp objects, and "
            "hot drinks need to be well out of reach."
        ),
        steps=[
            "Move all medicines to a high, locked cupboard",
            "Move cleaning products to a high cupboard or use childproof locks",
            "Never leave hot drinks within reach - use the back of worktops",
            "Install toilet locks if your toddler has discovered the bathroom",
        ],
        trigger_type="age", age_months=(20, 24), seasons=None,
        priority="essential",
    ),
    Action(
        id="safety-door-opening",
        swim_lane="safety",
        title="Prepare for door-opening abilities",
        big_picture=(
            "Around 24 months many toddlers learn to open door handles. Install "
            "door handle covers on exterior doors and any rooms with hazards. "
            "Consider a stair gate at the top of stairs even if they can navigate them."
        ),
        steps=[
            "Install door handle covers on front door, back door, and any hazardous rooms",
            "Consider a door chain at toddler-proof height on exterior doors",
            "Check garden gate is secure and toddler-proof",
            "Ensure bathroom door can be opened from outside (in case of lock-ins)",
        ],
        trigger_type="age", age_months=(23, 26), seasons=None,
        priority="essential",
    ),
    Action(
        id="safety-water-awareness",
        swim_lane="safety",
        title="Water safety awareness",
        big_picture=(
            "As summer and holiday approaches, be extra vigilant about water safety. "
            "Toddlers can drown in just a few centimetres of water. Never leave them "
            "unattended near water - pools, baths, ponds, paddling pools."
        ),
        steps=[
            "Never leave your toddler unattended near any water",
            "Empty paddling pools after every use",
            "Consider toddler swim lessons for water confidence",
            "If visiting pools or beaches, always be within arm's reach",
        ],
        trigger_type="season", age_months=None, seasons=["spring", "summer"],
        priority="essential",
    ),
]
